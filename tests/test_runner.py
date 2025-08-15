#!/usr/bin/env python3
"""
Test Runner for Stream Processor Configurations
Quick validation script for processor JSON files
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

# Import colorize_json from the tools directory
sys.path.append(str(Path(__file__).parent.parent / "tools"))
try:
    from atlas_api import colorize_json
except ImportError:
    # Fallback if colorize_json is not available
    def colorize_json(data):
        return json.dumps(data, indent=2)


def validate_processor_file(file_path: Path) -> Dict:
    """Validate a single processor file"""
    result = {
        "file": str(file_path),
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    try:
        # Test 1: Valid JSON
        with open(file_path, 'r') as f:
            processor = json.load(f)
        
        # Test 2: Required fields
        if "pipeline" not in processor:
            result["errors"].append("Missing required 'pipeline' field")
            result["valid"] = False
        
        pipeline = processor.get("pipeline", [])
        if not isinstance(pipeline, list):
            result["errors"].append("'pipeline' must be a list")
            result["valid"] = False
        
        if len(pipeline) == 0:
            result["errors"].append("'pipeline' cannot be empty")
            result["valid"] = False
        
        # Test 3: First stage must be $source
        if pipeline and "$source" not in pipeline[0]:
            result["errors"].append("First pipeline stage must be '$source'")
            result["valid"] = False
        
        # Test 4: Check for output stage
        output_stages = ["$merge", "$emit"]
        has_output = any(
            any(stage_key in stage for stage_key in output_stages)
            for stage in pipeline
        )
        if not has_output:
            result["warnings"].append("No output stage found ($merge, $emit)")
        
        # Test 5: Check connection names exist
        connections = load_valid_connections()
        for stage in pipeline:
            if "$source" in stage and "connectionName" in stage["$source"]:
                conn = stage["$source"]["connectionName"]
                if conn not in connections:
                    result["warnings"].append(f"Unknown source connection: {conn}")
            
            if "$merge" in stage and "into" in stage["$merge"]:
                into = stage["$merge"]["into"]
                if isinstance(into, dict) and "connectionName" in into:
                    conn = into["connectionName"]
                    if conn not in connections:
                        result["warnings"].append(f"Unknown merge connection: {conn}")
            
            if "$emit" in stage:
                emit = stage["$emit"]
                if isinstance(emit, dict) and "connectionName" in emit:
                    conn = emit["connectionName"]
                    if conn not in connections:
                        result["warnings"].append(f"Unknown emit connection: {conn}")
        
        # Test 6: Naming convention
        filename = file_path.stem
        if "name" in processor and processor["name"] != filename:
            result["warnings"].append(f"Processor name '{processor['name']}' doesn't match filename '{filename}'")
    
    except json.JSONDecodeError as e:
        result["errors"].append(f"Invalid JSON: {e}")
        result["valid"] = False
    except Exception as e:
        result["errors"].append(f"Validation error: {e}")
        result["valid"] = False
    
    return result


def load_valid_connections() -> List[str]:
    """Load valid connection names"""
    try:
        connections_file = Path(__file__).parent.parent / "connections" / "connections.json"
        with open(connections_file, 'r') as f:
            data = json.load(f)
        
        if "connections" in data:
            return [conn["name"] for conn in data["connections"]]
        elif isinstance(data, list):
            return [conn["name"] for conn in data]
        else:
            return [data.get("name", "")]
    except:
        return ["sample_stream_solar", "kgShardedCluster01"]


def validate_all_processors() -> Dict:
    """Validate all processor files"""
    processors_dir = Path(__file__).parent.parent / "processors"
    processor_files = list(processors_dir.glob("*.json"))
    
    results = {
        "total": len(processor_files),
        "valid": 0,
        "invalid": 0,
        "files": []
    }
    
    for proc_file in processor_files:
        file_result = validate_processor_file(proc_file)
        results["files"].append(file_result)
        
        if file_result["valid"]:
            results["valid"] += 1
        else:
            results["invalid"] += 1
    
    return results


def print_results(results: Dict, verbose: bool = False):
    """Print validation results"""
    print(f"\nProcessor Validation Results")
    print(f"{'='*50}")
    print(f"Total files: {results['total']}")
    print(f"Valid: {results['valid']}")
    print(f"Invalid: {results['invalid']}")
    
    if results['invalid'] > 0:
        print(f"\nFiles with errors:")
        for file_result in results["files"]:
            if not file_result["valid"]:
                print(f"  • {Path(file_result['file']).name}")
                for error in file_result["errors"]:
                    print(f"    - ERROR: {error}")
    
    if verbose:
        print(f"\nWarnings:")
        has_warnings = False
        for file_result in results["files"]:
            if file_result["warnings"]:
                has_warnings = True
                print(f"  • {Path(file_result['file']).name}")
                for warning in file_result["warnings"]:
                    print(f"    - WARNING: {warning}")
        
        if not has_warnings:
            print("  No warnings found.")


def main():
    """Main function"""
    import argparse
    from datetime import datetime, timezone
    
    parser = argparse.ArgumentParser(description="Validates processor JSON files")
    parser.add_argument("-p", "--processor", help="Test specific processor only")
    args = parser.parse_args()
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    if args.processor:
        # Validate single processor
        processor_path = Path(__file__).parent.parent / "processors" / f"{args.processor}.json"
        if not processor_path.exists():
            error_result = {
                "timestamp": timestamp,
                "operation": "test",
                "success": False,
                "error": f"Processor file not found: {processor_path}",
                "processor": args.processor
            }
            print(colorize_json(error_result))
            sys.exit(1)
        
        result = validate_processor_file(processor_path)
        results = {
            "valid": 1 if result["valid"] else 0,
            "invalid": 0 if result["valid"] else 1,
            "total": 1,
            "files": [result]
        }
    else:
        # Validate all processors
        results = validate_all_processors()
    
    # Always return JSON format
    json_result = {
        "timestamp": timestamp,
        "operation": "test",
        "success": results["invalid"] == 0,
        "summary": {
            "total": results["total"],
            "valid": results["valid"],
            "invalid": results["invalid"]
        },
        "files": results["files"]
    }
    
    if args.processor:
        json_result["processor"] = args.processor
    
    print(colorize_json(json_result))
    
    # Exit with error code if any files are invalid
    sys.exit(0 if results["invalid"] == 0 else 1)


if __name__ == "__main__":
    main()
