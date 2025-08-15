# WeatherFlow Atlas Stream Processing Starter

A complete example and toolkit for building MongoDB Atlas Stream Processing applications. This repository provides a fully functional weather data processing system with lightning detection alerts, along with powerful command-line tools for managing stream processors and connections.

## What This Provides

- **Complete working example** of weather data ingestion and alert processing
- **Unified CLI tool** (`tools/sp`) for managing all Stream Processing operations
- **JSON-based configuration** for processors and connections
- **Color-coded terminal output** for easy debugging and monitoring
- **Production-ready structure** you can clone and customize for your own use cases

## Project Structure

```
weatherflow_atlas/
├── config.txt                 # Atlas API credentials and configuration
├── connections/               # Connection definitions (databases, APIs, etc.)
│   └── connections.json      
├── processors/               # Stream processor pipeline definitions
│   ├── lightning_alert_processor.json
│   └── weatherflow_source_client.json
└── tools/                   # Management utilities
    ├── sp                   # Unified CLI tool (executable)
    ├── atlas_api.py        # Core API library
    └── requirements.txt    # Python dependencies
```

## Quick Start

### Option A: Use This Repository

```bash
git clone <this-repo>
cd weatherflow_atlas
pip install -r tools/requirements.txt
cp config.txt.example config.txt
# Edit config.txt with your Atlas credentials
```

### Option B: Create New Repository from Scratch

Use the repository setup script to create a fresh structure:

```bash
# Download just the setup script
curl -O https://raw.githubusercontent.com/kgorman/weatherflow_atlas/main/tools/create-repo-structure.sh
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
      "name": "weatherflow_api",
      "type": "Https", 
      "url": "https://swd.weatherflow.com",
      "description": "WeatherFlow API for weather data"
    },
    {
      "name": "my_cluster",
      "type": "Cluster",
      "clusterName": "MyAtlasCluster",
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

- **weatherflow_http**: HTTP connection to WeatherFlow API
- **kgShardedCluster01**: MongoDB Atlas cluster for data storage

## Stream Processing Pipelines

Stream processors are defined in JavaScript files using Terraform-like format:

### weatherflow_source_client.js
- Fetches data from WeatherFlow API every 5 minutes
- Processes and enriches weather observations
- Stores data in MongoDB Atlas cluster
- Handles errors via dead letter queue

### lightning_alert_processor.js

- Monitors for lightning activity
- Stores alerts in database for dangerous conditions
- Tracks lightning strike counts and distances

## Management Tools

The `tools/` directory contains Python utilities for managing the Atlas Stream Processing environment:

- **create_connections.py**: Creates and configures connections
- **create_processors.py**: Deploys processor pipelines from JavaScript files
- **control_processors.py**: Start, stop, monitor, and control processors
- **atlas_api.py**: Shared library for Atlas API operations

## Features

- **Real-time Processing**: Continuous weather data ingestion and processing
- **Lightning Alerts**: Automated database alerts for lightning activity
- **Error Handling**: Dead letter queues and comprehensive error handling
- **Monitoring**: Detailed statistics and status monitoring
- **Configuration-Driven**: JSON-based configuration for easy management
- **Color-Coded Output**: User-friendly terminal output with status indicators

## Prerequisites

- MongoDB Atlas account with Stream Processing enabled
- WeatherFlow API access
- Python 3.7+ with `requests` library

## Documentation

- See `tools/README.md` for detailed tool documentation
- JavaScript pipeline files contain inline documentation
- Configuration files include examples and variable substitution
3. **Call WeatherFlow API** - HTTP stage fetches real weather station data
4. **Store historical data** - Weather data is merged into MongoDB Atlas with full history

## Architecture

```
Sample Solar Stream → 5-min Window → HTTP API Call → Data Transform → MongoDB Atlas
       ↓                   ↓              ↓             ↓              ↓
   Timer Trigger      Frequency       WeatherFlow    Structure       weather_history
  (data discarded)     Control          API Call      & Enrich        Collection
```

## Files

- **`weatherflow_cron_processor.js`** - Main stream processor implementation
- **`setup_weatherflow_connection.sh`** - Script to create HTTP connection via Atlas Admin API
- **`red_flag_warning.py`** - Python change stream processor (existing)
- **`requirements.txt`** - Python dependencies (existing)

## Setup Instructions

### 1. Prerequisites

- MongoDB Atlas cluster with Stream Processing enabled
- Atlas Admin API key with Stream Processing permissions
- WeatherFlow API token and station ID (configured in `../client/kg_station.txt`)

### 2. Create HTTP Connection

First, set up the HTTP connection for the WeatherFlow API:

```bash
# Set your Atlas credentials
export ATLAS_PUBLIC_KEY="your_atlas_public_key"
export ATLAS_PRIVATE_KEY="your_atlas_private_key"
export ATLAS_PROJECT_ID="your_atlas_project_id"
export ATLAS_SP_INSTANCE_NAME="your_stream_processing_instance_name"

# Run the setup script
./setup_weatherflow_connection.sh
```

The script will:
- Validate your configuration
- Test WeatherFlow API connectivity
- Create the `weatherflow_api` HTTP connection in Atlas

### 3. Deploy Stream Processor

Deploy the stream processor using the Atlas UI or MongoDB Shell:

```javascript
// In MongoDB Shell connected to your Atlas cluster
load("weatherflow_cron_processor.js")
```

### 4. Start Processing

```javascript
// Start the processor
sp.weatherflow_cron_fetcher.start()

// Check status
sp.weatherflow_cron_fetcher.stats()

// View recent data
db.weather_history.find().sort({processing_timestamp: -1}).limit(5)
```

## Configuration

### Station Configuration

The processor uses station configuration from `../client/kg_station.txt`:
- **Station ID**: 72117
- **API Token**: 23e0cb90-8a11-4ca5-871e-133ab69c47ae
- **Base URL**: https://swd.weatherflow.com/swd/rest/observations/station/

### Processing Frequency

The processor fetches data **every 5 minutes** controlled by the tumbling window:

```javascript
const timerWindow = {
    $tumblingWindow: {
        interval: { size: NumberInt(5), unit: "minute" },
        // ...
    }
};
```

To change frequency, modify the `interval.size` value.

### Output Collections

- **`demo.weather_history`** - Historical weather data with full station observations
- **`demo.weather_fetch_dlq`** - Dead letter queue for failed processing

## Data Structure

### Input (WeatherFlow API Response)
```json
{
  "station_id": 72117,
  "obs": [
    {
      "timestamp": 1642723200,
      "air_temperature": 15.2,
      "relative_humidity": 65,
      "wind_avg": 3.2,
      "lightning_strike_count": 0,
      // ... more fields
    }
  ],
  "station_name": "Station Name",
  "public_name": "Public Display Name",
  // ... station metadata
}
```

### Output (MongoDB Document)
```json
{
  "_id": ObjectId("..."),
  "station_id": "72117",
  "station_meta": {
    "station_name": "Station Name",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "elevation": 10
  },
  "source": "weatherflow_api",
  "processing_timestamp": ISODate("2025-01-15T10:30:00Z"),
  "fetch_trigger": {
    "triggerTime": "2025-01-15T10:25:00Z",
    "sampleCount": 143
  },
  "observations": { /* full observation object */ },
  "temperature": 15.2,
  "humidity": 65,
  "wind_speed": 3.2,
  "lightning_strike_count": 0,
  // ... structured weather fields
  "raw_response": { /* complete API response */ }
}
```

## Monitoring

### Check Processor Status
```javascript
// View processor statistics
sp.weatherflow_cron_fetcher.stats()

// View processor definition
sp.weatherflow_cron_fetcher.sample()
```

### Monitor Data Collection
```javascript
// Recent weather data
db.weather_history.find().sort({processing_timestamp: -1}).limit(10)

// Count by hour
db.weather_history.aggregate([
  {
    $group: {
      _id: {
        $dateToString: {
          format: "%Y-%m-%d %H:00",
          date: "$processing_timestamp"
        }
      },
      count: { $sum: 1 }
    }
  },
  { $sort: { _id: -1 } },
  { $limit: 24 }
])
```

### Check for Errors
```javascript
// View dead letter queue
db.weather_fetch_dlq.find().sort({_stream_meta.timestamp: -1})

// Count errors by type
db.weather_fetch_dlq.aggregate([
  {
    $group: {
      _id: "$errInfo.reason",
      count: { $sum: 1 }
    }
  }
])
```

## Integration with Existing System

This processor complements your existing weather system:

### Lightning Detection
The weather data can trigger your existing lightning detection logic:

```javascript
// Example trigger condition (add to processor)
const lightningCheck = {
  $match: {
    $or: [
      { "lightning_strike_count_last_1hr": { $gt: 2 } },
      { "lightning_strike_last_distance": { $lt: 20 } }
    ]
  }
};
```

### Red Flag Warning
Weather data feeds into your red flag warning calculations:

```javascript
// Example red flag conditions
const redFlagCheck = {
  $match: {
    $and: [
      { "humidity": { $lte: 15 } },
      { "wind_gust": { $gte: 25 } }
    ]
  }
};
```

## Troubleshooting

### Common Issues

1. **HTTP Connection Failed**
   - Verify Atlas Admin API credentials
   - Check Stream Processing instance name
   - Ensure proper permissions

2. **WeatherFlow API Errors**
   - Verify API token in `kg_station.txt`
   - Check station ID (72117)
   - Test API endpoint manually

3. **No Data in Collection**
   - Check processor status: `sp.weatherflow_cron_fetcher.stats()`
   - Verify sample solar stream is active
   - Check dead letter queue for errors

### Manual Testing

Test the WeatherFlow API directly:
```bash
curl "https://swd.weatherflow.com/swd/rest/observations/station/72117?token=23e0cb90-8a11-4ca5-871e-133ab69c47ae"
```

## Next Steps

1. **Add Lightning Processing**: Integrate with existing lightning alert system
2. **Add Red Flag Processing**: Enhance with stream processing red flag calculations  
3. **Add Aggregations**: Create hourly/daily weather summaries
4. **Add Multiple Stations**: Extend to support multiple WeatherFlow stations
5. **Add Alerting**: Implement stream-based weather alerts
