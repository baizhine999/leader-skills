#!/usr/bin/env python3
"""
skill_writer.py — Leader Skill 文件写入器
生成和管理 leaders/ 目录下的三文件结构（meta.json / persona.md / work.md）
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

# ─── 配置 ──────────────────────────────────────────────────────────────────────

LEADERS_DIR = Path(__file__).parent.parent / "leaders"
TEMPLATE_DIR = LEADERS_DIR / "_template"

# ─── 核心类 ────────────────────────────────────────────────────────────────────


class SkillWriter:
    """
    从结构化 dict（通常由 leader_builder.py 生成）写出三文件。
    支持「新建 / 更新 / 校验」三个模式。
    """

    def __init__(self, leader_dir: str):
        self.dir_name = leader_dir
        self.target_dir = LEADERS_DIR / leader_dir
        self.template_dir = TEMPLATE_DIR

    # ── 新建 ───────────────────────────────────────────────────────────────────

    def create(self, data: dict, overwrite: bool = False) -> None:
        """
        从 data dict 新建 leader 目录和三文件。
        data 格式由 leader_builder.py 的 build() 方法输出。
        """
        if self.target_dir.exists() and not overwrite:
            print(f"⚠️  目录已存在: {self.target_dir}")
            print("使用 overwrite=True 或 update() 方法更新")
            return

        self.target_dir.mkdir(parents=True, exist_ok=True)

        self._write_meta(data.get("meta", {}))
        self._write_persona(data.get("persona", {}))
        self._write_work(data.get("work", {}))

        print(f"✅ Leader 技能文件已创建: {self.target_dir}")

    # ── 更新 ───────────────────────────────────────────────────────────────────

    def update(self, field: str, value, sub_key: str = "") -> None:
        """
        局部更新某个字段（由 correction_handler 触发）。
        field: 具体的 meta 字段名（如 'flavor'/'intensity'）| 'signature_phrase'
        若 field='meta' 且 value 是 dict，则批量更新多个字段。
        """
        if field == "meta" and isinstance(value, dict):
            # 批量更新多个 meta 字段
            for k, v in value.items():
                self._update_meta(k, v)
        elif field in self._meta_fields():
            self._update_meta(field, value)
        elif field == "signature_phrase":
            self._append_phrase(value)
        else:
            print(f"⚠️  不支持的字段更新: {field}")

    def _update_meta(self, field: str, value) -> None:
        meta_path = self.target_dir / "meta.json"
        if not meta_path.exists():
            print("❌ meta.json 不存在")
            return
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        meta[field] = value
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ meta.json[{field}] 已更新为: {value}")

    def _append_phrase(self, phrase: str) -> None:
        persona_path = self.target_dir / "persona.md"
        if not persona_path.exists():
            return
        content = persona_path.read_text(encoding="utf-8")
        # 找到 signature_phrases 列表块（用 [^\n]+ 避免跨行误匹配）
        pattern = r"(## 金句库[^\n]*\n)((?:- [^\n]+\n)*)"
        def replacer(m):
            return m.group(1) + m.group(2) + f"- {phrase}\n"
        new_content = re.sub(pattern, replacer, content)
        if new_content == content:
            new_content += f"\n- {phrase}\n"
        persona_path.write_text(new_content, encoding="utf-8")
        print(f"✅ 金句已追加: {phrase}")

    # ── 校验 ───────────────────────────────────────────────────────────────────

    def validate(self) -> list[str]:
        """校验三文件的完整性，返回缺失/格式错误的列表"""
        errors = []

        # 1. 目录存在
        if not self.target_dir.exists():
            return [f"目录不存在: {self.target_dir}"]

        # 2. 必要文件存在
        for fname in ("meta.json", "persona.md", "work.md"):
            fpath = self.target_dir / fname
            if not fpath.exists():
                errors.append(f"文件缺失: {fname}")

        # 3. meta.json 必填字段检查
        meta_path = self.target_dir / "meta.json"
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                try:
                    meta = json.load(f)
                except json.JSONDecodeError as e:
                    errors.append(f"meta.json JSON 格式错误: {e}")
                    meta = {}
            required_fields = ["name", "company", "level", "flavor", "intensity"]
            for field in required_fields:
                if field not in meta:
                    errors.append(f"meta.json 缺少必填字段: {field}")

        return errors

    # ── 列出 ───────────────────────────────────────────────────────────────────

    @staticmethod
    def list_leaders() -> list[dict]:
        """列出所有已有的 Leader（排除 _template）"""
        leaders = []
        for d in sorted(LEADERS_DIR.iterdir()):
            if not d.is_dir() or d.name.startswith("_"):
                continue
            meta_path = d / "meta.json"
            entry = {"dir": d.name}
            if meta_path.exists():
                with open(meta_path, encoding="utf-8") as f:
                    try:
                        meta = json.load(f)
                        entry.update({
                            "name": meta.get("name", ""),
                            "slug": meta.get("slug", meta.get("id", "")),
                            "flavor": meta.get("flavor", ""),
                            "version": meta.get("version", "v1.0"),
                        })
                    except json.JSONDecodeError:
                        entry["name"] = "（JSON 损坏）"
            leaders.append(entry)
        return leaders

    # ── 写文件 ─────────────────────────────────────────────────────────────────

    def _write_meta(self, meta: dict) -> None:
        meta_path = self.target_dir / "meta.json"
        # 从模板补全缺失字段（去除注释键 _comment）
        default_meta = self._load_template_meta()
        default_meta.pop("_comment", None)
        merged = {**default_meta, **meta}
        merged.pop("_comment", None)  # 确保注释不写入实际文件
        merged.setdefault("version", "v1.0")
        merged.setdefault("created_at", "")
        merged.setdefault("updated_at", "")
        meta_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_persona(self, persona: dict) -> None:
        """将 persona dict 渲染为 Markdown"""
        persona_path = self.target_dir / "persona.md"
        sections = []

        sections.append(f"# {persona.get('name', '未命名')} 人设文件\n")
        if persona.get("background"):
            sections.append(f"## 背景\n{persona['background']}\n")
        if persona.get("personality"):
            sections.append(f"## 性格特征\n{persona['personality']}\n")
        if persona.get("push_style"):
            sections.append(f"## 施压风格\n{persona['push_style']}\n")
        if persona.get("signature_phrases"):
            phrases = persona["signature_phrases"]
            sections.append("## 金句库\n" + "\n".join(f"- {p}" for p in phrases) + "\n")
        if persona.get("taboo"):
            sections.append(f"## 禁区\n{persona['taboo']}\n")
        if persona.get("raw"):
            sections.append(f"## 原始材料摘录\n{persona.get('raw', '')}\n")

        content = "\n---\n\n".join(sections)
        persona_path.write_text(content, encoding="utf-8")

    def _write_work(self, work: dict) -> None:
        """将 work dict 渲染为 Markdown"""
        work_path = self.target_dir / "work.md"
        sections = []

        sections.append("# 工作风格\n")
        if work.get("meeting_style"):
            sections.append(f"## 会议风格\n{work['meeting_style']}\n")
        if work.get("review_style"):
            sections.append(f"## Review 风格\n{work['review_style']}\n")
        if work.get("feedback_style"):
            sections.append(f"## 反馈风格\n{work['feedback_style']}\n")
        if work.get("decision_style"):
            sections.append(f"## 决策风格\n{work['decision_style']}\n")
        if work.get("escalation"):
            sections.append(f"## 升级策略\n{work['escalation']}\n")

        content = "\n---\n\n".join(sections)
        work_path.write_text(content, encoding="utf-8")

    def _load_template_meta(self) -> dict:
        """加载 _template/meta.json 作为默认值"""
        template_path = self.template_dir / "meta.json"
        if template_path.exists():
            with open(template_path, encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    pass
        return {}

    def _meta_fields(self) -> list[str]:
        return ["id", "slug", "name", "company", "level", "role", "flavor",
                "gender", "years_active", "tags", "push_style", "mbti",
                "signature_phrases", "intensity", "taboo",
                "version", "created_at", "updated_at"]


# ─── CLI 入口 ──────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print("用法: python skill_writer.py <命令> [参数...]")
        print()
        print("命令:")
        print("  list                        列出所有已有的 Leader")
        print("  validate <leader目录名>     校验三文件完整性")
        print("  from-json <leader目录名> <data.json>  从 JSON 文件创建 Leader")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        leaders = SkillWriter.list_leaders()
        if not leaders:
            print("暂无 Leader（leaders/ 目录为空）")
        else:
            print(f"\n共 {len(leaders)} 个 Leader：\n")
            print(f"  {'目录名':<25} {'slug/id':<18} {'姓名':<10} {'Flavor':<12} {'版本'}")
            print("  " + "-" * 75)
            for l in leaders:
                print(f"  {l['dir']:<25} {l.get('slug',''):<18} {l.get('name',''):<10} {l.get('flavor',''):<12} {l.get('version','')}")

    elif command == "validate":
        if len(sys.argv) < 3:
            print("❌ 请指定 Leader 目录名")
            sys.exit(1)
        writer = SkillWriter(sys.argv[2])
        errors = writer.validate()
        if not errors:
            print(f"✅ {sys.argv[2]} 校验通过（三文件完整，必填字段齐全）")
        else:
            print(f"❌ 校验失败（{len(errors)} 个问题）：")
            for e in errors:
                print(f"  - {e}")

    elif command == "from-json":
        if len(sys.argv) < 4:
            print("❌ 请指定 Leader 目录名和 JSON 文件路径")
            sys.exit(1)
        leader_dir = sys.argv[2]
        json_path = Path(sys.argv[3])
        if not json_path.exists():
            print(f"❌ JSON 文件不存在: {json_path}")
            sys.exit(1)
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        writer = SkillWriter(leader_dir)
        writer.create(data)

    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
