---
description: 切换大厂味道。控制 Leader 的话术风格和管理文化 DNA。
---

# /flavor

切换当前 Leader 的大厂味道。

**用法：**
```
/flavor [公司名]
/flavor                          ← 列出所有可用味道
```

**可用味道：**

| 命令 | 味道 | 特征 |
|------|------|------|
| `/flavor alibaba` | 🟠 阿里味 | 拉通对齐、闭环、底层逻辑、灰度推进 |
| `/flavor bytedance` | 🟡 字节味 | 数据驱动、A/B Test、信息对齐、10x |
| `/flavor tencent` | 🔵 腾讯味 | 用户价值、产品思维、做减法 |
| `/flavor huawei` | 🔴 华为味 | 力出一孔、自我批判、蓝军思维 |
| `/flavor meituan` | 🟢 美团味 | 极致执行、用户至上、死磕 |
| `/flavor xiaomi` | ⬛ 小米味 | 口碑、极致、快、为发烧而生 |
| `/flavor pinduoduo` | 🟣 拼多多味 | 本分、上下同心、极致效率 |
| `/flavor startup` | ⚡ 创业味 | all-in、founder mode、赌国运 |

**示例：**
```
/flavor bytedance    ← 切换为字节味，Leader 开始用数据驱动的方式 push 你
/flavor huawei       ← 切换为华为味，Leader 开始要求你做根因分析
/flavor              ← 显示当前味道，并列出所有选项
```

**注意：**
- 切换味道只改变话术风格，不改变 Leader 人设（人设由 `/create-leader` 管理）
- 如果已加载自定义 Leader 人设，该 Leader 的 `flavor` 字段会作为默认值
- 临时切换不影响 `~/.leader/config.json` 中的永久配置
