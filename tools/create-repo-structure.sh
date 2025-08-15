#!/bin/bash
#
# create-repo-structure.sh
# Creates the complete WeatherFlow Atlas Stream Processing repository structure
# Use this script to set up a new repository with the proper directory layout and template files
#

set -e  # Exit on any error

echo "Creating WeatherFlow Atlas Stream Processing Repository Structure"
echo "=================================================================="

# Get the target directory (default to current directory)
TARGET_DIR="${1:-.}"

# Create target directory if it doesn't exist
if [ "$TARGET_DIR" != "." ]; then
    mkdir -p "$TARGET_DIR"
fi

cd "$TARGET_DIR"

# Create directory structure
echo "Creating directory structure..."
mkdir -p connections
mkdir -p processors
mkdir -p docs
mkdir -p tools
mkdir -p stream_processing

# Create configuration templates
echo "Creating configuration templates..."

# Main config.txt.example
cat > config.txt.example << 'EOF'
# MongoDB Atlas API Credentials
# Get these from Atlas UI → Access Manager → API Keys
PUBLIC_KEY=your_atlas_public_key_here
PRIVATE_KEY=your_atlas_private_key_here

# Atlas Project Information  
# Get from Atlas UI → Project Settings → General
PROJECT_ID=your_atlas_project_id_here

# Stream Processing Instance Name
# Get from Atlas UI → Stream Processing → Your instance name
SP_INSTANCE_NAME=your_stream_processing_instance_name_here

# HTTP Connection Details
HTTP_CONNECTION_NAME=weatherflow_api
WEATHERFLOW_URL=https://swd.weatherflow.com/swd/rest/observations/station/72117
CLUSTER_NAME=YourAtlasClusterName

# Target Database Configuration
TARGET_DATABASE=weather
TARGET_COLLECTION=weatherflow_stream
EOF

# Create connections template
echo "Creating connections template..."
cat > connections/connections.json << 'EOF'
{
  "connections": [
    {
      "name": "sample_stream_solar",
      "type": "Sample",
      "description": "Sample solar data stream for testing"
    },
    {
      "name": "your_atlas_cluster",
      "type": "Cluster", 
      "clusterName": "YourAtlasClusterName",
      "description": "MongoDB Atlas cluster connection for data storage"
    }
  ]
}
EOF

# Create example processor
echo "Creating example processor..."
cat > processors/example_data_ingestion.json << 'EOF'
{
    "name": "example_data_ingestion",
    "pipeline": [
        {
            "$source": {
                "connectionName": "sample_stream_solar",
                "timeField": { "$dateFromString": { "dateString": "$timestamp" }}
            }
        },
        {
            "$addFields": {
                "processing_timestamp": "$$NOW",
                "processor_name": "example_data_ingestion",
                "data_source": "sample"
            }
        },
        {
            "$merge": {
                "into": {
                    "connectionName": "your_atlas_cluster",
                    "db": "raw_data",
                    "coll": "ingested_records"
                },
                "whenNotMatched": "insert"
            }
        }
    ],
    "options": {
        "dlq": {
            "connectionName": "your_atlas_cluster",
            "db": "errors",
            "coll": "processor_dlq"
        }
    }
}
EOF

# Copy tools if they don't exist
echo "Setting up tools..."
if [ ! -f "tools/atlas_api.py" ]; then
    echo "Note: atlas_api.py not found - you'll need to copy it from the original repository"
fi

if [ ! -f "tools/sp" ]; then
    echo "Note: sp CLI tool not found - you'll need to copy it from the original repository"
fi

# Create requirements.txt for tools
cat > tools/requirements.txt << 'EOF'
requests>=2.25.0
EOF

# Create documentation
echo "Creating documentation..."

# AI Assistant Guide
cat > docs/AI_ASSISTANT_GUIDE.md << 'EOF'
# AI Assistant Guide for MongoDB Atlas Stream Processing

This document provides AI systems with comprehensive guidance for using this repository to build MongoDB Atlas Stream Processing applications.

## 🎯 Repository Purpose

This is a **complete starter template** for MongoDB Atlas Stream Processing that AI systems should use to:

1. **Generate functional stream processors** based on user requirements
2. **Create proper JSON pipeline definitions** following MongoDB best practices
3. **Set up connections** to external data sources and sinks
4. **Provide working management tools** for deployment and monitoring

## 📚 Essential Reference Materials

### Official MongoDB Documentation
Always reference the most current documentation at:
- **Main Docs**: https://www.mongodb.com/docs/atlas/atlas-stream-processing/overview/
- **Pipeline Stages**: https://www.mongodb.com/docs/atlas/atlas-stream-processing/pipeline-stages/
- **Connection Types**: https://www.mongodb.com/docs/atlas/atlas-stream-processing/connections/

### MongoDB Example Repository
Reference the official examples at:
- **ASP Examples**: https://github.com/mongodb/asp_example
- **Code Snippets**: https://github.com/mongodb/asp_example/tree/main/code_snipplets
- **Example Processors**: https://github.com/mongodb/asp_example/tree/main/example_processors

## 🏗️ Repository Architecture Understanding

### Core Components

1. **`config.txt`** - Atlas API credentials and project configuration
2. **`connections/`** - External service connection definitions  
3. **`processors/`** - JSON-based stream processor pipeline definitions
4. **`tools/sp`** - Unified CLI for deployment and management

### Key Design Principles

1. **JSON-First**: All processors are defined in pure JSON format
2. **Declarative**: Configuration-driven approach with minimal code
3. **Tooling-Integrated**: Complete lifecycle management through CLI
4. **Production-Ready**: Includes error handling, DLQ, and monitoring

## 🔧 Stream Processor JSON Format

### Required Structure
```json
{
  "pipeline": [
    {
      "$source": {
        "connectionName": "data_source_connection",
        "timeField": {"$dateFromString": {"dateString": "$timestamp"}}
      }
    },
    // ... processing stages ...
    {
      "$merge": {
        "into": {
          "connectionName": "destination_connection",
          "db": "database_name", 
          "coll": "collection_name"
        }
      }
    }
  ],
  "options": {
    "dlq": {
      "connectionName": "error_connection",
      "db": "errors",
      "coll": "processor_errors"
    }
  }
}
```

Always refer to the official MongoDB documentation for the latest pipeline stage syntax and available operators.
EOF

# Create main README
echo "Creating main README..."
cat > README.md << 'EOF'
# MongoDB Atlas Stream Processing Template

A complete starter template for MongoDB Atlas Stream Processing with working examples, unified CLI tools, and comprehensive documentation.

## 🚀 Quick Start

### 1. Repository Setup

If you're starting fresh, use the setup script:

```bash
# Create new repository structure
./tools/create-repo-structure.sh

# Or create in a specific directory  
./tools/create-repo-structure.sh /path/to/new/repo
```

### 2. Configuration

1. Copy the configuration template:
   ```bash
   cp config.txt.example config.txt
   ```

2. Edit `config.txt` with your Atlas credentials:
   ```bash
   # Get these from Atlas UI → Access Manager → API Keys
   PUBLIC_KEY=your_atlas_public_key_here
   PRIVATE_KEY=your_atlas_private_key_here
   PROJECT_ID=your_atlas_project_id_here  
   SP_INSTANCE_NAME=your_stream_processing_instance_name_here
   ```

### 3. Install Dependencies

```bash
cd tools
pip install -r requirements.txt
```

### 4. Deploy and Test

```bash
# Create connections
./tools/sp create connections

# Create processors
./tools/sp create processors

# Check status
./tools/sp list

# Start processors  
./tools/sp start
```

## 📁 Repository Structure

```
├── config.txt.example          # Atlas API credentials template
├── connections/                 # Connection definitions
│   └── connections.json        # Atlas clusters, APIs, sample data
├── processors/                  # Stream processor definitions
│   └── *.json                  # JSON pipeline definitions
├── tools/                       # Management utilities
│   ├── sp                      # Unified CLI tool
│   ├── atlas_api.py           # Core API library
│   ├── requirements.txt       # Python dependencies
│   └── create-repo-structure.sh # Repository setup script
└── docs/                        # Documentation
    └── AI_ASSISTANT_GUIDE.md   # AI development guidance
```

## 🛠️ Tools Usage

### SP CLI Tool

The `sp` tool provides unified management for your stream processing workflows:

```bash
# Connection management
./tools/sp create connections     # Deploy all connections

# Processor management
./tools/sp create processors      # Deploy all processors
./tools/sp list                   # Show processor status
./tools/sp stats                  # Show detailed statistics
./tools/sp start                  # Start all processors
./tools/sp stop                   # Stop all processors
./tools/sp restart                # Restart all processors

# Configuration
./tools/sp --config /path/to/config.txt list
```

### Repository Setup Script

Use `create-repo-structure.sh` to bootstrap new repositories:

```bash
# Create structure in current directory
./tools/create-repo-structure.sh

# Create structure in new directory
./tools/create-repo-structure.sh /path/to/new/weatherflow-project

# What it creates:
# - Complete directory structure
# - Configuration templates  
# - Example connections and processors
# - Documentation templates
# - Tool requirements
```

## 🔗 Connections

Define external data sources in `connections/connections.json`:

```json
{
  "connections": [
    {
      "name": "my_api",
      "type": "Https", 
      "url": "https://api.example.com"
    },
    {
      "name": "my_cluster",
      "type": "Cluster",
      "clusterName": "MyAtlasCluster"
    }
  ]
}
```

## 🔄 Processors

Create stream processors as JSON files in `processors/`:

```json
{
  "name": "my_processor",
  "pipeline": [
    {
      "$source": {
        "connectionName": "my_api"
      }
    },
    {
      "$addFields": {
        "processed_at": "$$NOW"
      }
    },
    {
      "$merge": {
        "into": {
          "connectionName": "my_cluster",
          "db": "processed_data",
          "coll": "events"
        }
      }
    }
  ]
}
```

## 📚 Documentation

- **AI Assistant Guide**: `docs/AI_ASSISTANT_GUIDE.md` - Comprehensive guidance for AI systems
- **MongoDB Docs**: [Atlas Stream Processing](https://www.mongodb.com/docs/atlas/atlas-stream-processing/)
- **Examples**: [MongoDB ASP Examples](https://github.com/mongodb/asp_example)

## 🎯 Key Features

- **JSON-First Architecture**: Pure JSON processor definitions
- **Unified CLI**: Single tool for all operations
- **Smart Configuration**: Variable substitution and path detection
- **Production Ready**: Error handling, DLQ, monitoring
- **AI Optimized**: Comprehensive documentation for AI assistants

## 🔧 Development Workflow

1. **Design** your data flow and processing logic
2. **Define connections** in `connections/connections.json`
3. **Create processors** as JSON files in `processors/`
4. **Deploy** using `./tools/sp create connections` and `./tools/sp create processors`
5. **Monitor** with `./tools/sp list` and `./tools/sp stats`

This template provides everything you need to build production-ready stream processing applications with MongoDB Atlas.
EOF

# Create .gitignore
echo "Creating .gitignore..."
cat > .gitignore << 'EOF'
# Configuration files with secrets
config.txt
token.txt

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
EOF

echo ""
echo "Repository structure created successfully!"
echo ""
echo "Next steps:"
echo "1. Copy config.txt.example to config.txt and add your Atlas credentials"
echo "2. Copy the tools (atlas_api.py, sp) from an existing repository if needed"
echo "3. Run: cd tools && pip install -r requirements.txt"
echo "4. Test with: ./tools/sp list"
echo ""
echo "Created structure:"
tree 2>/dev/null || find . -type d | sort
echo ""
echo "Ready to build MongoDB Atlas Stream Processing applications!"
