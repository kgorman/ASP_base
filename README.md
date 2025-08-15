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
atlas_stream_processing/
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

Defines external connections (databases, APIs, external services):

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

**Connection Types:**

- **Https**: External REST APIs
- **Cluster**: MongoDB Atlas clusters

**Variable Substitution**: Use `${VARIABLE_NAME}` to reference values from `config.txt`

### Processor Definitions (`processors/*.json`)

Each processor is a separate JSON file defining a stream processing pipeline:

```json
{
  "pipeline": [
    {
      "$source": {
        "connectionName": "sample_stream_solar",
        "timeField": {"$dateFromString": {"dateString": "$timestamp"}}
      }
    },
    {
      "$match": {
        "temperature": {"$gt": 90}
      }
    },
    {
      "$addFields": {
        "alert_message": "High temperature detected!",
        "alert_timestamp": "$$NOW"
      }
    },
    {
      "$merge": {
        "into": {
          "connectionName": "my_cluster",
          "db": "alerts",
          "coll": "temperature_alerts"
        }
      }
    }
  ],
  "options": {
    "dlq": {
      "connectionName": "my_cluster",
      "db": "errors", 
      "coll": "processor_errors"
    }
  }
}
```

**Pipeline Stages:**
- **$source**: Data input (database, sample data, etc.)
- **$match**: Filter documents
- **$addFields**: Add or modify fields
- **$merge**: Output to destination collections
- **$emit**: Output to streaming platforms
- **$https**: Call external APIs
- **$tumblingWindow**: Time-based aggregations

**Options:**
- **dlq**: Dead letter queue for failed messages

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

## MongoDB Stream Processing Resources

- [Atlas Stream Processing Documentation](https://www.mongodb.com/docs/atlas/stream-processing/)
- [Pipeline Stage Reference](https://www.mongodb.com/docs/atlas/stream-processing/pipeline-stages/)
- [Connection Types Guide](https://www.mongodb.com/docs/atlas/stream-processing/connections/)

## Troubleshooting

### Common Issues

**Config file not found:**
```bash
# The sp command automatically looks for config.txt in:
# 1. ../config.txt (from tools/ directory)
# 2. ./config.txt (from project root)
# 3. config.txt (current directory)
```

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

### Getting Help

1. Use `tools/sp --help` for command usage
2. Check the JSON output for detailed error messages
3. Review MongoDB Atlas Stream Processing logs in the UI
4. Validate your JSON files with a JSON formatter

## Next Steps

1. **Fork this repository** as your starting point
2. **Update the connections** to match your data sources  
3. **Customize the processors** for your use case
4. **Add new processors** as separate JSON files
5. **Deploy with confidence** using the `tools/sp` command

This repository provides everything you need to build production-ready stream processing applications on MongoDB Atlas. Happy streaming!
├── lightning_alert_processor.js    # Lightning detection and alert processor pipeline
└── tools/                          # Python management tools
    ├── atlas_api.py                # Shared Atlas API library
    ├── create_connections.py       # Connection creation tool
    ├── create_processors.py        # Processor creation tool
    ├── control_processors.py       # Processor control and monitoring tool
    └── README.md                   # Tools documentation
```

## Quick Start

1. **Configure credentials** in `api.txt`:
   ```
   PUBLIC_KEY=your_atlas_public_key
   PRIVATE_KEY=your_atlas_private_key
   PROJECT_ID=your_project_id
   SP_INSTANCE_NAME=your_stream_instance_name
   ```

2. **Create connections**:
   ```bash
   cd tools
   python3 create_connections.py
   ```

3. **Create processors**:
   ```bash
   python3 create_processors.py
   ```

4. **Monitor and control**:
   ```bash
   python3 control_processors.py status
   python3 control_processors.py stats
   ```

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

## Architecture

```
Sample Solar Stream → Data Processing → MongoDB Atlas / Stream Output
       ↓                   ↓                    ↓
   Built-in Sample     Transform &          Store or Emit
     Data Source       Add Timestamp        to External Systems
```

## Example Processors Included

### solar_simple_processor.json
- **Purpose**: Demonstrates basic data ingestion and storage pattern
- **Source**: Uses built-in sample solar data stream
- **Processing**: Adds timestamps and filters data
- **Output**: Merges data into MongoDB Atlas collection

### test_emit_processor.json  
- **Purpose**: Shows how to emit data to external systems
- **Source**: Uses built-in sample solar data stream
- **Processing**: Transforms and enriches data
- **Output**: Emits processed data to external topics/systems

## Getting Started

### 1. Clone and Setup

```bash
git clone <this-repo>
cd ASP_base
pip install -r tools/requirements.txt
cp config.txt.example config.txt
# Edit config.txt with your Atlas credentials
```

### 2. Test Your Setup

```bash
# Validate all processor configurations
./tools/sp test

# Test individual processor
./tools/sp test -p solar_simple_processor
```

### 3. Create Connections and Processors

```bash
# Create connections defined in connections.json
./tools/sp create connections

# Create processors from JSON files
./tools/sp create processors
```

### 4. Start Processing

```bash
# Start all processors
./tools/sp start

# Check processor status
./tools/sp list

# View detailed statistics
./tools/sp stats
```

## Configuration

## Customizing for Your Use Case

This template provides examples using sample solar data, but you can easily adapt it for any streaming use case:

### Update Connections
Edit `connections/connections.json` to define your data sources:

```json
{
  "connections": [
    {
      "name": "your_api_endpoint",
      "type": "Https",
      "url": "https://your-api.com/data",
      "description": "Your external API"
    },
    {
      "name": "your_cluster",
      "type": "Cluster", 
      "clusterName": "YourAtlasCluster",
      "description": "Your Atlas cluster"
    }
  ]
}
```

### Create Your Processors
Use the example processors as templates:

- **Data Ingestion**: Copy `solar_simple_processor.json` and modify the source and processing logic
- **Stream Output**: Copy `test_emit_processor.json` and change the emit destination
- **Complex Processing**: Add aggregation stages, filtering, and transformations

### Testing Your Changes
Always validate your processors before deployment:

```bash
# Test all processors
./tools/sp test

# Test specific processor
./tools/sp test -p your_new_processor

# Run comprehensive validation
cd tests && ./test_runner.py
```

## Use Case Examples

This template structure works well for:

### IoT Data Processing
- Sensor data ingestion and alerting
- Device status monitoring
- Real-time analytics

### E-commerce Analytics
- Order processing pipelines
- Customer behavior tracking
- Inventory management

### Financial Data
- Transaction monitoring
- Fraud detection
- Risk assessment

### Social Media Analytics
- Content processing
- Sentiment analysis
- User engagement tracking

## Customization Steps

### 1. Update Connections
Edit `connections/connections.json` with your data sources

### 2. Create Your Processors
Copy and modify the example processors

### 3. Modify Alert Logic
Implement your business logic in the pipeline stages

### 4. Deploy and Monitor
Use the unified `sp` tool to manage your processors

## Testing Framework

The repository includes comprehensive testing:

### Quick Validation
```bash
# Test all processors
./tools/sp test

# Test specific processor  
./tools/sp test -p processor_name
```

### Comprehensive Testing
```bash
# Run full test suite
cd tests && python test_processors.py

# Quick colorized output
cd tests && ./test_runner.py
```

## Common Issues

1. **Configuration Errors**
   - Verify your Atlas API keys have Stream Processing permissions
   - Check connection definitions in `connections.json`
   - Ensure processor names match file names

2. **JSON Validation Errors**  
   - Use the test framework to validate syntax
   - Ensure JSON syntax is valid
   - Check that all required fields are present

3. **Connection Issues**
   - Verify Atlas cluster is accessible
   - Check API endpoints are reachable
   - Test authentication credentials

## Next Steps

Start building your stream processing application:

1. **Fork this repository** for your project
2. **Update connections** with your data sources  
3. **Create processors** for your specific use case
4. **Test thoroughly** using the validation framework
5. **Deploy and monitor** with the unified CLI tools

This template provides everything you need to build robust, production-ready stream processing applications on MongoDB Atlas.
