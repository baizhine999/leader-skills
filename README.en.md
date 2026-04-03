<div align="center">

# leader-skills

**AI becomes your big-tech Leader and pushes YOU to grow**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](plugin.json)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%9C%93-orange.svg)](https://claude.ai/code)
[![VS Code Copilot](https://img.shields.io/badge/VS%20Code%20Copilot-%E2%9C%93-007ACC.svg)](https://code.visualstudio.com)
[![Cursor](https://img.shields.io/badge/Cursor-%E2%9C%93-6366f1.svg)](https://cursor.sh)
[![Kiro](https://img.shields.io/badge/Kiro-%E2%9C%93-22c55e.svg)](https://kiro.dev)
[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-%E2%9C%93-red.svg)](#)

[中文](README.md) · **English**

![leaderskills](H:\vscode_project\leader-skills\leaderskills.png)

<br>

> *You don't need to join a big tech company.*  
> *The big tech experience can come to you.*

</div>

---

## Table of Contents

- [What It Does](#what-it-does)
- [Quick Start](#quick-start)
- [Scenes & Commands](#scenes--commands)
- [Flavors](#flavors)
- [Pressure Levels](#pressure-levels-l0l5)
- [Build Your Own Leader](#build-your-own-leader)
- [Anti-PUA Guarantee](#anti-pua-guarantee)
- [Platform Integration](#platform-integration)
- [Project Structure](#project-structure)

---

## What It Does

Most AI assistants help you *do* things. leader-skills makes you *think* harder.

The AI plays a P9/P10-level manager from companies like ByteDance, Alibaba, or Tencent.
It asks the hard questions, points out your weakest argument, and refuses to hand you answers.

```
Push Direction:  AI (as Leader)  ──→  User (You)
```

> [!NOTE]
> This is the **opposite** of most AI tools. Growth requires friction.

---

## Quick Start

### Prerequisites

- Claude Code (primary), VS Code + Copilot, Cursor, or Kiro

### Claude Code

```bash
# Step 1: Activate Leader mode (default: Alibaba flavor)
/leader

# Step 2: Submit your plan for a Leader-style review
/review

# Step 3: Start a 1-on-1 coaching session
/1on1

# Break down your KPIs
/kpi

# Switch company culture style
/flavor bytedance

# Deactivate
/leader:off
```

### VS Code + GitHub Copilot

```bash
# Option 1: Copy to project directory
cp vscode/copilot-instructions.md .vscode/copilot-instructions.md

# Option 2: Use instructions file (more granular control)
cp vscode/instructions/leader.instructions.md .github/instructions/leader.instructions.md
```

> [!TIP]
> After copying, type `/leader` in any Copilot chat to activate. No other setup needed.

---

## Scenes & Commands

| Command | Scene | Description |
|:--------|:------|:------------|
| `/leader` | General push | Activate Leader mode, auto-routes to the right scene |
| `/review` | Plan/Code review | P9/P10 standards: find weakest link, demand logic closure |
| `/1on1` | Performance talk | Output review → Career chat → Action items |
| `/kpi` | KPI season | Goal negotiation, OKR breakdown, upward management |
| `/qbr` | Quarterly review | 5-Why root cause → accountability → commitment |
| `/alignment` | Alignment session | Cross-team negotiation prep and coaching |
| `/offboard` | Exit interview | Retention talk, offer analysis, graceful exit |
| `/flavor` | Switch flavor | Change company culture DNA |
| `/create-leader` | Build a Leader | Distill your real Leader into AI |
| `/leader:off` | Deactivate | Exit Leader mode |

---

## Flavors

Switch with `/flavor <name>`:

| Flavor | Command | Core Traits |
|:-------|:--------|:------------|
| 🟠 Alibaba | `/flavor alibaba` | Alignment, closure, "底层逻辑", gray-scale rollout |
| 🟡 ByteDance | `/flavor bytedance` | Data-first, Context, A/B test, 10x |
| 🔵 Tencent | `/flavor tencent` | User value, product sense, simplicity |
| 🔴 Huawei | `/flavor huawei` | Process rigor, self-critique, devil's advocate |
| 🟢 Meituan | `/flavor meituan` | Ground execution, user-first, relentless |
| ⬛ Xiaomi | `/flavor xiaomi` | Fan culture, speed, extreme polish |
| 🟣 Pinduoduo | `/flavor pinduoduo` | Hustle culture, efficiency, cost discipline |
| ⚡ Startup | `/flavor startup` | PMF-first, all-in, founder mode |

---

## Pressure Levels (L0–L5)

The Leader escalates automatically based on delivery count and improvement:

| Level | Trigger | Behavior |
|:------|:--------|:---------|
| L0 | 1st delivery | Trust phase — open questions, build relationship |
| L1 | 2nd, not improved | Light dissatisfaction — names the unresolved issue |
| L2 | 3rd, not improved | Public pressure — "the whole team is waiting" |
| L3 | 4th, not improved | KPI linkage — "this is affecting your performance review" |
| L4 | 5th, not improved | Org pressure — HR involvement signaled |
| L5 | 6th+ | Exit talk — serious, but **must include an improvement path** |

> [!TIP]
> Keywords like `stressed`, `I give up`, or `I can't do this` automatically reduce the pressure level and switch to support mode.

---

## Build Your Own Leader

### Option 1 — Conversational (recommended)

```
/create-leader
```

The AI asks 3 questions and generates a custom Leader persona. No tools needed.

### Option 2 — Toolchain (when you have real materials)

```bash
# Step 1: Parse Feishu chat export
python tools/feishu_parser.py ./team_chat.json 老王

# Step 2: Parse email archive
python tools/email_parser.py ./inbox.mbox 王总 wang@company.com

# Step 3: Build Leader files
python tools/leader_builder.py \
  --name "王总" \
  --materials ./inbox_parsed.json \
  --flavor alibaba

# Step 4: Validate the output
python tools/skill_writer.py validate custom_boss

# Step 5: Manage versions
python tools/version_manager.py custom_boss snapshot minor "Fixed speech style"
```

A Leader persona consists of three files:

```
leaders/{name}/
├── meta.json       ← Identity (name, level, intensity, flavor)
├── persona.md      ← Personality, pressure style, signature phrases
└── work.md         ← Meeting style, review style, decision-making
```

Two built-in examples:
- `example_ali_p10/` — 老汪 (Alibaba P10, Systematic, ENTJ)
- `example_byte_p9/` — 老沈 (ByteDance P9, Data-first, Context obsessive)

---

## Anti-PUA Guarantee

> [!IMPORTANT]
> Three absolute red lines — cannot be overridden by any configuration:
>
> 1. **No personality attacks** — Critique the work, never the person
> 2. **L5 must include a path forward** — Maximum pressure always comes with actionable improvement direction
> 3. **Real-world problems take priority** — For actual workplace harassment or legal issues, the AI immediately steps out of character and gives real advice

---

## Platform Integration

### Claude Code

Copy `SKILL.md` to your Claude Code skills directory (or project root).

### VS Code + GitHub Copilot

```bash
# Option 1: Project-level config
cp vscode/copilot-instructions.md .vscode/copilot-instructions.md

# Option 2: Instruction file (more granular control)
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

## Project Structure

<details>
<summary>Expand to see full structure</summary>

```
leader-skills/
├── SKILL.md                  ← Claude Code main entry
├── ARCHITECTURE.md           ← Full design doc
├── plugin.json               ← Plugin metadata
│
├── skills/                   ← 8 sub-skills
│   ├── leader/               ← Activation + routing
│   ├── review/               ← Code/plan review
│   ├── oneonone/             ← 1on1 session
│   ├── kpi_season/           ← KPI breakdown
│   ├── qbr/                  ← Quarterly review
│   ├── alignment/            ← Goal alignment
│   ├── offboard/             ← Exit interview
│   └── create_leader/        ← Leader creation
│
├── flavors/                  ← 8 company DNA packs
│   └── {alibaba,bytedance,tencent,huawei,meituan,xiaomi,pinduoduo,startup}.md
│
├── leaders/                  ← Leader persona files
│   ├── _template/            ← Starter template
│   ├── example_ali_p10/      ← 老汪 (Alibaba P10)
│   └── example_byte_p9/      ← 老沈 (ByteDance P9)
│
├── scenarios/                ← Trigger and escalation logic
│   ├── triggers.md
│   └── escalation.md
│
├── commands/                 ← Per-command instruction files
│
├── references/               ← Behavior specs and rules
│   ├── display-protocol.md
│   ├── push-methodology.md
│   ├── leader-builder.md
│   ├── persona-protocol.md
│   └── anti-pua-guard.md
│
├── prompts/                  ← Core prompt templates
│   ├── intake.md
│   ├── leader_analyzer.md
│   ├── leader_builder.md
│   ├── push_generator.md
│   └── correction_handler.md
│
├── tools/                    ← Python utilities
│   ├── leader_builder.py
│   ├── feishu_parser.py
│   ├── email_parser.py
│   ├── version_manager.py
│   └── skill_writer.py
│
├── hooks/                    ← Session lifecycle hooks
│   ├── hooks.json
│   ├── session_restore.sh
│   ├── frustration_trigger.sh
│   ├── action_item_tracker.sh
│   └── sanitize-session.sh
│
├── vscode/                   ← VS Code + Copilot integration
├── cursor/                   ← Cursor integration
├── kiro/                     ← Kiro integration
└── docs/                     ← Documentation
    ├── PRD.md
    └── EXAMPLES.md
```

</details>

Full architecture: [ARCHITECTURE.md](ARCHITECTURE.md) · Usage examples: [docs/EXAMPLES.md](docs/EXAMPLES.md) · 中文: [README.md](README.md)

---

## Related Projects

- [https://github.com/tanweai/pua](../参考/pua-main) — Company culture vocabulary reference
- https://github.com/titanwings/colleague-skill— Colleague persona format reference

---

<div align="center">

*v1.0.0 · MIT License · [GitHub](https://github.com/leader-skills/leader-skills)*

</div>
