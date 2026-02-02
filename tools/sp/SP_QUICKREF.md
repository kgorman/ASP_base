# SP - Quick Reference

**Location**: `tools/sp/sp` | **Dir**: Always `cd tools/sp/` first | **Output**: JSON

## Essential Commands

```bash
# ALWAYS navigate to tools/sp/ first
cd tools/sp/

# Testing (do this before deploying!)
./sp processors test                    # Test all processors
./sp processors test -p processor_name  # Test specific processor

# Deployment
./sp workspaces connections create      # Deploy connections
./sp processors create                  # Deploy all processors
./sp processors create -p name          # Deploy specific processor

# Monitoring
./sp processors list                    # List all with full details (pipeline, stats, errors)
./sp processors stats                   # Performance metrics (all)
./sp processors stats --processor name  # Metrics for specific processor
./sp processors stats --processor name --verbose  # Detailed pipeline stats

# Lifecycle
./sp processors start                   # Start all
./sp processors start -p name --auto    # Start specific with auto-wait
./sp processors start -p name -t SP30   # Start with specific tier
./sp processors stop                    # Stop all
./sp processors stop -p name            # Stop specific
./sp processors restart                 # Restart all
./sp processors restart -p name         # Restart specific

# Deletion (careful!)
./sp processors drop processor_name     # Delete specific processor
./sp processors drop --all              # Delete ALL processors

# Tier Management
./sp processors tier-advise -p name     # Get tier recommendation
./sp processors tier-advise --all       # Analyze all processors

# Performance Profiling
./sp processors profile -p name         # Profile specific processor
./sp processors profile --all           # Profile all processors
./sp processors profile -p name --duration 600 --interval 60
./sp processors profile --continuous    # Continuous monitoring

# Schema Discovery
./sp processors schema processor_name   # Sample output schema
./sp processors schema processor_name -n 5  # Sample 5 documents

# Workspace Management
./sp workspaces list                    # List workspaces
./sp workspaces create name --cloud-provider AWS --region US_EAST_1
./sp workspaces delete name             # Delete workspace
./sp workspaces details name            # Get workspace details

# Connection Management
./sp workspaces connections list        # List connections
./sp workspaces connections create      # Deploy connections
./sp workspaces connections delete name # Delete connection
./sp workspaces connections test        # Test connections

# Collection Management
./sp collections count database.collection    # Count documents
./sp collections query database.collection -l 100  # Query documents
./sp collections query database.collection -f '{"field":"value"}' -l 50  # With filter
./sp collections query database.collection -p '{"field":1}' -l 20  # With projection
./sp collections list database                # List collections
./sp collections ttl database.collection --seconds 3600 --field timestamp

# Materialized Views
./sp materialized_views create view_name --database demo --file processor.json
./sp materialized_views list                  # List all views
./sp materialized_views list --database demo  # List views in database
./sp materialized_views drop view_name --database demo
```

## Workflow Pattern

```bash
# 1. Create processor JSON in processors/ directory
# 2. Test configuration
cd tools/sp && ./sp processors test -p my_processor

# 3. Deploy processor
./sp processors create -p my_processor

# 4. Verify deployment
./sp processors list

# 5. Start processor (if needed)
./sp processors start -p my_processor --auto
```

## File Structure

```
project_root/
├── config.txt              # Atlas credentials (required)
├── connections/
│   └── connections.json    # Connection definitions
├── processors/
│   └── *.json             # Processor definitions
└── tools/
  Get tier advice | `cd tools/sp && ./sp processors tier-advise -p name` |
| Profile processor | `cd tools/sp && ./sp processors profile -p name` |
| Start all | `cd tools/sp && ./sp processors start` |
| Start with tier | `cd tools/sp && ./sp processors start -p name -t SP30` |
| Delete one | `cd tools/sp && ./sp processors drop processor_name` |
| Create materialized view | `cd tools/sp && ./sp materialized_views create my_view --file processor.json` |
| List collections | `cd tools/sp && ./sp collections list mydb` |
| Count documents | `cd tools/sp && ./sp collections count mydb.mycoll` |

## Advanced Features

### Performance Profiling
```bash
# Profile with custom settings
./sp processors profile -p processor_name \
  --duration 300 \
  --interval 30 \
  --metrics memory,latency,throughput \
  --output results.json

# Continuous monitoring with alerts
./sp processors profile --all \
  --continuous \
  --thresholds thresholds.json
```

### Tier Analysis
```bash
# Analyze complexity and get tier recommendation
./sp processors tier-advise -p processor_name

# Analyze all processors
./sp processors tier-advise --all
```

### Materialized Views
```bash
# Create view with processor
./sp materialized_views create sales_summary \
  --database analytics \
  --file sales_aggregation.json

# List views in database
./sp materialized_views list --database analytics

# Drop view and its processor
./sp materialized_views drop sales_summary --database analytics
```

## Output Format

All commands return JSON:
```json
{
  "timestamp": "2026-01-21T10:30:00Z",
  "operation": "create_processors",
  "summary": {"total": 2, "success": 2, "failed": 0},
  "processors": [{"name": "my_processor", "status": "created"}]
}
```

## AI Rules

✅ **DO**: `cd tools/sp && ./sp processors create`  
❌ **DON'T**: Manual API calls or skip the cd command

✅ **DO**: Test before deploying (`./sp processors test`)  
❌ **DON'T**: Deploy without testing

✅ **DO**: Use `./sp processors list` for status  
❌ **DON'T**: Write custom status scripts

## Common Tasks

| Task | Command |
|------|---------|
| Create processor | `cd tools/sp && ./sp processors test -p name && ./sp processors create -p name` |
| Deploy connections | `cd tools/sp && ./sp workspaces connections create` |
| Check status | `cd tools/sp && ./sp processors list` |
| Monitor performance | `cd tools/sp && ./sp processors stats` |
| Start all | `cd tools/sp && ./sp processors start` |
| Delete one | `cd tools/sp && ./sp processors drop processor_name` |

## Configuration

Create `config.txt` in project root:
```
PUBLIC_KEY=your_atlas_public_key
PRIVATE_KEY=your_atlas_private_key
PROJECT_ID=your_project_id
```

## Documentation

- Full Manual: `docs/SP_USER_MANUAL.md`
- AI Guide: `docs/SP_UTILITY_SUMMARY.md`
- Tool README: `tools/sp/README.md`
