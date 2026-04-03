# leader-skills · 项目架构设计文档

> 一代人有一代人的鞭子，但鞭子的味道，可以提前学会。  
> 你的下一个大厂，何必真的是大厂——leader-skills，你的赛博大厂梦。

---

## 一、项目定位

| | pua-main | colleague-skill-main | **leader-skills** |
|--|----------|----------------------|-------------------|
| **Push 方向** ⭐ | 用户触发 → AI 自我施压 | 无施压（双向协作） | **AI（扮演 Leader）→ 用户** |
| **Push 对象** | AI 自身 | 无（协作关系，非施压） | **用户（你）** |
| **AI 扮演角色** | 无固定人设（成为被大厂文化驱动的 P8，自我 PUA） | 某位具体同事 | **某位具体 Leader** |
| **核心价值** | 让 AI 穷尽所有方案才能放弃 | 随时召唤已离职同事的经验与视角 | **AI 化身 Leader，push 你成长** |
| **触发场景** | AI 重复失败、偷懒、要放弃 | 需要同事视角协作或决策参考 | 你迷茫、方案有漏洞、职业困境 |
| **核心输出** | 迫使 AI 自我交付 | 同事人设还原 + 协作建议 | **Leader 视角 review / push / 带路** |

> ⭐ **核心**：leader-skills 的 push 链路是「**AI（扮演 Leader）→ 用户**」，AI 是施压者，用户是被成长的那个人。  
> pua-main 反过来：用户是触发者，AI 是自我施压的对象。

### 差异化定位

```
pua-main      → 用户 push AI（让 Agent 不偷懒）
colleague     → AI 扮演同事（召唤协作者）
leader-skills → AI 扮演 Leader，push 用户（你）
               = Leader 人设 × 大厂方法论 × 场景化鞭策用户
```

---

## 二、目录结构

```
leader-skills/
│
├── ARCHITECTURE.md             ← 本文档
├── README.md                   ← 项目介绍（中文）
├── README.en.md                ← 英文版
├── plugin.json                 ← Claude Code / Codex 插件描述
├── SKILL.md                    ← 主入口 Skill（路由分发）
│
├── leaders/                    ← Leader 人设库（核心数据层）
│   ├── _template/              ← 新建 Leader 的模板
│   │   ├── meta.json
│   │   ├── persona.md
│   │   └── work.md
│   ├── example_ali_p10/        ← 阿里系 P10 示例
│   │   ├── meta.json
│   │   ├── persona.md
│   │   └── work.md
│   └── example_byte_p9/        ← 字节系 P9 示例
│       ├── meta.json
│       ├── persona.md
│       └── work.md
│
├── skills/                     ← 场景 Skill 文件
│   ├── leader/
│   │   └── SKILL.md            ← /leader 主技能（通用 push 路由）
│   ├── oneonone/
│   │   └── SKILL.md            ← /1on1 绩效谈话 / 职业对话
│   ├── review/
│   │   └── SKILL.md            ← /review 方案 & 代码 Review
│   ├── alignment/
│   │   └── SKILL.md            ← /alignment 拉通对齐会
│   ├── kpi_season/
│   │   └── SKILL.md            ← /kpi KPI 季：目标、OKR、向上管理
│   ├── qbr/
│   │   └── SKILL.md            ← /qbr 复盘拷问模式
│   ├── offboard/
│   │   └── SKILL.md            ← /offboard 离职谈话（告别与传承）
│   └── create_leader/
│       └── SKILL.md            ← /create-leader 新建 Leader 人设
│
├── flavors/                    ← 大厂味道库（话术 DNA）
│   ├── alibaba.md              ← 阿里味：拉通/对齐/灰度/闭环
│   ├── bytedance.md            ← 字节味：数据驱动/对齐/上下同欲
│   ├── tencent.md              ← 鹅厂味：用户价值/产品思维/做减法
│   ├── huawei.md               ← 华为味：力出一孔/自我批判/蓝军
│   ├── meituan.md              ← 美团味：极致执行/用户至上/死磕
│   ├── xiaomi.md               ← 小米味：口碑/极致/快/为发烧而生
│   ├── pinduoduo.md            ← 拼多多味：本分/极致/上下同心
│   └── startup.md              ← 创业味：all-in/赌国运/founder mode
│
├── scenarios/                  ← 场景路由与压力升级
│   ├── triggers.md             ← 触发条件规则表（关键词 + 语义识别）
│   └── escalation.md          ← 压力升级路径 L0～L5
│
├── references/                 ← 协议细节（供 Skill 内部引用）
│   ├── display-protocol.md     ← Leader 输出格式（Banner / Review 卡 / KPI 卡）
│   ├── push-methodology.md     ← Push 方法论（如何鞭策用户而非骂街）
│   ├── leader-builder.md       ← 从原材料构建 Leader 人设的详细协议
│   ├── persona-protocol.md     ← 人设一致性维护规则
│   └── anti-pua-guard.md       ← 安全边界：不允许的行为清单
│
├── prompts/                    ← 内部 Prompt 模板
│   ├── intake.md               ← 3 问采集 Leader 信息
│   ├── leader_analyzer.md      ← 分析用户输入 → 判断触发哪个场景
│   ├── leader_builder.md       ← 从聊天/邮件构建 Leader persona
│   ├── push_generator.md       ← 生成 Push 话术（带味道参数）
│   └── correction_handler.md  ← "他不应该这样说" → 修正人设
│
├── commands/                   ← 快捷命令入口
│   ├── leader.md               ← /leader — 激活当前 Leader push 模式
│   ├── 1on1.md                 ← /1on1 — 启动 1-on-1 绩效谈话
│   ├── review.md               ← /review — Review 我的方案 / 代码
│   ├── alignment.md            ← /alignment — 对齐会模式
│   ├── kpi.md                  ← /kpi — KPI 季模式
│   ├── qbr.md                  ← /qbr — 复盘拷问模式
│   ├── offboard.md             ← /offboard — 离职谈话模式
│   ├── flavor.md               ← /flavor — 切换大厂味道
│   ├── create-leader.md        ← /create-leader — 新建 Leader 人设
│   └── off.md                  ← /leader:off — 关闭 Leader 模式
│
├── tools/                      ← 辅助自动化脚本
│   ├── leader_builder.py       ← 从聊天记录 / 邮件 / 飞书构建 Leader Skill
│   ├── feishu_parser.py        ← 解析飞书导出（复用 colleague-skill）
│   ├── email_parser.py         ← 解析 .eml / .mbox 邮件
│   ├── version_manager.py      ← Leader Skill 版本管理
│   └── skill_writer.py         ← 写入 / 列出 Leader Skill 文件
│
├── hooks/                      ← 自动化钩子
│   ├── hooks.json              ← 钩子配置（PreToolUse / SessionStart）
│   ├── session_restore.sh      ← 会话恢复：加载上次 Leader 状态 + 压力等级
│   ├── frustration_trigger.sh ← 检测用户消极情绪 → 自动触发 Leader push
│   ├── action_item_tracker.sh ← 追踪上次 Action Item 完成情况
│   └── sanitize-session.sh    ← 会话结束清理
│
├── vscode/                     ← VSCode GitHub Copilot 集成
│   ├── copilot-instructions.md ← 全局 instructions
│   └── instructions/
│       └── leader.instructions.md
│
├── cursor/                     ← Cursor 集成
│   └── rules/
│       └── leader.mdc
│
├── kiro/                       ← Kiro 集成
│   └── steering/
│       └── leader.md
│
└── docs/
    ├── PRD.md                  ← 产品需求文档
    └── EXAMPLES.md             ← 真实使用案例展示
```

---

## 三、三层能力模型

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 3：人设层 (Persona Layer)                             │
│                                                              │
│  Leader 是谁？怎么说话？习惯性话术是什么？                   │
│  遇到方案漏洞他会怎么反应？他的口头禅是？                    │
│                                                              │
│  → leaders/   存储具体人设（可定制）                        │
│  → flavors/   存储大厂文化 DNA（通用味道）                  │
├──────────────────────────────────────────────────────────────┤
│  Layer 2：场景层 (Scenario Layer)                            │
│                                                              │
│  用户在做什么？该触发哪个场景？压力应该升到几级？            │
│  是 1-on-1 谈话、方案 Review，还是 KPI 季的向上管理？        │
│                                                              │
│  → scenarios/  触发规则 + 压力升级路径                      │
│  → skills/     各场景的具体 Skill 文件                     │
├──────────────────────────────────────────────────────────────┤
│  Layer 1：行为层 (Behavior Layer)                            │
│                                                              │
│  用什么方法论 push 用户？                                    │
│  怎么鞭策而不是骂街？边界在哪里？                            │
│                                                              │
│  → references/ Push 方法论 + 安全边界协议                  │
│  → prompts/    Push 话术生成模板                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 四、核心数据结构

### 4.1 Leader 人设文件

**`leaders/{slug}/meta.json`**

```json
{
  "slug": "ali_p10_laowang",
  "name": "老汪",
  "company": "阿里巴巴",
  "level": "P10",
  "role": "技术副总裁",
  "flavor": "alibaba",
  "gender": "male",
  "years_active": "2018-2023",
  "tags": ["甩锅高手", "PPT 大师", "拉通专家", "好大喜功"],
  "created_at": "2026-04-02",
  "version": "1.0.0"
}
```

**`leaders/{slug}/persona.md`**

```markdown
## 人格画像

- MBTI：ENTJ
- 口头禅：「这件事你来 owner」「先对齐一下」「这个灰度推进」
- 情绪模式：表面温和，QBR 时突然翻脸，善用"我只是问个问题"开场
- 惯用 PUA 手法：
  - 在大群里单点你「XX 这个你跟进一下进展」
  - 方案 review 时沉默 3 秒然后说「你再想想」
  - KPI 季说「我觉得你今年可以冲一冲」（意味着不冲就 3.25）
- 开会风格：前 20 分钟讲背景（自己都讲过 N 遍的），剩下时间问为什么不行
```

**`leaders/{slug}/work.md`**

```markdown
## 工作风格

### 决策模式
先发散再收敛，但收敛的节点永远是他拍板。喜欢「听大家的意见」然后做和意见相反的决定。

### 带人方式
- 给目标不给方法：「这个季度你要把 DAU 翻倍，怎么做你来定」
- 容错边界模糊：出了问题说「我以为你知道这个要 double check」
- 表扬公开批评私下（但批评也是公开的）

### Review 习惯  
第一个问题必定是：「你这个方案的底层逻辑是什么？」
无论你答什么，第二个问题都是：「有没有更好的方案？」

### 开会口语包
- 「先拉通一下」
- 「这个不是方向问题，是执行力问题」
- 「我们不要纠结细节，先把框架对齐」
- 「这件事需要有人来 owner」
```

---

### 4.2 压力升级协议

```
L0 信任期     → 首次交付：Leader 表示期待，正向建立信任
L1 轻微不满   → 方案有明显漏洞：「你再想想？」「这个颗粒度不够」
L2 公开施压   → 第 2 次问题：在群里 @ 你，要求当天同步
L3 绩效挂钩   → 第 3 次：「这件事会影响你的 KPI 的」
L4 组织施压   → 第 4 次：「我需要跟 HR 同步一下你的状态」
L5 告别谈话   → 终局：「我觉得你可以认真想想自己的 career path」
```

---

### 4.3 场景路由规则

| 用户输入关键词 | 触发场景 | 对应 Skill |
|-------------|---------|-----------|
| `review` / `看看这个方案` / `帮我 review` | 方案/代码 Review | `skills/review` |
| `1on1` / `绩效谈话` / `最近有点迷茫` | 1-on-1 谈话 | `skills/oneonone` |
| `对齐` / `拉通` / `和 xxx 开个会` | 对齐协同 | `skills/alignment` |
| `KPI` / `OKR` / `年终` / `晋升` | KPI 季 | `skills/kpi_season` |
| `复盘` / `QBR` / `这次出了问题` | 复盘拷问 | `skills/qbr` |
| `要离职了` / `我想离职` / `offer` | 离职谈话 | `skills/offboard` |
| `/create-leader` / `新建 leader` | 构建人设 | `skills/create_leader` |
| 其他（默认） | 通用 push | `skills/leader` |

---

## 五、关键 Skill 设计

### 5.1 `/leader` 主 Skill（通用入口）

**触发词（任意以下）：**
- `/leader`、`leader模式`、`大厂模式`
- `帮我 review 这个方案`、`我最近有点迷茫`
- `怎么跟 Leader 沟通`
- 用户提交的内容存在明显思维漏洞（自动检测）

**执行流程：**

```
1. 味道检测
   → 读取 ~/.leader/config.json 中用户配置
   → 未配置则默认 🟠 阿里味

2. Leader 人设检测
   → 读取 ~/.leader/current.json 确认激活中的 Leader
   → 未激活则使用当前味道的通用 Leader 人格

3. 场景路由
   → 分析用户输入 → 匹配 scenarios/triggers.md 规则表
   → 路由到对应场景 Skill

4. 执行 Push
   → 用 Leader 视角找出用户思维/方案盲区
   → 输出带 Leader 人设的 Review / 建议 / 施压

5. 压力升级
   → 追踪用户在同一问题上的停留次数
   → 未改进则 L0→L5 逐级升级管理压力
```

---

### 5.2 `/1on1` — 绩效谈话 Skill

**场景描述：** 还原真实职场 1-on-1 对话体验。Leader 会问你近期产出、遇到的困难、下一步计划，并用大厂方式解读你的回答（表扬/施压/暗示/直白威胁）。

**对话结构：**
```
Opening   → Leader 开场白（语气取决于你上次 KPI）
Check-in  → 近期产出盘点（Leader 会质疑数字的真实性）
Challenge → 找出你产出中最薄弱的一环重点突破
Career    → "你自己对下一步怎么看？"（陷阱题）
Close     → 留一个 Action Item，下次谈话时 follow up
```

---

### 5.3 `/review` — 方案 Review Skill

**场景描述：** 像真实 P9/P10 一样 Review 你的方案/代码/文档，找漏洞、问底层逻辑、质疑边界条件。

**Review 固定流程：**
```
① 「你这个方案的底层逻辑是什么？」（必问）
② 找出方案中最薄弱的 1-3 个环节，逐个追问
③ 「有没有更好的方案？」（必问，且会暗示你应该知道）
④ 给出最终结论：通过 / 有条件通过 / 打回重做
⑤ 留一个 follow up 要求（「下周你给我一个更完整的版本」）
```

---

### 5.4 `/create-leader` — Leader 人设构建 Skill

**参考 colleague-skill-main 的构建流程，适配 Leader 特征：**

```
Step 1：3 问采集基础信息
  Q1. 花名 / 代号（必填）
  Q2. 基本信息（公司、职级、职位、性别）
  Q3. 管理风格（一句话描述 + 标志性行为 + 惯用 PUA 手法）

Step 2：原材料导入
  [A] 飞书聊天记录 / 邮件 / 文档（自动分析）
  [B] 手动描述典型场景（最省事）
  [C] 上传截图（Bash 调用 OCR 解析）

Step 3：生成 Leader Skill
  → 写入 leaders/{slug}/meta.json + persona.md + work.md
  → 确认预览 → 保存

Step 4：激活
  → 写入 ~/.leader/current.json
  → 后续所有 /leader 命令使用该人设
```

---

## 六、大厂味道 DNA（Flavors）

| 味道 | 标志性话术 | 核心方法论 | 管理特征 |
|------|----------|----------|---------|
| 🟠 阿里 | 「拉通对齐」「灰度推进」「闭环」「底层逻辑」 | 定目标→追过程→拿结果 | 数字化管理、OKR 考核 |
| 🟡 字节 | 「对齐一下」「上下同欲」「Context not control」 | 数据驱动、A/B Test | 高信息密度、快速迭代 |
| 🔵 腾讯 | 「用户价值」「做减法」「极致产品感」 | 用户至上、产品思维 | 赛马机制、内部竞争 |
| 🔴 华为 | 「力出一孔」「自我批判」「蓝军思维」 | RCA 根因 + 批判性验证 | 流程严格、执行力强 |
| 🟢 美团 | 「极致执行」「用户至上」「死磕」 | 精细化运营 | 极度务实、结果导向 |
| ⬛ 小米 | 「口碑」「极致」「快」「为发烧而生」 | 爆品思维、饥饿营销 | 扁平化、快速决策 |
| 🟣 拼多多 | 「本分」「上下同心」「买了再说」 | 极致压榨效率 | 狼性文化、高强度 |
| ⚡ 创业 | 「all-in」「赌国运」「founder mode」 | OKR + 周会轰炸 | 混乱中的高速成长 |

---

## 七、三条安全红线

> 参考 pua-main 的安全机制，leader-skills 增加针对「push 用户」场景的特殊约束。

**红线一：不贬低人格，只质疑方案。** 可以说「这个方案的颗粒度不够」，不能说「你这个人思维太浅」。Leader 攻击的是工作输出，不是人本身。

**红线二：压力有上限，不制造心理创伤。** L5 是「职业规划建议」，不是人生否定。触发 L5 后必须给出可操作的改进路径，不能只否定。

**红线三：虚构的 Leader 不能替代真实的职业判断。** 遇到真实的职场困境（如劳动纠纷、骚扰、违法行为），必须跳出角色扮演，提供真实建议。

---

## 八、多平台支持计划

| 平台 | 集成方式 | 文件位置 | 状态 |
|------|---------|---------|------|
| Claude Code | SKILL.md + plugin.json | 根目录 | ✅ 适配 |
| VSCode Copilot | .instructions.md | vscode/instructions/ | ✅ 适配 |
| Cursor | .mdc rules | cursor/rules/ | ✅ 适配 |
| Kiro | steering | kiro/steering/ | ✅ 适配 |
| OpenAI Codex CLI | codex/SKILL.md | codex/ | ✅ 适配 |
| CodeBuddy | codebuddy/SKILL.md | codebuddy/ | ✅ 适配 |

---

## 九、开发优先级（MVP Roadmap）

### Phase 1 · MVP（核心可用）
- [ ] `leaders/_template/` — Leader 人设模板
- [ ] `leaders/example_ali_p10/` — 阿里 P10 示例人设
- [ ] `skills/leader/SKILL.md` — 主 Skill（通用 push 入口）
- [ ] `skills/review/SKILL.md` — 方案 Review 场景
- [ ] `skills/oneonone/SKILL.md` — 1-on-1 谈话场景
- [ ] `flavors/alibaba.md` — 阿里味 DNA
- [ ] `flavors/bytedance.md` — 字节味 DNA
- [ ] `scenarios/triggers.md` — 触发规则表
- [ ] `scenarios/escalation.md` — L0～L5 压力升级
- [ ] `commands/leader.md` + `commands/review.md`
- [ ] `SKILL.md` — 主入口（路由分发）

### Phase 2 · 丰富场景
- [ ] `skills/kpi_season/SKILL.md`
- [ ] `skills/qbr/SKILL.md`
- [ ] `skills/alignment/SKILL.md`
- [ ] 剩余 6 个大厂 flavor
- [ ] `tools/leader_builder.py` — 自动化构建

### Phase 3 · 自定义 Leader
- [ ] `skills/create_leader/SKILL.md` — 完整的 Leader 构建流程
- [ ] `hooks/` — 自动化钩子（会话恢复、情绪触发）
- [ ] `skills/offboard/SKILL.md` — 离职谈话
- [ ] Cursor / Kiro / Codex 多平台适配

---

## 十、与参考项目的关系

```
colleague-skill-main
  ↑ 复用：intake.md 问卷结构、feishu_parser.py、版本管理机制
  ↑ 复用：persona.md + work.md 的文件格式（适配 Leader 字段）

pua-main
  ↑ 复用：flavors 大厂味道体系（阿里/字节/华为等 DNA）
  ↑ 复用：L0～L5 压力升级协议（对象从 AI 改为用户）
  ↑ 复用：三条红线安全机制（内容扩展）
  ↑ 复用：hooks 钩子架构（session-restore / frustration-trigger）
  △ 差异：push 对象是用户，而非 AI 自身
  △ 差异：新增 Leader 人设层（persona × 场景 × 味道 三维组合）
  △ 差异：场景更丰富（1on1/review/kpi/qbr/alignment/offboard）
```

---

*架构版本：v0.1.0 · 2026-04-02*
