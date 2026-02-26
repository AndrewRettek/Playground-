#!/bin/bash
## run_tests.sh - Run BindrChat Ren'Py tests with automatic cleanup
##
## Usage:
##   ./run_tests.sh                   # Run lint only (no window)
##   ./run_tests.sh smoke_test        # Run a specific test case
##   ./run_tests.sh all               # Run all test cases
##
## The test runner opens a game window that stays open after completion.
## This script monitors output, captures the result, then kills the process.

RENPY="C:/Users/andre/Downloads/renpy-8.5.2-sdk/renpy.exe"
PROJECT="C:/Users/andre/Playground-"

## --- Lint (always runs first, headless) ---
echo "=== Running Ren'Py Lint ==="
"$RENPY" "$PROJECT" lint 2>&1
LINT_EXIT=$?

if [ $LINT_EXIT -ne 0 ]; then
    echo ""
    echo "LINT FAILED (exit code $LINT_EXIT)"
    exit 1
fi
echo ""
echo "Lint passed."

## If no test argument, stop after lint
if [ -z "$1" ]; then
    echo "No test specified. Run './run_tests.sh smoke_test' to run a test."
    exit 0
fi

## --- Test Runner ---
TEST_NAME="$1"
echo ""
echo "=== Running Test: $TEST_NAME ==="

## Run the test in background and capture output
TMPFILE=$(mktemp)

if [ "$TEST_NAME" = "all" ]; then
    "$RENPY" "$PROJECT" test > "$TMPFILE" 2>&1 &
else
    "$RENPY" "$PROJECT" test "$TEST_NAME" > "$TMPFILE" 2>&1 &
fi
TEST_PID=$!

## Monitor output for PASSED/FAILED (check every 2 seconds, max 90 seconds)
ELAPSED=0
RESULT=""
while [ $ELAPSED -lt 90 ]; do
    sleep 2
    ELAPSED=$((ELAPSED + 2))

    if grep -q "Status: PASSED" "$TMPFILE" 2>/dev/null; then
        RESULT="PASSED"
        break
    fi
    if grep -q "Status: FAILED" "$TMPFILE" 2>/dev/null; then
        RESULT="FAILED"
        break
    fi
    ## Check if process already exited
    if ! kill -0 $TEST_PID 2>/dev/null; then
        RESULT="EXITED"
        break
    fi
done

## Print test output
echo ""
cat "$TMPFILE"
echo ""

## Kill the lingering Ren'Py process (game window stays open after test)
if kill -0 $TEST_PID 2>/dev/null; then
    kill $TEST_PID 2>/dev/null
    sleep 1
    kill -9 $TEST_PID 2>/dev/null
fi

rm -f "$TMPFILE"

## Report result
if [ "$RESULT" = "PASSED" ]; then
    echo "TEST RESULT: PASSED"
    exit 0
elif [ "$RESULT" = "FAILED" ]; then
    echo "TEST RESULT: FAILED"
    exit 1
elif [ "$RESULT" = "EXITED" ]; then
    echo "TEST RESULT: Process exited (check output above)"
    exit 1
else
    echo "TEST RESULT: TIMEOUT (no result after 90 seconds)"
    exit 1
fi
