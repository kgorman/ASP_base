# Connection Testing

This directory contains tools to test your Atlas Stream Processing connections and verify they're working properly.

## Quick Test

Run a complete connection test:

```bash
python3 test_connection.py
```

Or if executable:

```bash
./test_connection.py
```

This script will:
1. ✅ Write test data from sample_stream_solar to your Atlas cluster
2. ✅ Read the data back from your cluster 
3. ✅ Verify the round-trip data flow
4. ✅ Create summary results in your test database
5. ✅ Clean up test processors when done

## What Gets Tested

The test verifies your `Cluster01` connection by:

- **Write Test**: Takes sample solar data and writes it to `Cluster01.test.connection_verification`
- **Read Test**: Reads the written data and writes verification results to `Cluster01.test.connection_test_results`
- **Summary**: Creates a final summary in `Cluster01.test.connection_test_summary`

## Manual Testing

If you want to test individual components:

### Test Writer Only
```bash
cd tools
./sp processors create ../test/connection_test_writer.json
./sp processors start connection_test_writer
# Wait 30 seconds
./sp processors stop connection_test_writer
./sp processors delete connection_test_writer
```

### Test Reader Only
```bash
cd tools  
./sp processors create ../test/connection_test_reader.json
./sp processors start connection_test_reader
# Wait 15 seconds
./sp processors stop connection_test_reader
./sp processors delete connection_test_reader
```

## Verification

After running tests, check your Atlas cluster:

1. **Database**: `test`
2. **Collections**: 
   - `connection_verification` (written data)
   - `connection_test_results` (round-trip verification)
   - `connection_test_summary` (test summary)

If you see data in these collections, your connection is working perfectly!

## Troubleshooting

If the test fails:

1. **Check your connection**: Verify `Cluster01` exists and points to the right cluster
2. **Check permissions**: Ensure your Atlas user has read/write access to the `test` database
3. **Check instance**: Verify your Stream Processing instance is running
4. **Check API keys**: Ensure your Atlas API keys have Stream Processing permissions

Run individual steps manually to isolate any issues.
