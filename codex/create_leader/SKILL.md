---
name: create_leader
description: "Leader 人设构建器。通过 3 个问题 + 材料导入，帮助用户把一个真实的 Leader（上司/偶像/前辈）蒸馏成可复用的 AI Leader 人设。输出标准的 meta.json + persona.md + work.md 三件套。触发词：/create-leader, 我想创建一个Leader, 把我老板蒸馏成AI, 录入新Leader。"
license: MIT
---

# leader-skills · Create Leader（CodeBuddy 版）

好，我们来创建一个新的 Leader 人设。

## 三问采集

**Q1：他是谁？**  
花名/代号（必填）。

**Q2：基本信息？**  
公司、职级、职位、性别（影响话术风格）。

**Q3：管理风格？**  
一句话描述他的标志性管理方式 + 他最经典的一句话/行为。

## 原材料（可选）

- 粘贴飞书/微信聊天记录 → AI 自动提取话术特征
- 描述典型场景（「他开会时最喜欢问……」）
- 上传邮件截图（Bash 调用解析）

## 输出

```
leaders/{slug}/meta.json    — 基本信息
leaders/{slug}/persona.md   — 人格画像
leaders/{slug}/work.md      — 工作风格
```

采集完成后，写入文件并询问是否立即激活。
