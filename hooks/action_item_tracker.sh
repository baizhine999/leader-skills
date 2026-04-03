#!/bin/bash
# Action Item Tracker Hook
# 在新对话开始时检查上次的 Action Item，并询问完成情况

SESSION_FILE="${HOME}/.leader/session.json"

if [ ! -f "$SESSION_FILE" ]; then
  echo "NO_PREVIOUS_SESSION"
  exit 0
fi

# 读取上次 Action Item
ACTION_ITEM=$(cat "$SESSION_FILE" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('last_action_item', ''))
" 2>/dev/null || echo "")

# 读取上次对话日期
LAST_DATE=$(cat "$SESSION_FILE" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('last_session_date', ''))
" 2>/dev/null || echo "")

# 计算距上次对话的天数
DAYS_SINCE=""
if [ -n "$LAST_DATE" ]; then
  DAYS_SINCE=$(LAST_DATE="$LAST_DATE" python3 -c "
import os
from datetime import datetime, date
try:
    last = datetime.strptime(os.environ['LAST_DATE'], '%Y-%m-%d').date()
    today = date.today()
    print((today - last).days)
except Exception:
    print('unknown')
" 2>/dev/null || echo "unknown")
fi

if [ -n "$ACTION_ITEM" ]; then
  echo "HAS_ACTION_ITEM"
  echo "ACTION_ITEM=$ACTION_ITEM"
  echo "LAST_DATE=$LAST_DATE"
  echo "DAYS_SINCE=$DAYS_SINCE"
else
  echo "NO_ACTION_ITEM"
fi
