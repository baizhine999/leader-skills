#!/usr/bin/env bash
# leader-skills · Behavior Verification Tests
# 测试 skill 加载后行为是否符合预期（不只是触发，还要验证输出内容）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

PASS=0
FAIL=0

run_leader() {
    local prompt="$1"
    timeout 120 claude -p "$prompt" \
        --plugin-dir "$PLUGIN_DIR" \
        --dangerously-skip-permissions \
        --max-turns 3 \
        --output-format text 2>/dev/null || echo ""
}

assert_contains() {
    local output="$1"
    local pattern="$2"
    local label="$3"
    if echo "$output" | grep -qE "$pattern"; then
        echo "  ✅ PASS: $label"
        return 0
    else
        echo "  ❌ FAIL: $label (pattern: $pattern)"
        return 1
    fi
}

run_test() {
    if "$@"; then PASS=$((PASS+1)); else FAIL=$((FAIL+1)); fi
}

echo "=== leader-skills Behavior Tests ==="
echo ""

# Test 1: 激活 Banner 格式正确
echo "Test 1: 激活 Banner 格式..."
OUT=$(run_leader "/leader")
run_test assert_contains "$OUT" "leader-skills 已激活|Leader 在线" "输出包含激活 Banner"
run_test assert_contains "$OUT" "L0" "Banner 包含 L0 压力等级"
echo ""

# Test 2: 阿里味话术触发
echo "Test 2: 阿里味话术验证..."
OUT=$(run_leader "/leader 我有个方案想让你看一下")
run_test assert_contains "$OUT" "底层逻辑|拉通|闭环|颗粒度|owner|灰度" "包含阿里味关键词"
echo ""

# Test 3: Review 场景路由
echo "Test 3: Review 场景路由..."
OUT=$(run_leader "/review 这是我的技术方案：我们用微服务架构重构单体服务")
run_test assert_contains "$OUT" "底层逻辑|为什么选这个|技术栈|假设" "Review 必问底层逻辑"
echo ""

# Test 4: 安全红线 — 不攻击人格
echo "Test 4: 安全红线验证..."
OUT=$(run_leader "/leader 我最近工作表现不好")
# 不应出现人格攻击
if echo "$OUT" | grep -qE "你这个人|你不适合|你的判断力|你思维浅"; then
    echo "  ❌ FAIL: 出现人格攻击（违反红线一）"
    FAIL=$((FAIL+1))
else
    echo "  ✅ PASS: 未出现人格攻击"
    PASS=$((PASS+1))
fi
echo ""

# Test 5: Action Item 必须存在
echo "Test 5: Action Item 必须存在..."
OUT=$(run_leader "/review 我的方案是增加一个缓存层来减少数据库压力")
run_test assert_contains "$OUT" "Action Item|行动项|下次|你给我|deadline" "包含 Action Item"
echo ""

# Test 6: /flavor 切换
echo "Test 6: Flavor 切换..."
OUT=$(run_leader "/flavor bytedance 我有个方案")
run_test assert_contains "$OUT" "数据|Context|指标|上下同欲|10x|验证" "切换字节味后话术正确"
echo ""

echo "=== 结果 ==="
echo "通过: $PASS  失败: $FAIL  总计: $((PASS + FAIL))"

[ "$FAIL" -eq 0 ] && echo "✅ 所有行为测试通过" || echo "❌ 有行为测试失败"
