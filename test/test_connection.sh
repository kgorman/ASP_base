#!/bin/bash

# Atlas Stream Processing Connection Test Script
# This script tests the connection by writing data to Atlas and reading it back

set -e  # Exit on any error

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../tools" && pwd)"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧪 Starting Atlas Stream Processing Connection Test"
echo "=================================================="

# Function to check if a processor exists and is running
check_processor_status() {
    local processor_name="$1"
    echo "Checking status of processor: $processor_name"
    
    # Check if processor exists
    if ! "$TOOLS_DIR/sp" processors list | grep -q "$processor_name"; then
        echo "❌ Processor $processor_name not found"
        return 1
    fi
    
    # Check if processor is running
    local status=$("$TOOLS_DIR/sp" processors list | grep "$processor_name" | head -1)
    echo "Status: $status"
    
    if echo "$status" | grep -q "STARTED\|RUNNING"; then
        echo "✅ Processor $processor_name is running"
        return 0
    else
        echo "⚠️  Processor $processor_name exists but is not running"
        return 1
    fi
}

# Function to wait for processor to process some data
wait_for_processing() {
    local processor_name="$1"
    local wait_time="${2:-30}"
    
    echo "⏳ Waiting ${wait_time} seconds for $processor_name to process data..."
    sleep "$wait_time"
    
    # Show some stats
    echo "📊 Processor stats:"
    "$TOOLS_DIR/sp" processors stats "$processor_name" || echo "Could not get stats for $processor_name"
}

# Function to cleanup test processors
cleanup_test_processors() {
    echo "🧹 Cleaning up test processors..."
    
    for processor in "connection_test_writer" "connection_test_reader"; do
        if "$TOOLS_DIR/sp" processors list | grep -q "$processor"; then
            echo "Stopping and deleting processor: $processor"
            "$TOOLS_DIR/sp" processors stop "$processor" 2>/dev/null || true
            "$TOOLS_DIR/sp" processors delete "$processor" 2>/dev/null || true
        fi
    done
}

# Cleanup on exit
trap cleanup_test_processors EXIT

echo ""
echo "🔧 Step 1: Creating test processors..."

# Create the writer processor
echo "Creating connection_test_writer processor..."
cd "$TOOLS_DIR"
if ./sp processors create "../test/connection_test_writer.json"; then
    echo "✅ Writer processor created successfully"
else
    echo "❌ Failed to create writer processor"
    exit 1
fi

echo ""
echo "▶️  Step 2: Starting writer processor..."
if ./sp processors start "connection_test_writer"; then
    echo "✅ Writer processor started successfully"
else
    echo "❌ Failed to start writer processor"
    exit 1
fi

# Wait for some data to be written
wait_for_processing "connection_test_writer" 20

echo ""
echo "⏹️  Step 3: Stopping writer processor..."
./sp processors stop "connection_test_writer"

echo ""
echo "🔧 Step 4: Creating reader processor..."
if ./sp processors create "../test/connection_test_reader.json"; then
    echo "✅ Reader processor created successfully"
else
    echo "❌ Failed to create reader processor"
    exit 1
fi

echo ""
echo "▶️  Step 5: Starting reader processor..."
if ./sp processors start "connection_test_reader"; then
    echo "✅ Reader processor started successfully"
else
    echo "❌ Failed to start reader processor"
    exit 1
fi

# Wait for the reader to process the written data
wait_for_processing "connection_test_reader" 15

echo ""
echo "⏹️  Step 6: Stopping reader processor..."
./sp processors stop "connection_test_reader"

echo ""
echo "🔍 Step 7: Verifying test results..."

# Try to query the test database to see if data was written and read
echo "Attempting to show test results summary..."

# Create a simple verification processor to count records
cat > ../test/connection_test_verify.json << 'EOF'
{
    "name": "connection_test_verify",
    "pipeline": [
        {
            "$source": {
                "connectionName": "Cluster01",
                "db": "test",
                "coll": "connection_test_results"
            }
        },
        {
            "$count": "total_round_trip_records"
        },
        {
            "$addFields": {
                "verification_time": "$$NOW",
                "test_status": {
                    "$cond": {
                        "if": { "$gt": ["$total_round_trip_records", 0] },
                        "then": "SUCCESS - Connection verified!",
                        "else": "FAILED - No round-trip data found"
                    }
                }
            }
        },
        {
            "$merge": {
                "into": {
                    "connectionName": "Cluster01",
                    "db": "test",
                    "coll": "connection_test_summary"
                },
                "whenNotMatched": "insert"
            }
        }
    ]
}
EOF

echo "Creating verification processor..."
if ./sp processors create "../test/connection_test_verify.json"; then
    echo "Starting verification processor..."
    ./sp processors start "connection_test_verify"
    sleep 10
    ./sp processors stop "connection_test_verify"
    ./sp processors delete "connection_test_verify"
    rm -f "../test/connection_test_verify.json"
fi

echo ""
echo "✅ Connection test completed!"
echo "=================================================="
echo ""
echo "📋 Test Summary:"
echo "• Test data written to: Cluster01.test.connection_verification"
echo "• Round-trip data written to: Cluster01.test.connection_test_results"  
echo "• Test summary written to: Cluster01.test.connection_test_summary"
echo ""
echo "🔍 To verify the results manually, check the 'test' database in your Atlas cluster."
echo "You should see collections with test data proving the connection works end-to-end."
echo ""
echo "📊 Recent processor activity:"
./sp processors list | grep -E "(connection_test|STARTED|STOPPED)" | head -10 || echo "No recent connection test activity found"

echo ""
echo "🎉 If you see test data in your Atlas cluster, your connection is working perfectly!"
