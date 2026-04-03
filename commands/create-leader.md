# `/create-leader` — 构建新的 Leader 人设

**触发方式**

```
/create-leader
我想创建一个 Leader
把我老板蒸馏成 AI
录入新 Leader
新建人设
```

**作用**

激活 `skills/create_leader/SKILL.md`，进入 Leader 人设构建器模式。

Builder 将：
- 通过三个问题收集 Leader 的核心特征
- 支持粘贴聊天记录/邮件等原始材料
- 自动生成 `meta.json` + `persona.md` + `work.md` 三件套
- 写入 `leaders/{id}/` 目录供后续使用

**用法示例**

```
用户：/create-leader
Builder：好，我们来创建一个新的 Leader。
         你要创建的这个 Leader，他是谁？

用户：把我前上司录进去，他叫老李
Builder：他在哪家公司，大概什么职级/角色？你跟他的关系是什么？
```

**也可以用命令行工具**

```bash
cd tools/
python3 leader_builder.py --interactive
# 或者
python3 leader_builder.py --input ./my_chat_logs/ --name "老李" --output ../leaders/
```

**生成完成后激活**

```
/leader 老李    # 激活刚创建的 Leader 人设
```
