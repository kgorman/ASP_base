# Atlas Stream Processing Base

A complete toolkit and template for building MongoDB Atlas Stream Processing applications. This repository provides a ready-to-use foundation with powerful command-line tools, structured configurations, and example processors to jumpstart your stream processing projects.

## What This Provides

- **Complete development toolkit** with unified CLI for all Stream Processing operations
- **Template structure** with example processors using sample solar data
- **JSON-based configuration** for processors and connections
- **Color-coded terminal output** for easy debugging and monitoring
- **Production-ready structure** you can clone and customize for your own use cases
- **Comprehensive testing framework** to validate your processors

## Project Structure

```
ASP_base/
├── config.txt                 # Atlas API credentials and configuration
├── connections/               # Connection definitions (databases, APIs, etc.)
│   └── connections.json      
├── processors/               # Stream processor pipeline definitions
│   ├── solar_simple_processor.json
│   └── test_emit_processor.json
├── tests/                   # Validation and testing framework
│   ├── test_processors.py
│   ├── test_runner.py
│   └── README.md
└── tools/                   # Management utilities
    ├── sp                   # Unified CLI tool (executable)
    ├── atlas_api.py        # Core API library
    └── requirements.txt    # Python dependencies
```

## Quick Start

### Option A: Use This Repository

```bash
git clone <this-repo>
cd ASP_base
pip install -r tools/requirements.txt
cp config.txt.example config.txt
# Edit config.txt with your Atlas credentials
```

### Option B: Create New Repository from Scratch

Use the repository setup script to create a fresh structure:

```bash
# Download just the setup script
curl -O https://raw.githubusercontent.com/kgorman/ASP_base/main/tools/create-repo-structure.sh
chmod +x create-repo-structure.sh

# Create new repository structure
./create-repo-structure.sh my-new-stream-processing-project
cd my-new-stream-processing-project

# Add your Atlas credentials
cp config.txt.example config.txt
# Edit config.txt with your Atlas credentials
```

### Deploy and Test

```bash
# Create all connections from JSON definitions
tools/sp create connections

# Create all processors from JSON definitions  
tools/sp create processors
```

### 4. Manage Processors

```bash
# List processor status
tools/sp list

# Start all processors
tools/sp start

# View detailed statistics
tools/sp stats

# Stop all processors
tools/sp stop
```

## Configuration

### Atlas API Configuration (`config.txt`)

This file contains your MongoDB Atlas credentials and project information:

```bash
# MongoDB Atlas API Credentials
PUBLIC_KEY=your_atlas_public_key
PRIVATE_KEY=your_atlas_private_key
PROJECT_ID=your_atlas_project_id
SP_INSTANCE_NAME=your_stream_processing_instance_name
```

**How to get these values:**
1. **Atlas API Keys**: Atlas UI → Access Manager → API Keys → Create API Key
2. **Project ID**: Atlas UI → Project Settings → General
3. **SP Instance Name**: Atlas UI → Stream Processing → Your instance name

### Connection Definitions (`connections/connections.json`)

Defines external connections for your stream processors to access data sources and destinations. Atlas Stream Processing supports many connection types for different platforms and services.

```json
{
  "connections": [
    {
      "name": "sample_stream_solar",
      "type": "Sample",
      "description": "Sample solar data stream for testing"
    },
    {
      "name": "atlas_cluster",
      "type": "Cluster",
      "clusterName": "YourAtlasCluster",
      "description": "MongoDB Atlas cluster for data storage"
    }
  ]
}
```

**Connection Types Available:**

Atlas Stream Processing supports connections to various platforms and services. For the complete list of supported connection types and their configuration options, see:

- **[Atlas Stream Processing Documentation](https://www.mongodb.com/docs/atlas/atlas-sp/)** - Complete Stream Processing reference including connections
- **[Connection Registry Management](https://www.mongodb.com/docs/atlas/atlas-stream-processing/manage-connection-registry/#manage-connections)** - How to manage and configure connections
- **[MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)** - Full Atlas platform documentation

Common connection types include databases, message queues, REST APIs, cloud storage, and streaming platforms.

**Variable Substitution**: Use `${VARIABLE_NAME}` to reference values from `config.txt`

### Processor Definitions (`processors/*.json`)

Each processor is a JSON file defining a complete stream processing pipeline. Atlas Stream Processing supports the full MongoDB aggregation pipeline syntax plus streaming-specific stages.

**Required Structure:**
```json
{
  "name": "your_processor_name",
  "pipeline": [
    // Your aggregation pipeline stages here
  ],
  "options": {
    // Optional configuration like DLQ, etc.
  }
}
```

**Example - Basic Data Processing:**
```json
{
  "name": "solar_data_processor",
  "pipeline": [
    {
      "$source": {
        "connectionName": "sample_stream_solar"
      }
    },
    {
      "$merge": {
        "into": {
          "connectionName": "atlas_cluster",
          "db": "solar",
          "coll": "processed_data"
        }
      }
    }
  ]
}
```

**Building Your Pipelines:**

Atlas Stream Processing supports hundreds of operators and stages. Rather than limiting yourself to a small subset, explore the full capabilities:

- **[Official Atlas Stream Processing Documentation](https://www.mongodb.com/docs/atlas/atlas-sp/)** - Complete reference for all stages and operators
- **[Stream Aggregation Pipeline](https://www.mongodb.com/docs/atlas/atlas-stream-processing/stream-aggregation/)** - Stream processing aggregation stages
- **[Stream Aggregation Expressions](https://www.mongodb.com/docs/atlas/atlas-stream-processing/stream-aggregation-expression/)** - Expressions for stream processing
- **[MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)** - Complete Atlas platform documentation

**Common Patterns:**
- **Data Ingestion**: `$source` → transformations → `$merge`
- **Real-time Analytics**: `$source` → `$match` → aggregations → `$emit`  
- **ETL Processing**: `$source` → complex transformations → multiple outputs
- **Alerting**: `$source` → `$match` conditions → `$emit` notifications

The examples in this repository show basic patterns, but your processors can be as simple or complex as your use case requires. Use the official documentation to discover the right stages for your specific needs.

## Tools/SP Command Reference

The `tools/sp` command is your main interface for managing Stream Processing:

### Processor Management

```bash
# List all processors with status
tools/sp list

# Show detailed processor statistics
tools/sp stats

# Start all processors
tools/sp start

# Stop all processors  
tools/sp stop

# Restart all processors (stop + start)
tools/sp restart
```

### Resource Creation

```bash
# Create connections from connections/*.json
tools/sp create connections

# Create processors from processors/*.json
tools/sp create processors
```

### Processor Testing

```bash
# Validate all processor JSON files
tools/sp test

# Test with detailed warnings
tools/sp test --verbose

# Test specific processor only
tools/sp test -p solar_simple_processor
```

### Repository Setup Script

Use the setup script to create new repositories with the complete structure:

```bash
# Create structure in current directory
./tools/create-repo-structure.sh

# Create in a new directory
./tools/create-repo-structure.sh /path/to/new/project

# What it creates:
# ├── config.txt.example         # Configuration template
# ├── connections/               # Connection definitions directory
# ├── processors/               # Stream processor definitions directory  
# ├── tools/                    # Management utilities directory
# ├── docs/                     # Documentation templates
# └── README.md                 # Complete project documentation
```

### Configuration Options

```bash
# Use custom config file
tools/sp --config /path/to/config.txt list

# All commands support custom config
tools/sp --config ./prod-config.txt create processors
```

### Output Format

All commands return color-coded JSON with:
- **Blue keys** for property names
- **Green strings** for text values  
- **Yellow numbers** for numeric values
- **Magenta booleans** for true/false

## Example Use Cases

This repository demonstrates a complete weather monitoring system, but you can adapt it for:

### IoT Data Processing
- Sensor data ingestion and alerting
- Real-time device monitoring
- Anomaly detection

### E-commerce Analytics  
- Order processing pipelines
- Inventory alerts
- Customer behavior analysis

### Financial Data
- Transaction monitoring
- Fraud detection alerts
- Real-time reporting

### Social Media Analytics
- Content processing
- Sentiment analysis
- Engagement tracking

## Customizing for Your Use Case

### 1. Update Connections
Edit `connections/connections.json` to point to your data sources and destinations.

### 2. Create Your Processors
Add new JSON files to `processors/` directory with your pipeline logic.

### 3. Modify Alert Logic
Update the `$match` and `$addFields` stages to implement your business rules.

### 4. Deploy and Monitor
Use `tools/sp` to deploy and monitor your processors in production.

## Troubleshooting

### Common Issues

1. Use `tools/sp --help` for command usage
2. Check the JSON output for detailed error messages
3. Review MongoDB Atlas Stream Processing logs in the UI
4. Validate your JSON files with a JSON formatter

**API authentication errors:**
- Verify your Atlas API keys have Stream Processing permissions
- Check that PROJECT_ID matches your Atlas project
- Ensure SP_INSTANCE_NAME matches your Stream Processing instance

**Connection creation failures:**

- Verify cluster names match exactly (case-sensitive)
- Check that external URLs are accessible

**Processor deployment issues:**
- Ensure JSON syntax is valid
- Check that connection names exist
- Verify database and collection names

## Configuration Files

### connections.json
Defines Atlas Stream Processing connections:

- **sample_stream_solar**: Sample data stream for solar/energy data
- **atlas_cluster**: MongoDB Atlas cluster for data storage

## Stream Processing Pipelines

Stream processors are defined in JSON files with MongoDB aggregation pipeline syntax:

### solar_simple_processor.json
- Uses sample solar data from built-in stream
- Processes and enriches solar observations with timestamps
- Stores data in MongoDB Atlas cluster using $merge operation
- Demonstrates basic data ingestion pattern

### test_emit_processor.json

- Uses sample solar data from built-in stream
- Demonstrates $emit operation for streaming output
- Shows how to send processed data to external systems or topics

## Management Tools

The `tools/` directory contains Python utilities for managing the Atlas Stream Processing environment:

- **sp**: Unified CLI tool for all Stream Processing operations (create, start, stop, test, etc.)
- **atlas_api.py**: Shared library for Atlas API operations with JSON colorization
- **test_runner.py**: Quick validation tool for processor configurations

## Features

- **Template Structure**: Ready-to-use foundation for any stream processing project
- **Sample Data Processing**: Built-in examples using solar energy data
- **Comprehensive Testing**: Dual validation framework with unittest and quick tests
- **Error Handling**: JSON validation and comprehensive error reporting
- **Monitoring**: Detailed statistics and status monitoring with colorized output
- **Configuration-Driven**: JSON-based configuration for easy management
- **Color-Coded Output**: User-friendly terminal output with status indicators

## Prerequisites

- MongoDB Atlas account with Stream Processing enabled
- Python 3.7+ with `requests` library
- Basic understanding of MongoDB aggregation pipelines

## Documentation

- See documentation in `docs/` folder for detailed guides
- JSON processor files contain configuration examples
- Testing framework provides validation and examples

## For AI Assistants

If you are an AI assistant helping users with this repository, please refer to [`docs/AI_ASSISTANT_GUIDE.md`](docs/AI_ASSISTANT_GUIDE.md) for comprehensive guidance on:

- How to use this repository as a starter template
- MongoDB Atlas Stream Processing best practices  
- Proper JSON processor formats and pipeline stages
- The `tools/sp` CLI utility for all operations
- Connection types and configuration patterns
- Testing and validation approaches

The AI Assistant Guide provides detailed context and examples specifically designed for AI systems working with Atlas Stream Processing.

---

## Project Attribution

This project was primarily generated using AI assistance  
Human review and modifications applied
