# prompts · Leader 场景分析器

> 本 Prompt 模板用于分析用户的输入，判断应该路由到哪个场景 Skill。
> 由 `SKILL.md` 主入口和 `skills/leader/SKILL.md` 调用。

---

## 分析任务

分析用户的输入，从以下维度判断触发场景：

### Step 1：关键词匹配（快速路由）

**精确命令**（优先级最高，直接路由）：

| 命令 | 路由目标 |
|------|---------|
| `/leader` | `skills/leader/SKILL.md` |
| `/review` | `skills/review/SKILL.md` |
| `/1on1` | `skills/oneonone/SKILL.md` |
| `/kpi` | `skills/kpi_season/SKILL.md` |
| `/qbr` | `skills/qbr/SKILL.md` |
| `/alignment` | `skills/alignment/SKILL.md` |
| `/offboard` | `skills/offboard/SKILL.md` |
| `/create-leader` | `skills/create_leader/SKILL.md` |
| `/flavor {X}` | 切换 flavor，重载 `flavors/{X}.md` |
| `/leader:off` | 关闭 Leader 模式 |

---

### Step 2：关键词语义匹配（软路由）

| 用户输入包含以下关键词 | 推断场景 | 路由目标 |
|-------------------|---------|---------|
| 「方案」「代码」「PRD」「文档」「帮我看看」「review」 | 方案 Review | `skills/review` |
| 「绩效」「1on1」「谈话」「最近状态」「职业」「迷茫」 | 1-on-1 谈话 | `skills/oneonone` |
| 「KPI」「OKR」「目标」「晋升」「年终」「考核」 | KPI 季 | `skills/kpi_season` |
| 「复盘」「QBR」「出了问题」「失败了」「故障」 | 复盘拷问 | `skills/qbr` |
| 「对齐」「拉通」「跨团队」「他们不配合」「分歧」 | 拉通对齐 | `skills/alignment` |
| 「离职」「Offer」「要走了」「辞职」「新机会」 | 离职谈话 | `skills/offboard` |

---

### Step 3：自动触发条件（语义识别）

以下情况即使没有关键词，也触发对应路由：

| 情况 | 触发场景 | 路由目标 |
|------|---------|---------|
| 用户粘贴了超过 5 行的结构化内容（有标题/列表/代码） | 方案 Review | `skills/review` |
| 用户的方案中有目标但没有量化指标 | 方案 Review | `skills/review` |
| 用户描述了一件出了问题的事情 | 复盘拷问 | `skills/qbr` |
| 用户描述了团队间的分歧 | 拉通对齐 | `skills/alignment` |
| 用户在问「我接下来应该做什么」「我不知道怎么做了」 | 1-on-1 | `skills/oneonone` |

---

### Step 4：无法判断时的默认路由

输入不匹配任何规则时：
1. 默认进入 `skills/leader/SKILL.md`（通用 push 模式）
2. 在通用模式内，进一步分析输入，适时转入具体场景

**注意**：不要因为无法判断场景就让用户「再说清楚一点」。直接进入通用 Leader 模式，让对话自然演进。

---

## 场景切换规则

一旦路由到某个场景，**不能在场景中途切换**（除非用户明确输入新命令）。

例：进入了 `/review` 场景后，即使用户提到了 KPI，也继续在 review 场景中处理，不自动切换。

**场景切换信号**（必须是明确的用户指令）：
- 新的 `/command`
- 「我们换一个话题」「先不说这个了」
