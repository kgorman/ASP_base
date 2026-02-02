#!/bin/bash
#
# Example SP Workflow Script
# Demonstrates common usage patterns for the SP tool
#

set -e  # Exit on error

echo "=== SP Tool - Example Workflow ==="
echo ""

# Always start in the tools directory
cd "$(dirname "$0")/.."

echo "Step 1: List existing processors"
echo "Command: ./sp processors list"
./sp processors list
echo ""

echo "Step 2: Test all processor configurations"
echo "Command: ./sp processors test"
./sp processors test
echo ""

echo "Step 3: Test a specific processor"
echo "Command: ./sp processors test -p solar_simple_processor"
# Uncomment to run:
# ./sp processors test -p solar_simple_processor
echo "[Skipped in example - uncomment to run]"
echo ""

echo "Step 4: Deploy connections (if needed)"
echo "Command: ./sp workspaces connections create"
# Uncomment to run:
# ./sp workspaces connections create
echo "[Skipped in example - uncomment to run]"
echo ""

echo "Step 5: Create/deploy all processors"
echo "Command: ./sp processors create"
# Uncomment to run:
# ./sp processors create
echo "[Skipped in example - uncomment to run]"
echo ""

echo "Step 6: Create a specific processor"
echo "Command: ./sp processors create -p solar_simple_processor"
# Uncomment to run:
# ./sp processors create -p solar_simple_processor
echo "[Skipped in example - uncomment to run]"
echo ""

echo "Step 7: Check processor status"
echo "Command: ./sp processors list"
./sp processors list
echo ""

echo "Step 8: Get performance statistics"
echo "Command: ./sp processors stats"
# Uncomment to run:
# ./sp processors stats
echo "[Skipped in example - uncomment to run]"
echo ""

echo "Step 9: Start a processor with auto-wait"
echo "Command: ./sp processors start -p solar_simple_processor --auto"
# Uncomment to run:
# ./sp processors start -p solar_simple_processor --auto
echo "[Skipped in example - uncomment to run]"
echo ""

echo "Step 10: Get stats for specific processor"
echo "Command: ./sp processors stats --processor solar_simple_processor"
# Uncomment to run:
# ./sp processors stats --processor solar_simple_processor
echo "[Skipped in example - uncomment to run]"
echo ""

echo "=== Advanced Operations ==="
echo ""

echo "Stop a specific processor:"
echo "  ./sp processors stop -p processor_name"
echo ""

echo "Restart all processors:"
echo "  ./sp processors restart"
echo ""

echo "Delete a specific processor:"
echo "  ./sp processors drop processor_name"
echo ""

echo "Delete ALL processors (careful!):"
echo "  ./sp processors drop --all"
echo ""

echo "=== Workflow Complete ==="
echo ""
echo "Notes:"
echo "- Always run from the tools/ directory"
echo "- Test configurations before deploying"
echo "- Use --auto flag when starting processors to wait for CREATED state"
echo "- All commands return structured JSON output"
echo ""
