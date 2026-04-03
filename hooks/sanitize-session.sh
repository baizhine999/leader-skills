#!/usr/bin/env bash
# sanitize-session.sh — 清除本次对话的临时状态
# 由对话结束 hook 调用，避免 session 状态污染下次对话

set -euo pipefail

CONFIG_DIR="${HOME}/.leader"
SESSION_FILE="${CONFIG_DIR}/session.json"
TEMP_CORRECTIONS="${CONFIG_DIR}/pending_corrections.json"

# ── 清除 session 临时状态 ────────────────────────────────────────────────────

echo "[leader-skills] 🧹 清理 session 状态..."

# 清除当前 session 标记（保留 config.json 不动）
if [[ -f "${SESSION_FILE}" ]]; then
    rm -f "${SESSION_FILE}"
    echo "  ✓ session.json 已清除"
fi

# 清除未保存的修正意见（如果对话中没有保存）
if [[ -f "${TEMP_CORRECTIONS}" ]]; then
    CORRECTION_COUNT=$(python3 -c "
import json, os
path = os.path.expanduser('~/.leader/pending_corrections.json')
try:
    d = json.load(open(path))
    print(len(d) if isinstance(d, list) else len(d.keys()))
except Exception:
    print(0)
" 2>/dev/null || echo "0")
    if [[ "${CORRECTION_COUNT}" -gt 0 ]]; then
        echo "  ⚠️  有 ${CORRECTION_COUNT} 条未保存的修正记录"
        echo "  💡 提示：运行 version_manager.py snapshot 保存当前状态"
    fi
    rm -f "${TEMP_CORRECTIONS}"
    echo "  ✓ 临时修正记录已清除"
fi

# 清除 action item 临时文件（已由 action_item_tracker.sh 归档）
TEMP_ACTIONS="${CONFIG_DIR}/session_actions.json"
if [[ -f "${TEMP_ACTIONS}" ]]; then
    rm -f "${TEMP_ACTIONS}"
    echo "  ✓ session 行动项临时文件已清除"
fi

# 重置 escalation level（对话结束后归零）
CONFIG_FILE="${CONFIG_DIR}/config.json"
if [[ -f "${CONFIG_FILE}" ]]; then
    python3 - <<'PYTHON'
import json, os
config_path = os.path.expanduser("~/.leader/config.json")
with open(config_path, encoding="utf-8") as f:
    config = json.load(f)
if config.get("current_level", 0) > 0:
    config["current_level"] = 0
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print("  ✓ 压力等级已重置为 L0")
PYTHON
fi

echo "[leader-skills] ✅ sanitize 完成"
