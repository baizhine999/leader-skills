#!/bin/bash
# Frustration Detection + Pressure Auto-Reset Hook
# 检测用户是否处于高压状态，并在必要时降低压力等级

USER_MESSAGE="$1"
SESSION_FILE="${HOME}/.leader/session.json"

# 沮丧/高压关键词列表
FRUSTRATION_KEYWORDS=("我不行了" "太难了" "要崩了" "放弃" "撑不住" "好累" "我快顶不住了" "焦虑死了" "想辞职" "心态崩了" "不想干了" "累死了")

# 完成/进步关键词列表
PROGRESS_KEYWORDS=("完成了" "做好了" "已经搞定" "提交了" "改好了" "弄完了" "达成了" "拿到了")

# 检测是否包含沮丧关键词
detect_frustration() {
  for keyword in "${FRUSTRATION_KEYWORDS[@]}"; do
    if [[ "$USER_MESSAGE" == *"$keyword"* ]]; then
      echo "FRUSTRATION_DETECTED"
      echo "KEYWORD=$keyword"
      return 0
    fi
  done
  echo "NO_FRUSTRATION"
  return 1
}

# 检测是否包含进步关键词
detect_progress() {
  for keyword in "${PROGRESS_KEYWORDS[@]}"; do
    if [[ "$USER_MESSAGE" == *"$keyword"* ]]; then
      echo "PROGRESS_DETECTED"
      echo "KEYWORD=$keyword"
      return 0
    fi
  done
  echo "NO_PROGRESS"
  return 1
}

# 读取当前压力等级
CURRENT_LEVEL=$(cat "$SESSION_FILE" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('pressure_level',0))" 2>/dev/null || echo "0")

# 执行检测
FRUSTRATION_RESULT=$(detect_frustration)
PROGRESS_RESULT=$(detect_progress)

if [[ "$FRUSTRATION_RESULT" == FRUSTRATION_DETECTED* ]]; then
  echo "$FRUSTRATION_RESULT"
  echo "CURRENT_LEVEL=$CURRENT_LEVEL"
  echo "ACTION=REDUCE_PRESSURE_AND_SUPPORT"
elif [[ "$PROGRESS_RESULT" == PROGRESS_DETECTED* ]]; then
  echo "$PROGRESS_RESULT"
  echo "CURRENT_LEVEL=$CURRENT_LEVEL"
  echo "ACTION=REDUCE_PRESSURE_BY_ONE"
else
  echo "NO_ACTION"
fi
