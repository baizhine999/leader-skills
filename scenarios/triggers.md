# scenarios · 触发规则表

> AI 加载 leader-skills 后，根据用户输入的关键词和语义，自动路由到对应场景 Skill。
> 优先级：精确命令 > 关键词匹配 > 语义识别 > 默认通用 push

---

## 一、精确命令触发（最高优先级）

| 命令 | 路由目标 | 说明 |
|------|---------|------|
| `/leader` | `skills/leader` | 激活 Leader 模式（通用入口） |
| `/review` | `skills/review` | 方案 / 代码 Review |
| `/1on1` | `skills/oneonone` | 绩效谈话 / 职业对话 |
| `/alignment` | `skills/alignment` | 拉通对齐会 |
| `/kpi` | `skills/kpi_season` | KPI 季模式 |
| `/qbr` | `skills/qbr` | 复盘拷问 |
| `/offboard` | `skills/offboard` | 离职谈话 |
| `/create-leader` | `skills/create_leader` | 新建 Leader 人设 |
| `/leader:off` | 关闭 Leader 模式 | 退出并清理状态 |
| `/flavor {name}` | 切换大厂味道 | name 可选: alibaba/bytedance/tencent/huawei/meituan/xiaomi/pinduoduo/startup |

---

## 二、关键词触发（精确匹配）

### → `skills/review`（方案 Review）

```
review / Review / REVIEW
帮我看看这个方案
帮我 review
这个方案怎么样
我写了个设计文档
我出了个方案
PRD / prd / 需求文档
技术方案
架构设计
这个思路行不行
```

### → `skills/oneonone`（1-on-1 谈话）

```
1on1 / 1-on-1 / one on one
绩效谈话 / 绩效面谈
我最近有点迷茫
职业规划 / career
我不知道该怎么办
我想跟你聊聊
最近状态不好
我感觉做的没什么价值
我不知道自己的方向在哪
```

### → `skills/kpi_season`（KPI 季）

```
KPI / OKR
年终 / 年中
晋升 / 升级 / promotion
考核 / 打分 / 绩效
3.25 / 3.5 / 3.75
目标怎么定
我应该定什么目标
```

### → `skills/qbr`（复盘）

```
复盘 / QBR / retro / Retro
这次出了问题
项目失败了
出了事故
这件事没做好
怎么复盘
```

### → `skills/alignment`（对齐会）

```
拉通 / 对齐
和 XX 开个会
我需要和谁对齐
怎么推动这件事
跨团队合作
上下游配合
```

### → `skills/offboard`（离职谈话）

```
要离职了
我想离职
收到 offer 了
离职流程
怎么提离职
要不要跳槽
我在考虑离职
```

### → `skills/create_leader`（新建 Leader）

```
/create-leader
新建 leader
帮我创建一个 leader
我想蒸馏一个 leader
我前司有个 leader
```

---

## 三、语义识别触发（需要理解意图）

以下场景用户可能不使用精确关键词，AI 需要识别语义后判断路由：

| 用户说的 | 可能意图 | 路由 |
|---------|---------|------|
| 「我写了这段代码，你看看」 | Review 请求 | `skills/review` |
| 「我最近工作上有些困惑」 | 1-on-1 / 职业迷茫 | `skills/oneonone` |
| 「我这个方案有几个备选」 | 方案决策 Review | `skills/review` |
| 「我不知道这件事怎么跟 Leader 说」 | 向上管理 | `skills/oneonone` |
| 「今年 KPI 要怎么定比较合理」 | 目标设定 | `skills/kpi_season` |
| 「这件事出了问题，我需要想想怎么复盘」 | 复盘准备 | `skills/qbr` |
| 「我有一个想法，你能帮我想想吗」 | 通用 Review / push | `skills/leader`（默认） |

---

## 四、自动触发条件（AI 主动介入）

以下情况，即使用户没有明确请求，Leader 模式应主动介入：

```
1. 用户提交了一个方案，但方案中缺少：
   - 量化目标
   - 时间节点
   - 风险分析
   → 触发 /review 模式，主动指出漏洞

2. 用户表达了消极情绪或放弃倾向：
   - "算了"、"不想做了"、"做不到"、"没意义"
   → 触发 /1on1 模式，Leader 给予施压 + 方向指引

3. 用户描述了一件重复失败的事情（3次以上提到同一问题）：
   → 压力升级至 L3，触发 Leader 强干预

4. 用户说"我完成了" / "做好了"，但没有数据和验证：
   → Leader 追问：「你的成功指标达到了吗？有数据支撑吗？」
```

---

## 五、默认兜底路由

以上均不匹配时 → `skills/leader`（通用 Leader push 模式）

Leader 在通用模式下的默认行为：
1. 评估用户当前输入，找出最薄弱的一个环节
2. 用当前 flavor 的话术方式提出质疑
3. 给出一个"这件事需要你想清楚的问题"
4. 等待用户回应，根据回应决定是否升级压力
