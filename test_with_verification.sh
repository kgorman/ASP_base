#!/bin/bash

# Atlas Stream Processing Connection Test with MongoDB Verification
# This script runs the connection test using the virtual environment with pymongo

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r test/requirements.txt
else
    echo "Using existing virtual environment"
    source venv/bin/activate
fi

echo "Running Atlas Stream Processing Connection Test with MongoDB Verification"
echo ""

# Check if MONGODB_CONNECTION_STRING is set
if [ -z "$MONGODB_CONNECTION_STRING" ]; then
    echo "MONGODB_CONNECTION_STRING environment variable not set"
    echo "   The test will run but without MongoDB native driver verification"
    echo "   For full verification, set your MongoDB connection string:"
    echo "   export MONGODB_CONNECTION_STRING='mongodb+srv://user:pass@cluster.mongodb.net/'"
    echo ""
    echo "   Example for your KGShardedCluster01:"
    echo "   export MONGODB_CONNECTION_STRING='mongodb+srv://<username>:<password>@kgshardedcluster01.mongodb.net/'"
    echo ""
fi

# Run the test
python3 test/test_connection.py

echo ""
echo "Virtual environment deactivated"
