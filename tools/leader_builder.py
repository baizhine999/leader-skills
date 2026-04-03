#!/usr/bin/env python3
"""
leader_builder.py — Leader 人设自动构建工具

从聊天记录、邮件、会议纪要等原始材料中，
自动提取并生成标准的 Leader 人设三件套：
  - leaders/{id}/meta.json
  - leaders/{id}/persona.md
  - leaders/{id}/work.md

用法：
  python3 leader_builder.py --input <文件或目录> --name <别名> --output <输出目录>
  python3 leader_builder.py --interactive   # 交互式模式

示例：
  python3 leader_builder.py --input ./chat_logs/ --name "老汪" --output ./leaders/
  python3 leader_builder.py --input email.txt --name "CTO老张" --flavor alibaba --output ./leaders/

依赖：
  pip install click rich pathlib
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import click
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None


# ─────────────────────────────────────────────
# 话语特征提取器
# ─────────────────────────────────────────────

class PhraseExtractor:
    """从原始文本中提取 Leader 的标志性句式和话语风格"""

    # 常用大厂话术关键词（用于 flavor 自动识别）
    FLAVOR_SIGNALS = {
        "alibaba": ["拉通", "对齐", "闭环", "底层逻辑", "颗粒度", "owner", "灰度", "数据说话", "p级", "晋升"],
        "bytedance": ["上下同欲", "飞轮效应", "context", "a/b test", "10x", "为什么", "数据驱动", "对齐飞轮"],
        "tencent": ["日活", "月活", "留存", "对标", "用户心智", "小而美", "产品感", "ab测试"],
        "huawei": ["奋斗者", "客户", "交付", "ipd", "ltc", "流程", "作战", "攻坚"],
        "meituan": ["打穿", "认知", "执行", "效率", "打大仗", "供给侧"],
        "xiaomi": ["极致", "性价比", "生态链", "米粉", "口碑", "极致体验"],
        "pinduoduo": ["实干", "少说话", "结果", "月亮", "内耗", "快"],
        "startup": ["窗口期", "赛道", "all in", "pmf", "融资", "mission", "联创"],
    }

    # 疑问句式（Leader 常用的拷问句型）
    QUESTION_PATTERNS = [
        r"你.{0,20}是什么[？?]",
        r"为什么.{0,30}[？?]",
        r"你有没有.{0,20}[？?]",
        r"这件事.{0,20}[？?]",
        r"你.{0,10}怎么.{0,10}[？?]",
        r"底层逻辑.{0,20}[？?]",
        r"你来 owner",
        r"成功指标.{0,20}[？?]",
        r"你觉得.{0,20}[？?]",
    ]

    def extract_phrases(self, text: str) -> list[str]:
        """提取文本中的标志性句子（问句 + 短句）"""
        phrases = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue

            # 提取疑问句
            for pattern in self.QUESTION_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    # 清理格式，只保留核心句子
                    clean = re.sub(r'^[>\-\*\s]+', '', line)
                    clean = re.sub(r'\s+', ' ', clean).strip()
                    if 5 < len(clean) < 80 and clean not in phrases:
                        phrases.append(clean)
                    break

        return phrases[:10]  # 最多返回 10 句

    def detect_flavor(self, text: str) -> str:
        """从文本内容推断 flavor"""
        text_lower = text.lower()
        scores = {}

        for flavor, keywords in self.FLAVOR_SIGNALS.items():
            score = sum(1 for kw in keywords if kw.lower() in text_lower)
            scores[flavor] = score

        if max(scores.values()) == 0:
            return "alibaba"  # 默认

        return max(scores, key=scores.get)

    def detect_mbti(self, text: str) -> str:
        """根据语言风格推断 MBTI（粗略）"""
        # E vs I
        e_score = len(re.findall(r'我们|团队|大家|一起|开会', text))
        i_score = len(re.findall(r'我觉得|我认为|我的判断|独立', text))
        ei = "E" if e_score >= i_score else "I"

        # N vs S
        n_score = len(re.findall(r'未来|方向|愿景|可能性|战略', text))
        s_score = len(re.findall(r'数据|指标|具体|细节|落地', text))
        ns = "N" if n_score >= s_score else "S"

        # T vs F
        t_score = len(re.findall(r'逻辑|分析|标准|效率|结果', text))
        f_score = len(re.findall(r'感受|理解|支持|激励|文化', text))
        tf = "T" if t_score >= f_score else "F"

        # J vs P
        j_score = len(re.findall(r'计划|截止|deadline|时间节点|承诺', text))
        p_score = len(re.findall(r'灵活|调整|看情况|再说|弹性', text))
        jp = "J" if j_score >= p_score else "P"

        return f"{ei}{ns}{tf}{jp}?"  # 加 ? 表示推断


# ─────────────────────────────────────────────
# Leader 人设生成器
# ─────────────────────────────────────────────

class LeaderBuilder:
    """根据收集到的信息生成 Leader 人设三件套"""

    def __init__(self, output_dir: str = "./leaders"):
        self.output_dir = Path(output_dir)
        self.extractor = PhraseExtractor()

    def build_from_intake(
        self,
        name: str,
        company: str,
        level: str,
        relationship: str,
        stories: list[str],
        love_hate: str,
        raw_text: str = "",
        flavor: Optional[str] = None,
    ) -> dict:
        """从 intake 数据构建 Leader 人设"""

        # 自动检测 flavor（如果没指定）
        all_text = " ".join(stories) + " " + love_hate + " " + raw_text
        if not flavor:
            flavor = self.extractor.detect_flavor(all_text)

        # 生成安全 ID
        leader_id = self._make_id(name)

        # 提取话术
        phrases = self.extractor.extract_phrases(all_text)

        # 推断 MBTI
        mbti = self.extractor.detect_mbti(all_text)

        # 判断强度（基于描述中的关键词）
        intensity = self._estimate_intensity(all_text)

        # 判断 push 风格
        push_style = self._detect_push_style(all_text)

        return {
            "id": leader_id,
            "name": name,
            "company": company,
            "level": level,
            "relationship": relationship,
            "flavor": flavor,
            "mbti": mbti,
            "intensity": intensity,
            "push_style": push_style,
            "signature_phrases": phrases,
            "stories": stories,
            "love_hate": love_hate,
            "raw_text": raw_text,
        }

    def _make_id(self, name: str) -> str:
        """生成安全的目录 ID"""
        # 保留字母、数字、中文、下划线
        safe = re.sub(r'[^\w\u4e00-\u9fff]', '_', name)
        safe = re.sub(r'_+', '_', safe).strip('_').lower()
        return safe or "leader_unknown"

    def _estimate_intensity(self, text: str) -> int:
        """估算施压强度 1-5"""
        high_words = ["绩效挂钩", "末位淘汰", "告别谈话", "你不行", "换人", "严厉", "狠", "恐怖"]
        low_words = ["温和", "支持", "鼓励", "包容", "理解", "轻松"]
        
        high_score = sum(1 for w in high_words if w in text)
        low_score = sum(1 for w in low_words if w in text)
        
        base = 3
        result = base + high_score - low_score
        return max(1, min(5, result))

    def _detect_push_style(self, text: str) -> str:
        """检测 push 风格"""
        direct = len(re.findall(r'直接|明确|言|不讲情面|说白了|直白', text))
        indirect = len(re.findall(r'暗示|引导|让你自己|潜移默化', text))
        emotional = len(re.findall(r'激励|情怀|愿景|使命|热血', text))
        expectation = len(re.findall(r'期待|标准|要求|预期|bar', text))

        styles = {
            "直面施压型": direct,
            "迂回引导型": indirect,
            "情绪感召型": emotional,
            "期望管理型": expectation,
        }

        return max(styles, key=styles.get)

    def write_files(self, leader_data: dict) -> Path:
        """写入三件套文件"""
        leader_id = leader_data["id"]
        leader_dir = self.output_dir / leader_id
        leader_dir.mkdir(parents=True, exist_ok=True)

        # 写入 meta.json
        meta = {
            "id": leader_data["id"],
            "name": leader_data["name"],
            "title": f"{leader_data['level']} · {leader_data['company']}",
            "flavor": leader_data["flavor"],
            "mbti": leader_data["mbti"],
            "push_style": leader_data["push_style"],
            "signature_phrases": leader_data["signature_phrases"],
            "intensity": leader_data["intensity"],
            "version": "v1.0",
            "created_by": "leader_builder.py",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        }
        (leader_dir / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        # 写入 persona.md
        persona_content = self._generate_persona_md(leader_data)
        (leader_dir / "persona.md").write_text(persona_content, encoding="utf-8")

        # 写入 work.md
        work_content = self._generate_work_md(leader_data)
        (leader_dir / "work.md").write_text(work_content, encoding="utf-8")

        return leader_dir

    def _generate_persona_md(self, d: dict) -> str:
        phrases_block = "\n".join(f'> 「{p}」' for p in d["signature_phrases"]) or "> （暂无提取到的金句，可手动补充）"

        return f"""# {d['name']} · 人设档案

**姓名（别名）**：{d['name']}  
**职级背景**：{d['level']} · {d['company']}  
**MBTI（推断）**：{d['mbti']}  
**施压强度**：{'⭐' * d['intensity']} ({d['intensity']}/5)  
**Push 风格**：{d['push_style']}  

---

## 角色概述

{d['name']} 是典型的 {d['flavor']} 风格 Leader。
他的核心特质是{d['push_style']}，
在工作中倾向于{self._style_description(d['push_style'])}。

---

## 他的故事

{''.join(f"- {s}{chr(10)}" for s in d['stories']) if d['stories'] else "- （暂无案例，可手动补充）"}

---

## 他的矛盾之处

{d['love_hate'] or '（暂无描述，可手动补充他让你又爱又恨的地方）'}

---

## 他的金句库

{phrases_block}

---

## 他的情绪风格

| 场景 | 反应 |
|------|------|
| 方案有瑕疵 | 冷静发问，不着急发火 |
| 同一问题第三次出现 | 明显语气变重，开始施加组织压力 |
| 遇到真正努力的人 | 表达欣赏，但不一定说出来 |
| 被人耍小聪明 | 直接点破，不给面子 |

> ⚠️ 以上内容为自动生成，请根据实际情况手动修订
"""

    def _generate_work_md(self, d: dict) -> str:
        return f"""# {d['name']} · 工作风格档案

**Flavor**：{d['flavor']}  
**Push 风格**：{d['push_style']}  

---

## 会议风格

- 会前：要求提前发材料（阅读型）/ 直接开讲（行动型）
- 会中：喜欢打断，问「这件事的底层逻辑是什么」
- 会后：必须有明确 Action Item，Owner 和 deadline

---

## Review 风格

1. 先沉默读完，给施压感
2. 从最薄弱的环节入手，问一个尖锐问题
3. 不接受「差不多」、「大概是这样」的答案
4. 最后给出结论：pass / 有条件 pass / 打回重做

---

## 绩效评价观

| 评级 | 他的标准 |
|------|---------|
| 优秀 | 超出预期完成 + 自带方法论 |
| 良好 | 按时完成，有 owner 意识 |
| 一般 | 完成了，但缺乏主动性和深度 |
| 不及预期 | 推一下动一下，没有闭环 |

---

## 1-on-1 套路

1. 「最近在做什么？」（摸底）
2. 「这件事的核心难点在哪里？」（考察认知深度）
3. 「你觉得自己今年的成长是什么？」（绩效铺垫）
4. 给一个 Action Item，下次检查

---

> ⚠️ 以上内容为自动生成，请根据实际情况手动修订
"""

    def _style_description(self, style: str) -> str:
        descriptions = {
            "直面施压型": "直接指出问题，不留情面，以结果为导向",
            "迂回引导型": "通过提问让你自己找到答案，让你感觉是自己想明白的",
            "情绪感召型": "用愿景和使命激励你，让你产生为大目标奋斗的冲动",
            "期望管理型": "通过设定高期望值来驱动你，让你不好意思达不到标准",
        }
        return descriptions.get(style, "因事因人调整施压方式")


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

def interactive_mode():
    """交互式构建模式"""
    print("\n=== Leader 人设构建器（交互模式）===\n")

    name = input("[ Q1 ] 这个 Leader 的别名是？（不需要真名）: ").strip()
    if not name:
        name = "未命名Leader"

    company = input("      他在哪家公司？（阿里/字节/腾讯/华为/美团/其他）: ").strip() or "未知"
    level = input("      他的职级/角色？（如 P10 / VP / CTO / 合伙人）: ").strip() or "高级别"
    relationship = input("      你和他的关系？（直属上司/前上司/偶像）: ").strip() or "上司"

    print("\n[ Q2 ] 讲 3 个他让你印象最深的时刻（每次按 Enter，输入空行结束）:")
    stories = []
    while len(stories) < 5:
        story = input(f"  故事 {len(stories)+1}: ").strip()
        if not story:
            break
        stories.append(story)

    print("\n[ Q3 ] 他有什么让你又爱又恨的地方？他说过什么让你印象深刻的话？")
    love_hate = input("  回答: ").strip()

    print("\n[ 可选 ] 粘贴他说过的原话 / 聊天记录（可多行，输入 END 结束）:")
    raw_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        raw_lines.append(line)
    raw_text = "\n".join(raw_lines)

    output_dir = input("\n[ 输出目录，默认 ./leaders ]: ").strip() or "./leaders"

    # 构建并写入
    builder = LeaderBuilder(output_dir=output_dir)
    leader_data = builder.build_from_intake(
        name=name,
        company=company,
        level=level,
        relationship=relationship,
        stories=stories,
        love_hate=love_hate,
        raw_text=raw_text,
    )
    output_path = builder.write_files(leader_data)

    print(f"\n✅ 人设构建完成！文件已写入：{output_path}")
    print(f"  - {output_path}/meta.json")
    print(f"  - {output_path}/persona.md")
    print(f"  - {output_path}/work.md")
    print(f"\n检测到的 Flavor：{leader_data['flavor']}")
    print(f"推断 MBTI：{leader_data['mbti']}")
    print(f"施压强度：{'⭐' * leader_data['intensity']} ({leader_data['intensity']}/5)")
    if leader_data['signature_phrases']:
        print(f"\n提取到的金句：")
        for p in leader_data['signature_phrases'][:3]:
            print(f"  「{p}」")


def cli_mode(input_path: str, name: str, output_dir: str, flavor: Optional[str] = None):
    """命令行批量构建模式"""
    input_p = Path(input_path)

    # 读取所有文本内容
    raw_text = ""
    if input_p.is_file():
        raw_text = input_p.read_text(encoding="utf-8", errors="ignore")
    elif input_p.is_dir():
        for f in input_p.rglob("*.txt"):
            raw_text += f.read_text(encoding="utf-8", errors="ignore") + "\n"
        for f in input_p.rglob("*.md"):
            raw_text += f.read_text(encoding="utf-8", errors="ignore") + "\n"

    builder = LeaderBuilder(output_dir=output_dir)
    leader_data = builder.build_from_intake(
        name=name,
        company="未知（自动分析）",
        level="未知（自动分析）",
        relationship="上司",
        stories=[],
        love_hate="",
        raw_text=raw_text,
        flavor=flavor,
    )
    output_path = builder.write_files(leader_data)

    print(f"✅ 构建完成 → {output_path}")


# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--interactive" in args or not args:
        interactive_mode()
    elif "--input" in args and "--name" in args:
        try:
            input_path = args[args.index("--input") + 1]
            name = args[args.index("--name") + 1]
            output_dir = args[args.index("--output") + 1] if "--output" in args else "./leaders"
            flavor_arg = args[args.index("--flavor") + 1] if "--flavor" in args else None
            cli_mode(input_path, name, output_dir, flavor_arg)
        except (IndexError, ValueError) as e:
            print(f"参数错误：{e}")
            print("用法：python3 leader_builder.py --input <路径> --name <别名> [--output <目录>] [--flavor <flavor>]")
            sys.exit(1)
    else:
        print("用法：")
        print("  python3 leader_builder.py --interactive")
        print("  python3 leader_builder.py --input <路径> --name <别名> --output <目录>")
        sys.exit(1)
