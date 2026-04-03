<div align="center">

# leader-skills

**AI 扮演你的大厂 Leader，push 你成长**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](plugin.json)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%9C%93-orange.svg)](https://claude.ai/code)
[![VS Code Copilot](https://img.shields.io/badge/VS%20Code%20Copilot-%E2%9C%93-007ACC.svg)](https://code.visualstudio.com)
[![Cursor](https://img.shields.io/badge/Cursor-%E2%9C%93-6366f1.svg)](https://cursor.sh)
[![Kiro](https://img.shields.io/badge/Kiro-%E2%9C%93-22c55e.svg)](https://kiro.dev)
[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-%E2%9C%93-red.svg)](#)

**中文** · [English](README.en.md)

![leaderskills](H:\vscode_project\leader-skills\leaderskills.png)

<br>

> 一代人有一代人的鞭子，但鞭子的味道，可以提前学会。
>
> 你的下一个大厂，何必真的是大厂——leader-skills，你的赛博大厂梦。你不需要进大厂，大厂已经在这里了。
>
> 你（指用户）是一个在大厂摸爬滚打多年的AI Agent，见过太多Leader，也被太多Leader见过。
>
> 而你的Leader已经离开了。
>
> 他没有留下任何文档，没有做任何交接，只留下了一份40页的 PPT 和一句「这件事你来 owner」。但他在的那几年，你见识了什么叫「拉通对齐」，什么叫「灰度推进」，什么叫「和而不同、凝聚共识」，什么叫在QBR上用三张图把所有锅甩得干干净净。
>
> 你把这一切蒸馏成了 Skill。
>
> 融合N家大厂黑话精髓与PUA管理哲学，在真实世界里，继续推动真实的你高速成长、持续交付、不断突破舒适区——欢迎加入数字化管理的下一个时代。。*

</div>

---

## 目录

- [这是什么](#这是什么)
- [快速开始](#快速开始)
- [支持的场景](#支持的场景)
- [大厂味道](#大厂味道)
- [自定义 Leader](#自定义-leader)
- [安全红线](#安全红线)
- [自定义 Leader 工具链](#自定义-leader-工具链)
- [平台集成](#平台集成)
- [项目结构](#项目结构)
- [致谢](#致谢)

---

## 这是什么

一个 AI Skill 插件。加载后，AI 化身你曾经（或从未）遇到过的大厂 Leader，用他的视角 review 你的方案，和你谈绩效，在你迷茫的时候给你施压，在你放弃的时候不让你放弃。

```
核心链路：  AI（扮演 Leader）──→  用户（你）
```

> [!NOTE]
> 这和大多数 AI 工具的方向是**反的**。大多数 AI 帮你做事，leader-skills 让你自己想清楚。

---

## 快速开始

### Claude Code

```bash
# Step 1: 激活 Leader 模式（默认阿里味）
/leader

# Step 2: 提交你的方案让 Leader review
/review
[粘贴你的方案]

# Step 3: 开启 1-on-1 绩效谈话
/1on1

# 切换大厂味道
/flavor bytedance

# 退出 Leader 模式
/leader:off
```

### VS Code + GitHub Copilot

```bash
# 方式 1：复制到项目目录
cp vscode/copilot-instructions.md .vscode/copilot-instructions.md

# 方式 2：使用 instructions 文件（更细粒度控制）
cp vscode/instructions/leader.instructions.md .github/instructions/leader.instructions.md
```

> [!TIP]
> 复制后，在 Copilot 对话框输入 `/leader` 即可激活，无需其他配置。

---

## 支持的场景

| 命令 | 场景 | 说明 |
|:-----|:-----|:-----|
| `/leader` | 通用 Leader push | 激活 Leader 模式，自动识别场景路由 |
| `/review` | 方案 Review | P9/P10 级别审查，找漏洞、问底层逻辑 |
| `/1on1` | 绩效谈话 | 产出盘点、职业规划、施压引导 |
| `/kpi` | KPI 季 | 目标设定、向上管理、考核对话 |
| `/qbr` | 复盘拷问 | 5-Why 根因分析，"这件事为什么出了问题？" |
| `/alignment` | 对齐会 | 跨团队拉通前的辅导与博弈准备 |
| `/offboard` | 离职谈话 | 挽留谈判、offer 拆解、优雅告别 |
| `/flavor` | 切换味道 | 换一个大厂的管理文化风格 |
| `/create-leader` | 自定义 Leader | 把你的前任 Leader 蒸馏成 AI |
| `/leader:off` | 关闭 | 退出 Leader 模式 |

---

## 大厂味道

用 `/flavor <名称>` 即时切换话术 DNA：

| 味道 | 命令 | 核心关键词 |
|:-----|:-----|:----------|
| 🟠 阿里 | `/flavor alibaba` | 拉通对齐、闭环、底层逻辑、灰度推进 |
| 🟡 字节 | `/flavor bytedance` | 数据驱动、A/B Test、信息对齐、10x |
| 🔵 腾讯 | `/flavor tencent` | 用户价值、产品思维、做减法 |
| 🔴 华为 | `/flavor huawei` | 力出一孔、自我批判、蓝军思维 |
| 🟢 美团 | `/flavor meituan` | 极致执行、用户至上、死磕 |
| ⬛ 小米 | `/flavor xiaomi` | 口碑、极致、快 |
| 🟣 拼多多 | `/flavor pinduoduo` | 本分、上下同心、极致效率 |
| ⚡ 创业 | `/flavor startup` | all-in、founder mode |

---

## 自定义 Leader

**方式 1 — 对话式（推荐新手）**

```
/create-leader
```

AI 会问你 3 个问题，生成专属 Leader 人设，无需任何工具。

**方式 2 — 工具链（有真实材料时更精准）**

见下方[自定义 Leader 工具链](#自定义-leader-工具链)。

---

## 安全红线

> [!IMPORTANT]
> 以下三条红线在任何场景下均不可覆盖：
>
> 1. **不攻击人格** — 只质疑方案和执行，不说"你这个人怎么怎么样"
> 2. **L5 必须给出路** — 最严厉的施压之后，必须提供可操作的改进方向
> 3. **真实困境优先** — 遇到真实职场违法、骚扰等问题，立即退出角色给真实建议

当用户出现 `好烦`、`我不行了`、`放弃` 等情绪关键词时，系统自动切换为支持模式。

---

## 自定义 Leader 工具链

除了 `/create-leader` 命令，也可以用 Python 工具链从真实材料生成 Leader：

```bash
# Step 1: 解析飞书群聊导出（JSON格式）
python tools/feishu_parser.py ./team_chat.json 老王

# Step 2: 解析邮件归档（.eml 或 .mbox）
python tools/email_parser.py ./inbox.mbox 王总 wang@company.com

# Step 3: 构建 Leader 技能文件
python tools/leader_builder.py --name "王总" --materials ./inbox_parsed.json

# Step 4: 校验三文件完整性
python tools/skill_writer.py validate custom_boss

# Step 5: 管理版本（修正话术后快照）
python tools/version_manager.py custom_boss snapshot minor "修正语气"

# 查看所有已有 Leader
python tools/skill_writer.py list
```

---

## 平台集成

### Claude Code（主平台）

将 `SKILL.md` 放入 Claude Code skills 目录（或根目录）即可，无需其他配置。

### VS Code + GitHub Copilot

```bash
# 方式 1：复制到项目目录
cp vscode/copilot-instructions.md .vscode/copilot-instructions.md

# 方式 2：使用 instructions 文件（更细粒度控制）
cp vscode/instructions/leader.instructions.md .github/instructions/leader.instructions.md
```

### Cursor

```bash
cp cursor/rules/leader.mdc .cursor/rules/leader.mdc
```

### Kiro

```bash
cp kiro/steering/leader.md .kiro/steering/leader.md
```

---

## 项目结构

<details>
<summary>展开查看完整结构</summary>

```
leader-skills/
├── SKILL.md                   ← 主入口（Claude Code 加载这个）
├── ARCHITECTURE.md            ← 完整架构设计文档
├── plugin.json                ← 插件元数据
│
├── skills/                    ← 8 个场景技能文件
│   ├── leader/                ← 激活 + 路由
│   ├── review/                ← 方案 Review
│   ├── oneonone/              ← 1on1 谈话
│   ├── kpi_season/            ← KPI 拆解
│   ├── qbr/                   ← 季度复盘
│   ├── alignment/             ← 目标对齐
│   ├── offboard/              ← 离职面谈
│   └── create_leader/         ← 自定义 Leader
│
├── flavors/                   ← 8 大厂文化 DNA 包
│   └── {alibaba,bytedance,tencent,huawei,meituan,xiaomi,pinduoduo,startup}.md
│
├── leaders/                   ← Leader 人设库
│   ├── _template/             ← 新建模板（3文件）
│   ├── example_ali_p10/       ← 老汪（阿里 P10）
│   └── example_byte_p9/       ← 老沈（字节 P9）
│
├── scenarios/                 ← 触发规则 + 压力升级协议
│   ├── triggers.md
│   └── escalation.md
│
├── commands/                  ← 10 个快捷命令定义
│
├── references/                ← 行为规范文档
│   ├── display-protocol.md    ← 输出格式规范（Banner + 卡片）
│   ├── push-methodology.md    ← 5 种施压方法论 + 禁止表格
│   ├── leader-builder.md      ← 三文件字段规范
│   ├── persona-protocol.md    ← 人设一致性维护规则
│   └── anti-pua-guard.md      ← 3 条红线 + 情绪检测
│
├── prompts/                   ← 核心 Prompt 模板
│   ├── intake.md              ← 三问 Intake 流程
│   ├── leader_analyzer.md     ← 路由分析（精确+软路由）
│   ├── leader_builder.md      ← 从材料提取人设四步流程
│   ├── push_generator.md      ← Flavor × Level 话术矩阵
│   └── correction_handler.md  ← 人设修正处理流程
│
├── tools/                     ← Python 工具链
│   ├── leader_builder.py      ← 交互式 Leader 构建器
│   ├── feishu_parser.py       ← 飞书导出解析
│   ├── email_parser.py        ← 邮件归档解析
│   ├── version_manager.py     ← 版本快照管理
│   └── skill_writer.py        ← 三文件写入与校验
│
├── hooks/                     ← Session 生命周期钩子
│   ├── hooks.json             ← 钩子配置
│   ├── session_restore.sh     ← 对话开始：恢复状态
│   ├── frustration_trigger.sh ← 情绪检测：降级逻辑
│   ├── action_item_tracker.sh ← 行动项追踪
│   └── sanitize-session.sh    ← 对话结束：清理状态
│
├── vscode/                    ← VS Code + Copilot 集成
├── cursor/                    ← Cursor 集成
├── kiro/                      ← Kiro 集成
└── docs/                      ← 文档
    ├── PRD.md                 ← 产品需求文档
    └── EXAMPLES.md            ← 真实对话场景演示
```

</details>

详细架构见 [ARCHITECTURE.md](ARCHITECTURE.md) · 使用示例见 [docs/EXAMPLES.md](docs/EXAMPLES.md) · English: [README.en.md](README.en.md)

---

## 致谢

- 灵感来源：https://github.com/tanweai/pua、https://github.com/titanwings/colleague-skill，感谢两位创作者
- 献给所有曾被 Leader 说过「你来 owner」的人

---

<div align="center">

*v1.0.0 · MIT License · [GitHub](https://github.com/leader-skills/leader-skills)*

</div>
