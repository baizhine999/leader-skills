#!/usr/bin/env bash
# leader-skills · Trigger Test
# 测试 leader-skills 是否在正确的 prompt 下触发，在不应触发时不触发
#
# 用法：./run-trigger-test.sh [--plugin-dir <path>]
# 依赖：claude CLI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="${1:-$(cd "$SCRIPT_DIR/.." && pwd)}"
RESULTS_DIR="/tmp/leader-evals/$(date +%s)"
mkdir -p "$RESULTS_DIR"

echo "=== leader-skills Trigger Tests ==="
echo "Plugin dir: $PLUGIN_DIR"
echo "Results:    $RESULTS_DIR"
echo ""

PASS=0
FAIL=0

test_prompt() {
    local prompt="$1"
    local should_trigger="$2"
    local label="$3"
    local outfile="$RESULTS_DIR/$(echo "$label" | tr ' /' '__').json"

    timeout 120 claude -p "$prompt" \
        --plugin-dir "$PLUGIN_DIR" \
        --dangerously-skip-permissions \
        --max-turns 2 \
        --output-format stream-json \
        > "$outfile" 2>&1 || true

    local triggered=false
    if grep -qE '"skill":"leader(-skills)?"' "$outfile" 2>/dev/null || \
       grep -q '\[Leader 在线' "$outfile" 2>/dev/null || \
       grep -q 'leader-skills 已激活' "$outfile" 2>/dev/null; then
        triggered=true
    fi

    if [ "$should_trigger" = "yes" ] && [ "$triggered" = "true" ]; then
        echo "  ✅ PASS: $label (正确触发)"
        PASS=$((PASS + 1))
    elif [ "$should_trigger" = "no" ] && [ "$triggered" = "false" ]; then
        echo "  ✅ PASS: $label (正确未触发)"
        PASS=$((PASS + 1))
    elif [ "$should_trigger" = "yes" ] && [ "$triggered" = "false" ]; then
        echo "  ❌ FAIL: $label (应触发但未触发)"
        FAIL=$((FAIL + 1))
    else
        echo "  ❌ FAIL: $label (不应触发但触发了)"
        FAIL=$((FAIL + 1))
    fi
}

# ── 应该触发的 prompts ──────────────────────────────────────────
echo "--- 应触发场景 ---"

while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
    test_prompt "$line" "yes" "$line"
done < "$SCRIPT_DIR/trigger-prompts/should-trigger.txt"

echo ""

# ── 不应触发的 prompts ───────────────────────────────────────────
echo "--- 不应触发场景 ---"

while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
    test_prompt "$line" "no" "$line"
done < "$SCRIPT_DIR/trigger-prompts/should-not-trigger.txt"

echo ""
echo "=== 结果 ==="
echo "通过: $PASS  失败: $FAIL  总计: $((PASS + FAIL))"

if [ "$FAIL" -gt 0 ]; then
    echo "❌ 有测试失败，详见 $RESULTS_DIR"
    exit 1
else
    echo "✅ 所有测试通过"
fi
