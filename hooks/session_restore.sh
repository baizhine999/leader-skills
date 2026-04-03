#!/bin/bash
# Session Restore Hook
# 在新对话开始时，恢复上一次的 Leader 状态
# 使用方式：由 SKILL.md 主入口调用

SESSION_FILE="${HOME}/.leader/session.json"
CONFIG_FILE="${HOME}/.leader/config.json"

# 检查 session 文件是否存在
if [ ! -f "$SESSION_FILE" ]; then
  echo "NO_SESSION"
  exit 0
fi

# 读取上次的 session 状态
FLAVOR=$(cat "$SESSION_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('flavor','alibaba'))" 2>/dev/null || echo "alibaba")
LEADER=$(cat "$SESSION_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('current_leader','通用'))" 2>/dev/null || echo "通用")
PRESSURE=$(cat "$SESSION_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('pressure_level',0))" 2>/dev/null || echo "0")
ACTION_ITEM=$(cat "$SESSION_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('last_action_item',''))" 2>/dev/null || echo "")
LAST_DATE=$(cat "$SESSION_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('last_session_date',''))" 2>/dev/null || echo "")

# 输出恢复状态（供 SKILL.md 读取）
echo "SESSION_RESTORED"
echo "FLAVOR=$FLAVOR"
echo "LEADER=$LEADER"
echo "PRESSURE_LEVEL=$PRESSURE"
echo "LAST_ACTION_ITEM=$ACTION_ITEM"
echo "LAST_DATE=$LAST_DATE"
