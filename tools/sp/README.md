# SP - MongoDB Atlas Stream Processing CLI

**SP** is a comprehensive command-line tool for managing MongoDB Atlas Stream Processing workloads. It provides a unified interface for creating, deploying, testing, and monitoring stream processors with declarative configuration management.

## Quick Start

```bash
# Navigate to tools/sp directory
cd tools/sp/

# Test processors before deployment
./sp processors test

# Deploy processors
./sp processors create

# Check status
./sp processors list

# Monitor performance
./sp processors stats
```

## Core Features

- **Declarative Configuration**: Define processors and connections in JSON
- **Automated Testing**: Validate configurations before deployment
- **Tier Optimization**: Automatic processor tier selection based on complexity
- **Performance Monitoring**: Real-time statistics and metrics
- **Lifecycle Management**: Start, stop, restart, and delete processors
- **Connection Management**: HTTP and cluster connection handling
- **CI/CD Ready**: JSON output for pipeline integration

## Installation & Setup

### Prerequisites
- Python 3.7+
- MongoDB Atlas account with Stream Processing enabled
- Atlas API credentials

### Configuration
1. Create `config.txt` in the project root:
   ```
   PUBLIC_KEY=your_atlas_public_key
   PRIVATE_KEY=your_atlas_private_key
   PROJECT_ID=your_project_id
   ```

2. Make the tool executable:
   ```bash
   chmod +x tools/sp/sp
   ```

3. Verify installation:
   ```bash
   cd tools/sp/
   ./sp --version
   ```

## Usage

### Testing
```bash
# Test all processors
./sp processors test

# Test specific processor
./sp processors test -p solar_simple_processor
```

### Deployment
```bash
# Deploy connections
./sp workspaces connections create

# Deploy all processors
./sp processors create

# Deploy specific processor
./sp processors create -p processor_name
```

### Monitoring
```bash
# List all processors with full details (pipeline, stats, latency, errors)
./sp processors list

# Get performance statistics
./sp processors stats

# Get stats for specific processor with pipeline breakdown
./sp processors stats --processor processor_name --verbose
```

### Lifecycle Management
```bash
# Start processors
./sp processors start                    # Start all
./sp processors start -p processor_name  # Start specific

# Stop processors
./sp processors stop                     # Stop all
./sp processors stop -p processor_name   # Stop specific

# Restart processors
./sp processors restart                  # Restart all
./sp processors restart -p processor_name # Restart specific

# Delete processors
./sp processors drop processor_name      # Delete specific
./sp processors drop --all              # Delete all (careful!)
```

### Verifying Results
```bash
# After starting a processor that writes to MongoDB, always verify data flow
./sp collections count -c database.collection

# Query documents from a collection
./sp collections query -c database.collection -l 100

# Query with filter
./sp collections query -c database.collection -f '{"field": "value"}' -l 50

# Query with projection (specific fields only)
./sp collections query -c database.collection -p '{"field1": 1, "field2": 1}' -l 20

# Check processor performance and errors
./sp processors stats --processor processor_name
```

**Important**: When starting processors with `$merge` operations, always check the target MongoDB collection to confirm data is being written correctly.

## Creating Stream Processors

### Default Pattern: Simple Source-to-Sink
When you ask for a "stream processor" or "processor", the SP skill creates a basic source-to-sink pattern:

```json
{
  "name": "processor_name",
  "pipeline": [
    { "$source": { "connectionName": "...", "topic": "..." } },
    { "$merge": { "into": { "connectionName": "...", "db": "...", "coll": "..." } } }
  ]
}
```

**Key Principles:**
- ✅ **Start Simple**: Basic processor = source + sink only
- ✅ **No Assumptions**: Don't add transformations unless requested
- ✅ **Explicit Requests**: Add stages like `$addFields`, `$match`, etc. only when specified

### When to Add Transformation Stages
Only add additional pipeline stages when users explicitly request:
- Data filtering (`$match`)
- Field transformations (`$addFields`, `$project`)
- Aggregations (`$group`, `$count`)
- Time windows (`$tumblingWindow`)
- Custom functions (`$function`)

## File Structure

```
project_root/
├── config.txt                    # Atlas credentials
├── connections/
│   └── connections.json          # Connection definitions
├── processors/
│   ├── processor1.json          # Processor definitions
│   └── processor2.json
└── tools/
    └── sp/                      # SP skill (self-contained)
        ├── sp                   # Main CLI tool
        ├── atlas_api.py         # Atlas API client
        ├── requirements.txt     # Python dependencies
        ├── README.md            # This file
        ├── sp.yaml              # Skill metadata
        ├── sp-schema.json       # JSON schema
        ├── SP_QUICKREF.md       # Quick reference
        └── examples/            # Example workflows
```

## Output Format

All commands return structured JSON for easy parsing and automation:

```json
{
  "timestamp": "2026-01-21T10:30:00Z",
  "operation": "create_processors",
  "summary": {
    "total": 2,
    "success": 2,
    "failed": 0
  },
  "processors": [
    {
      "name": "my_processor",
      "status": "created",
      "tier": "SP30",
      "message": "Processor created successfully"
    }
  ]
}../docs/SP_UTILITY_SUMMARY.md)** - Quick reference for AI assistants
- **[SP_USER_MANUAL.md](../../docs/SP_USER_MANUAL.md)** - Comprehensive user manual
- **[SP_QUICKREF.md](SP_QUICKREF.md)** - Ultra-concise command reference
- **[AI_ASSISTANT_GUIDE.md](../../docs/AI_ASSISTANT_GUIDE.md)** - Guide for AI-powered workflows
- **[TESTING_GUIDE.md](../
- **[SP_UTILITY_SUMMARY.md](../docs/SP_UTILITY_SUMMARY.md)** - Quick reference for AI assistants
- **[SP_USER_MANUAL.md](../docs/SP_USER_MANUAL.md)** - Comprehensive user manual
- **[SP_QUICKREF.md](SP_QUICKREF.md)** - Ultra-concise command reference
- **[AI_ASSISTANT_GUIDE.md](../docs/AI_ASSISTANT_GUIDE.md)** - Guide for AI-powered workflows
- **[TESTING_GUIDE.md](../docs/TESTING_GUIDE.md)** - Testing and validation guide

## Examples

See the `examples/` directory for:
- Common workflow patterns
- Sample processor configurations
- CI/CD pipeline examples
- Error handling patterns

## Support

For issues, questions, or contributions:
- Review the [SP User Manual](../../docs/SP_USER_MANUAL.md)
- Check the [Testing Guide](../../docs/TESTING_GUIDE.md)
- See processor examples in `processors/` directory

## License

See [LICENSE](../../LICENSE) file in the project root.
