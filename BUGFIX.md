# Bug Fix Report — v1.0.1

**日期**: 2026-06-01  
**审计范围**: leader-skills 全项目（95 个文件）  
**修复数量**: 10 个 bug，涉及 17 个文件  

---

## 高优先级修复（4 项）

### 1. Shell Hook: JSON `null` → 字符串 `"None"`  
**文件**: `hooks/action_item_tracker.sh`, `hooks/session_restore.sh`  
**严重度**: HIGH  
**问题**: `dict.get('key', '')` 在 JSON 值为 `null` 时返回 Python `None`，`print(None)` 输出字符串 `None`，导致 `[ -n "$VAR" ]` 误判为 true  
**影响**: 无 action item 时会输出 `ACTION_ITEM=None`，下游 parser 误认为存在 action item  
**修复**: 改用 `dict.get('key') or ''`

### 2. sanitize-session.sh: 硬编码路径 + 缺少错误保护  
**文件**: `hooks/sanitize-session.sh`  
**严重度**: HIGH  
**问题 A**: 嵌入式 Python 硬编码 `~/.leader/pending_corrections.json` 和 `~/.leader/config.json`，忽略脚本顶部 shell 变量  
**问题 B**: `set -euo pipefail` 下 Python heredoc 无 `|| true` 保护，config.json 损坏时整个清理脚本退出，后续清理不执行  
**修复**: 通过环境变量传入路径，添加 `|| true` 容错

### 3. codex/ 目录下 8 个 SKILL.md 标错平台  
**文件**: `codex/*/SKILL.md`（全部 8 个）  
**严重度**: HIGH  
**问题**: 标题全部写 `（CodeBuddy 版）`，目录名是 `codex/`  
**修复**: 全局替换为 `（Codex 版）`

### 4. README.en.md / README.ja.md 损坏的外部链接  
**文件**: `README.en.md`, `README.ja.md`  
**严重度**: HIGH  
**问题**: `[https://github.com/tanweai/pua](../参考/pua-main)` 指向不存在的相对路径  
**修复**: 改为直接 URL

---

## 中优先级修复（2 项）

### 5. cursor/rules/leader.mdc: 错误的关闭命令  
**文件**: `cursor/rules/leader.mdc`  
**问题**: 关闭命令写 `/off`，项目统一用 `/leader:off`  
**修复**: 2 处修正

### 6. SKILL.md: 缺少触发关键词  
**文件**: `SKILL.md`  
**问题**: metadata description 遗漏 `/alignment`、`/offboard` 关键词  
**修复**: 补全

---

## 低优先级修复（4 项）

### 7. leader_builder.py: 正则关键词过于宽泛  
**文件**: `tools/leader_builder.py`  
**问题**: 单个 `言` 字命中 `语言`、`发言` 等无关词，系统性误判 push 风格分类  
**修复**: `言` → `直言不讳`

### 8. leader_builder.py: 死导入清理  
**文件**: `tools/leader_builder.py`  
**问题**: `rich.console.Console`、`rich.panel.Panel`、`rich.prompt.Prompt/Confirm`、`rich.table.Table` 导入后从未使用  
**修复**: 移除未使用的 rich 子模块导入

### 9. feishu_parser.py: 未使用的 import  
**文件**: `tools/feishu_parser.py`  
**问题**: `from typing import Optional` 未在任何类型注解中使用  
**修复**: 移除

### 10. README.ja.md: 新增日文 README  
**文件**: `README.ja.md`（新增）  
**说明**: 基于英文版全文翻译为日文，3 语言 README 相互链接

---

## 版本管理

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0.0 | 2026-04-03 | 初始发布 |
| v1.0.1 | 2026-06-01 | Bug 修复：10 个 bug fix |

---

## 已知未修复（低优先级）

- `hooks/hooks.json` 的 `conversation_end` 触发器兼容性待验证
- `_template/meta.json` 的 `_comment` 字段在遍历 keys 时可能被误读
- `landing.html` Clipboard API 在 `file://` 协议下无 fallback
- `ARCHITECTURE.md` Roadmap 复选框未更新
- `references/display-protocol.md` 引用不存在的 `~/.leader/session.json`
