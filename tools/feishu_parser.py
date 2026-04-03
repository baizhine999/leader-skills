#!/usr/bin/env python3
"""
feishu_parser.py — 飞书文档解析器
将飞书导出的 JSON/Markdown 文件解析为 LeaderBuilder 可用的原始材料格式
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional


# ─── 飞书文档结构常量 ───────────────────────────────────────────────────────────

FEISHU_MSG_TYPES = {
    "text": "文本消息",
    "post": "富文本",
    "interactive": "卡片消息",
    "system": "系统消息",
    "file": "文件",
}

# ─── 解析器 ────────────────────────────────────────────────────────────────────


class FeishuParser:
    """
    支持三种飞书导出格式：
    1. 飞书群聊 JSON 导出（`/export` 功能）
    2. 飞书文档 Markdown 导出
    3. 飞书会议纪要文本
    """

    def __init__(self, source_path: str, target_name: str):
        self.source_path = Path(source_path)
        self.target_name = target_name
        self.messages: list[dict] = []
        self.quotes: list[str] = []       # 直接引语
        self.behaviors: list[str] = []    # 行为描述
        self.context: str = ""            # 原始文本

    # ── 入口 ───────────────────────────────────────────────────────────────────

    def parse(self) -> dict:
        """解析文件，返回 leader_builder.py 可用的原始材料 dict"""
        suffix = self.source_path.suffix.lower()

        if suffix == ".json":
            return self._parse_json()
        elif suffix in (".md", ".txt"):
            return self._parse_text()
        else:
            raise ValueError(f"不支持的格式: {suffix}。支持 .json / .md / .txt")

    # ── JSON 模式 ──────────────────────────────────────────────────────────────

    def _parse_json(self) -> dict:
        with open(self.source_path, encoding="utf-8") as f:
            data = json.load(f)

        # 尝试识别是群聊 JSON 还是文档 JSON
        if "messages" in data:
            return self._parse_chat_json(data["messages"])
        elif "blocks" in data:
            return self._parse_doc_json(data["blocks"])
        else:
            # 尝试直接当作消息列表
            if isinstance(data, list):
                return self._parse_chat_json(data)
            raise ValueError("无法识别的飞书 JSON 结构")

    def _parse_chat_json(self, messages: list) -> dict:
        """解析群聊消息 JSON，提取目标人物的发言"""
        for msg in messages:
            sender_name = self._extract_sender(msg)
            if not sender_name:
                continue

            # 只提取目标人物（模糊匹配）
            if self.target_name.lower() not in sender_name.lower():
                continue

            content = self._extract_text(msg)
            if content and len(content) > 10:
                self.quotes.append(content)

        return self._build_output()

    def _parse_doc_json(self, blocks: list) -> dict:
        """解析飞书文档 block 结构"""
        full_text = []
        for block in blocks:
            block_type = block.get("block_type", "")
            if block_type in (1, 2, 3, 4, 5):  # paragraph, heading
                text = self._extract_block_text(block)
                if text:
                    full_text.append(text)

        self.context = "\n".join(full_text)
        return self._parse_text_content(self.context)

    # ── Markdown/文本 模式 ─────────────────────────────────────────────────────

    def _parse_text(self) -> dict:
        with open(self.source_path, encoding="utf-8") as f:
            content = f.read()
        self.context = content
        return self._parse_text_content(content)

    def _parse_text_content(self, content: str) -> dict:
        """从文本中提取目标人物的引语（通过 「名字：」 格式识别）"""
        # 匹配「老王：」「张总：」「{target_name}说：」等格式
        pattern = rf"(?:{re.escape(self.target_name)}[：:说道表示补充强调认为])\s*(.+?)(?=\n|$)"
        matches = re.findall(pattern, content, re.MULTILINE)
        self.quotes.extend([m.strip() for m in matches if len(m.strip()) > 5])

        # 提取以引号包裹的句子（可能是引语）
        quote_pattern = r'[「『"](.*?)[」』"]'
        quoted = re.findall(quote_pattern, content)
        for q in quoted:
            if len(q) > 10:
                self.quotes.append(f'（引用自文档）「{q}」')

        # 提取行为描述（会议纪要常见格式：「他要求/他强调/他指出」）
        behavior_pattern = rf"(?:他|{re.escape(self.target_name)})(?:要求|强调|指出|提出|坚持|质疑|表示|认为|说)([^。\n]+)"
        behaviors = re.findall(behavior_pattern, content)
        self.behaviors.extend([b.strip() for b in behaviors])

        return self._build_output()

    # ── 输出 ───────────────────────────────────────────────────────────────────

    def _build_output(self) -> dict:
        return {
            "source": str(self.source_path),
            "target_name": self.target_name,
            "quotes": self.quotes,
            "behaviors": self.behaviors,
            "summary": f"共提取引语 {len(self.quotes)} 条，行为描述 {len(self.behaviors)} 条",
        }

    # ── 工具函数 ───────────────────────────────────────────────────────────────

    def _extract_sender(self, msg: dict) -> str:
        """尝试多种字段名提取发送者"""
        for key in ("sender_name", "sender", "from_name", "name", "user_name"):
            val = msg.get(key, "")
            if val:
                return str(val)
        return ""

    def _extract_text(self, msg: dict) -> str:
        """提取消息文本内容"""
        content = msg.get("content", msg.get("body", msg.get("text", "")))
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, dict):
            # text 类型
            return content.get("text", "").strip()
        return ""

    def _extract_block_text(self, block: dict) -> str:
        """提取飞书文档 block 的纯文本"""
        elements = block.get("elements", [])
        parts = []
        for el in elements:
            if "text_run" in el:
                parts.append(el["text_run"].get("content", ""))
        return "".join(parts).strip()


# ─── CLI 入口 ──────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 3:
        print("用法: python feishu_parser.py <飞书导出文件路径> <目标人物名字>")
        print("示例: python feishu_parser.py ./export.json 老王")
        sys.exit(1)

    source_path = sys.argv[1]
    target_name = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    parser = FeishuParser(source_path, target_name)
    result = parser.parse()

    print(f"\n✅ 解析完成：{result['summary']}")
    print(f"\n📝 提取的引语（前5条）：")
    for i, q in enumerate(result["quotes"][:5], 1):
        print(f"  {i}. {q}")

    if output_path:
        out = Path(output_path)
    else:
        # 与原文件同目录，避免丢失路径
        out = Path(source_path).parent / (Path(source_path).stem + "_parsed.json")

    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n💾 结果已保存至: {out}")
    print("\n💡 可将此文件传给 leader_builder.py --materials 参数")


if __name__ == "__main__":
    main()
