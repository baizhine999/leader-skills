#!/usr/bin/env python3
"""
email_parser.py — 邮件解析器
解析 .eml 或 .mbox 格式的邮件文件，提取目标人物的措辞与行为特征
"""

import email
import email.policy
import json
import mailbox
import re
import sys
from email.header import decode_header
from pathlib import Path
from typing import Optional


# ─── 解析器 ────────────────────────────────────────────────────────────────────


class EmailParser:
    """
    支持两种格式：
    - .eml：单封邮件
    - .mbox：邮件包（导出的归档文件）

    解析策略：
    - 发件人匹配目标人物（名字或邮箱）
    - 提取正文（去除引用部分，只保留当前层）
    - 识别命令式语句与质问式语句（Leader 风格标记）
    """

    def __init__(self, source_path: str, target_name: str, target_email: str = ""):
        self.source_path = Path(source_path)
        self.target_name = target_name
        self.target_email = target_email.lower()
        self.quotes: list[str] = []
        self.behaviors: list[str] = []
        self.metadata: dict = {"subject_keywords": [], "recipients": set()}

    # ── 入口 ───────────────────────────────────────────────────────────────────

    def parse(self) -> dict:
        suffix = self.source_path.suffix.lower()
        if suffix == ".mbox":
            return self._parse_mbox()
        elif suffix == ".eml":
            return self._parse_eml()
        else:
            raise ValueError(f"不支持的格式: {suffix}。支持 .eml / .mbox")

    # ── .eml 格式 ──────────────────────────────────────────────────────────────

    def _parse_eml(self) -> dict:
        with open(self.source_path, "rb") as f:
            msg = email.message_from_binary_file(f, policy=email.policy.default)
        self._process_message(msg)
        return self._build_output()

    # ── .mbox 格式 ─────────────────────────────────────────────────────────────

    def _parse_mbox(self) -> dict:
        mbox = mailbox.mbox(str(self.source_path))
        count = 0
        for msg in mbox:
            self._process_message(msg)
            count += 1
        print(f"  共扫描 {count} 封邮件")
        return self._build_output()

    # ── 邮件处理 ───────────────────────────────────────────────────────────────

    def _process_message(self, msg) -> None:
        """处理单封邮件"""
        # 检查是否为目标人物发送
        from_field = self._decode_header_str(msg.get("From", ""))
        if not self._is_target(from_field):
            return

        # 提取主题关键词
        subject = self._decode_header_str(msg.get("Subject", ""))
        if subject:
            self.metadata["subject_keywords"].append(subject)

        # 提取正文
        body = self._extract_body(msg)
        if not body:
            return

        # 去除引用部分（> 开头的行）
        clean_body = self._strip_quoted(body)
        if len(clean_body) < 20:
            return

        # 提取语句
        sentences = self._split_sentences(clean_body)
        for s in sentences:
            s = s.strip()
            if len(s) < 10:
                continue
            if self._is_command_or_pressure(s):
                self.behaviors.append(s)
            elif len(s) > 20:
                self.quotes.append(s)

    def _is_target(self, from_field: str) -> bool:
        """判断发件人是否为目标人物"""
        if self.target_name and self.target_name.lower() in from_field.lower():
            return True
        if self.target_email and self.target_email in from_field.lower():
            return True
        return False

    def _extract_body(self, msg) -> str:
        """提取纯文本正文"""
        body_parts = []
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == "text/plain":
                    try:
                        body_parts.append(part.get_content())
                    except Exception:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_parts.append(payload.decode("utf-8", errors="replace"))
        else:
            try:
                body_parts.append(msg.get_content())
            except Exception:
                payload = msg.get_payload(decode=True)
                if payload:
                    body_parts.append(payload.decode("utf-8", errors="replace"))
        return "\n".join(body_parts)

    def _strip_quoted(self, text: str) -> str:
        """去除邮件引用（> 开头的行和 On ... wrote: 标记之后的内容）"""
        lines = text.split("\n")
        clean_lines = []
        in_quote = False
        for line in lines:
            stripped = line.strip()
            # 英文引用标记
            if re.match(r"On .+ wrote:", stripped):
                in_quote = True
            if stripped.startswith(">"):
                continue
            if in_quote:
                continue
            clean_lines.append(line)
        return "\n".join(clean_lines)

    def _split_sentences(self, text: str) -> list[str]:
        """按中文句号、英文句号、换行分句"""
        sentences = re.split(r"[。！？\n]+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _is_command_or_pressure(self, s: str) -> bool:
        """识别命令式或施压式语句"""
        pressure_keywords = [
            "必须", "一定要", "需要你", "要求", "马上", "立即", "今天内",
            "why", "为什么还没", "什么时候能", "再不", "别告诉我"
        ]
        return any(kw in s for kw in pressure_keywords)

    def _decode_header_str(self, header_val: str) -> str:
        """解码邮件 header（处理 =?utf-8?...?= 格式）"""
        decoded_parts = decode_header(header_val)
        parts = []
        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                parts.append(part.decode(charset or "utf-8", errors="replace"))
            else:
                parts.append(part)
        return "".join(parts)

    # ── 输出 ───────────────────────────────────────────────────────────────────

    def _build_output(self) -> dict:
        return {
            "source": str(self.source_path),
            "target_name": self.target_name,
            "quotes": self.quotes[:50],  # 最多50条
            "behaviors": self.behaviors[:30],
            "metadata": {
                "subject_keywords": list(set(self.metadata["subject_keywords"]))[:20],
            },
            "summary": f"共提取引语 {len(self.quotes)} 条，施压行为 {len(self.behaviors)} 条",
        }


# ─── CLI 入口 ──────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 3:
        print("用法: python email_parser.py <邮件文件.eml/.mbox> <目标人物名字> [邮箱地址]")
        print("示例1: python email_parser.py ./inbox.mbox 老王")
        print("示例2: python email_parser.py ./boss.eml 王总 wang@company.com")
        sys.exit(1)

    source_path = sys.argv[1]
    target_name = sys.argv[2]
    target_email = sys.argv[3] if len(sys.argv) > 3 else ""
    output_path = sys.argv[4] if len(sys.argv) > 4 else None

    parser = EmailParser(source_path, target_name, target_email)
    result = parser.parse()

    print(f"\n✅ 解析完成：{result['summary']}")
    print(f"\n📝 施压行为示例（前3条）：")
    for i, b in enumerate(result["behaviors"][:3], 1):
        print(f"  {i}. {b}")

    if output_path:
        out = Path(output_path)
    else:
        # 与原文件同目录，避免丢失路径
        out = Path(source_path).parent / (Path(source_path).stem + "_parsed.json")

    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n💾 结果已保存至: {out}")
    print("💡 可将此文件传给 leader_builder.py --materials 参数")


if __name__ == "__main__":
    main()
