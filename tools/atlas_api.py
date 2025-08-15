#!/usr/bin/env python3
"""
Shared Atlas Stream Processing API library
Common functionality for connection and processor management
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import requests
from requests.auth import HTTPDigestAuth


def colorize_json(obj):
    """Add color codes to JSON output for terminal display"""
    import json
    
    def colorize_value(value, indent=0):
        spaces = "  " * indent
        if isinstance(value, dict):
            if not value:
                return "{}"
            items = []
            for k, v in value.items():
                colored_key = f'\033[94m"{k}"\033[0m'  # Blue for keys
                colored_value = colorize_value(v, indent + 1)
                items.append(f"{spaces}  {colored_key}: {colored_value}")
            return "{\n" + ",\n".join(items) + f"\n{spaces}}}"
        elif isinstance(value, list):
            if not value:
                return "[]"
            items = []
            for item in value:
                colored_item = colorize_value(item, indent + 1)
                items.append(f"{spaces}  {colored_item}")
            return "[\n" + ",\n".join(items) + f"\n{spaces}]"
        elif isinstance(value, str):
            return f'\033[92m"{value}"\033[0m'  # Green for strings
        elif isinstance(value, (int, float)):
            return f'\033[93m{value}\033[0m'  # Yellow for numbers
        elif isinstance(value, bool):
            return f'\033[95m{str(value).lower()}\033[0m'  # Magenta for booleans
        elif value is None:
            return f'\033[90mnull\033[0m'  # Gray for null
        else:
            return str(value)
    
    return colorize_value(obj)


class AtlasStreamProcessingAPI:
    """Atlas Stream Processing API client with common operations"""
    
    def __init__(self, config_file: str = "../config.txt"):
        self.config = self._load_config(config_file)
        self.auth = HTTPDigestAuth(
            self.config["PUBLIC_KEY"], 
            self.config["PRIVATE_KEY"]
        )
        self.base_url = f"https://cloud.mongodb.com/api/atlas/v2/groups/{self.config['PROJECT_ID']}/streams/{self.config['SP_INSTANCE_NAME']}"
        self.headers = {"Accept": "application/vnd.atlas.2024-05-30+json"}
    
    def _load_config(self, config_file: str) -> Dict[str, str]:
        """Load configuration from api.txt file"""
        config = {}
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file {config_file} not found")
        
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        
        required_keys = ["PUBLIC_KEY", "PRIVATE_KEY", "PROJECT_ID", "SP_INSTANCE_NAME"]
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")
        
        return config
    
    def _substitute_variables(self, text: str) -> str:
        """Substitute ${VAR} placeholders with config values"""
        def replace_var(match):
            var_name = match.group(1)
            return self.config.get(var_name, match.group(0))
        
        return re.sub(r'\$\{([^}]+)\}', replace_var, text)
    
    # Processor Operations
    def list_processors(self) -> List[Dict]:
        """Get list of all processors"""
        response = requests.get(
            f"{self.base_url}/processors",
            auth=self.auth,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json().get("results", [])
    
    def get_processor_status(self) -> Dict:
        """Get status of all processors"""
        timestamp = datetime.now(timezone.utc).isoformat()
        result = {
            "timestamp": timestamp,
            "operation": "status",
            "summary": {"total": 0, "success": 0, "failed": 0},
            "processors": []
        }
        
        try:
            processors = self.list_processors()
            result["summary"]["total"] = len(processors)
            
            for processor in processors:
                proc_info = {
                    "name": processor["name"],
                    "operation": "status",
                    "status": processor.get("state", "UNKNOWN"),
                    "message": "Status retrieved successfully"
                }
                result["processors"].append(proc_info)
                result["summary"]["success"] += 1
                
        except requests.RequestException as e:
            result["summary"]["failed"] = 1
            result["processors"].append({
                "name": "API_ERROR",
                "operation": "status",
                "status": "ERROR",
                "message": str(e)
            })
        
        return result
    
    def get_processor_stats(self) -> Dict:
        """Get detailed stats of all processors"""
        timestamp = datetime.now(timezone.utc).isoformat()
        result = {
            "timestamp": timestamp,
            "operation": "stats",
            "summary": {"total": 0, "success": 0, "failed": 0},
            "processors": []
        }
        
        try:
            processors = self.list_processors()
            result["summary"]["total"] = len(processors)
            
            for processor in processors:
                stats = processor.get("stats", {})
                proc_info = {
                    "name": processor["name"],
                    "operation": "stats",
                    "status": processor.get("state", "UNKNOWN"),
                    "message": "Stats retrieved successfully",
                    "stats": {
                        "processor": processor["name"],
                        "state": processor.get("state", "UNKNOWN"),
                        "inputMessageCount": stats.get("inputMessageCount", 0),
                        "outputMessageCount": stats.get("outputMessageCount", 0),
                        "dlqMessageCount": stats.get("dlqMessageCount", 0),
                        "memoryUsageBytes": stats.get("memoryUsageBytes", 0),
                        "lastMessageIn": stats.get("lastMessageIn"),
                        "scaleFactor": stats.get("scaleFactor", 1)
                    }
                }
                result["processors"].append(proc_info)
                result["summary"]["success"] += 1
                
        except requests.RequestException as e:
            result["summary"]["failed"] = 1
            result["processors"].append({
                "name": "API_ERROR",
                "operation": "stats",
                "status": "ERROR",
                "message": str(e)
            })
        
        return result
    
    def get_single_processor_status(self, processor_name: str) -> Dict:
        """Get status of a specific processor"""
        timestamp = datetime.now(timezone.utc).isoformat()
        result = {
            "timestamp": timestamp,
            "operation": "status",
            "summary": {"total": 1, "success": 0, "failed": 0},
            "processors": []
        }
        
        try:
            processors = self.list_processors()
            target_processor = None
            
            for processor in processors:
                if processor["name"] == processor_name:
                    target_processor = processor
                    break
            
            if target_processor:
                proc_info = {
                    "name": processor_name,
                    "operation": "status",
                    "status": target_processor.get("state", "UNKNOWN"),
                    "message": "Status retrieved successfully"
                }
                result["processors"].append(proc_info)
                result["summary"]["success"] = 1
            else:
                result["processors"].append({
                    "name": processor_name,
                    "operation": "status",
                    "status": "NOT_FOUND",
                    "message": f"Processor '{processor_name}' not found"
                })
                result["summary"]["failed"] = 1
                
        except requests.RequestException as e:
            result["summary"]["failed"] = 1
            result["processors"].append({
                "name": processor_name,
                "operation": "status",
                "status": "ERROR",
                "message": str(e)
            })
        
        return result
    
    def get_single_processor_stats(self, processor_name: str) -> Dict:
        """Get detailed stats of a specific processor"""
        timestamp = datetime.now(timezone.utc).isoformat()
        result = {
            "timestamp": timestamp,
            "operation": "stats",
            "summary": {"total": 1, "success": 0, "failed": 0},
            "processors": []
        }
        
        try:
            processors = self.list_processors()
            target_processor = None
            
            for processor in processors:
                if processor["name"] == processor_name:
                    target_processor = processor
                    break
            
            if target_processor:
                stats = target_processor.get("stats", {})
                proc_info = {
                    "name": processor_name,
                    "operation": "stats",
                    "status": target_processor.get("state", "UNKNOWN"),
                    "message": "Stats retrieved successfully",
                    "stats": {
                        "processor": processor_name,
                        "state": target_processor.get("state", "UNKNOWN"),
                        "inputMessageCount": stats.get("inputMessageCount", 0),
                        "outputMessageCount": stats.get("outputMessageCount", 0),
                        "dlqMessageCount": stats.get("dlqMessageCount", 0),
                        "memoryUsageBytes": stats.get("memoryUsageBytes", 0),
                        "lastMessageIn": stats.get("lastMessageIn"),
                        "scaleFactor": stats.get("scaleFactor", 1)
                    }
                }
                result["processors"].append(proc_info)
                result["summary"]["success"] = 1
            else:
                result["processors"].append({
                    "name": processor_name,
                    "operation": "stats",
                    "status": "NOT_FOUND",
                    "message": f"Processor '{processor_name}' not found"
                })
                result["summary"]["failed"] = 1
                
        except requests.RequestException as e:
            result["summary"]["failed"] = 1
            result["processors"].append({
                "name": processor_name,
                "operation": "stats",
                "status": "ERROR",
                "message": str(e)
            })
        
        return result
    
    def start_processor(self, processor_name: str) -> Dict:
        """Start a specific processor"""
        try:
            response = requests.post(
                f"{self.base_url}/processor/{processor_name}:start",
                auth=self.auth,
                headers=self.headers
            )
            response.raise_for_status()
            return {
                "name": processor_name,
                "operation": "start",
                "status": "started",
                "message": "Started successfully"
            }
        except requests.RequestException as e:
            return {
                "name": processor_name,
                "operation": "start",
                "status": "failed",
                "message": str(e),
                "http_code": getattr(e.response, 'status_code', None)
            }
    
    def stop_processor(self, processor_name: str) -> Dict:
        """Stop a specific processor"""
        try:
            response = requests.post(
                f"{self.base_url}/processor/{processor_name}:stop",
                auth=self.auth,
                headers=self.headers
            )
            response.raise_for_status()
            return {
                "name": processor_name,
                "operation": "stop",
                "status": "stopped",
                "message": "Stopped successfully"
            }
        except requests.RequestException as e:
            return {
                "name": processor_name,
                "operation": "stop",
                "status": "failed",
                "message": str(e),
                "http_code": getattr(e.response, 'status_code', None)
            }
    
    def create_processor(self, name: str, pipeline_file: str) -> Dict:
        """Create a processor from a JavaScript pipeline file"""
        try:
            # Read the pipeline from file
            pipeline_path = Path(pipeline_file)
            if not pipeline_path.exists():
                return {
                    "name": name,
                    "file": pipeline_file,
                    "operation": "create_processor",
                    "status": "failed",
                    "message": f"Pipeline file '{pipeline_file}' not found"
                }
            
            with open(pipeline_path, 'r') as f:
                pipeline_code = f.read()
            
            # First try to delete existing processor (idempotent)
            try:
                requests.delete(
                    f"{self.base_url}/processor/{name}",
                    auth=self.auth,
                    headers=self.headers
                )
            except requests.RequestException:
                pass  # Ignore delete errors
            
            # Create the processor
            payload = {
                "name": name,
                "pipeline": pipeline_code
            }
            response = requests.post(
                f"{self.base_url}/processor",
                auth=self.auth,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            return {
                "name": name,
                "file": pipeline_file,
                "operation": "create_processor",
                "status": "created",
                "message": "Processor created successfully"
            }
            
        except requests.RequestException as e:
            return {
                "name": name,
                "file": pipeline_file,
                "operation": "create_processor",
                "status": "failed",
                "message": str(e),
                "http_code": getattr(e.response, 'status_code', None)
            }

    def create_processor_from_content(self, name: str, pipeline_content: str) -> Dict:
        """Create a processor from pipeline content string"""
        try:
            # First try to delete existing processor (idempotent)
            try:
                requests.delete(
                    f"{self.base_url}/processor/{name}",
                    auth=self.auth,
                    headers=self.headers
                )
            except requests.RequestException:
                pass  # Ignore delete errors
            
            # Parse the JavaScript content to extract pipeline and options
            parsed_content = self._parse_js_processor_content(pipeline_content)
            
            # Create the processor with the correct payload format
            payload = {
                "name": name,
                "pipeline": parsed_content["pipeline"]
            }
            
            # Add options if they exist (like dlq configuration)
            if "options" in parsed_content:
                payload["options"] = parsed_content["options"]
            
            response = requests.post(
                f"{self.base_url}/processor",
                auth=self.auth,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            return {
                "name": name,
                "operation": "create_processor",
                "status": "created",
                "message": "Processor created successfully"
            }
            
        except requests.RequestException as e:
            return {
                "name": name,
                "operation": "create_processor",
                "status": "failed",
                "message": str(e),
                "http_code": getattr(e.response, 'status_code', None)
            }
        except Exception as e:
            return {
                "name": name,
                "operation": "create_processor",
                "status": "failed",
                "message": f"Parse error: {str(e)}"
            }

    def _parse_js_processor_content(self, content: str) -> Dict:
        """Parse JavaScript processor content and convert to JSON format"""
        import json
        import re
        
        # Remove comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        
        # Find the main object - look for { ... } that contains name and pipeline
        # This is a simple approach that works for our Terraform-like format
        
        # Extract pipeline array - find pipeline: [...] 
        pipeline_match = re.search(r'pipeline:\s*(\[.*?\])', content, re.DOTALL)
        if not pipeline_match:
            raise ValueError("Could not find pipeline array in JavaScript content")
        
        pipeline_str = pipeline_match.group(1)
        
        # Convert JavaScript object syntax to JSON
        # Replace unquoted property names with quoted ones
        pipeline_str = re.sub(r'(\w+):', r'"\1":', pipeline_str)
        # Handle special MongoDB operators that start with $
        pipeline_str = re.sub(r'"(\$\w+)":', r'"\1":', pipeline_str)
        
        try:
            pipeline = json.loads(pipeline_str)
        except json.JSONDecodeError as e:
            # If direct JSON parsing fails, try a more sophisticated approach
            # For now, return the original error
            raise ValueError(f"Could not parse pipeline as JSON: {str(e)}")
        
        result = {"pipeline": pipeline}
        
        # Look for options like dlq configuration
        dlq_match = re.search(r'dlq:\s*(\{[^}]+\})', content)
        if dlq_match:
            dlq_str = dlq_match.group(1)
            # Convert to JSON format
            dlq_str = re.sub(r'(\w+):', r'"\1":', dlq_str)
            try:
                dlq_config = json.loads(dlq_str)
                result["options"] = {"dlq": dlq_config}
            except json.JSONDecodeError:
                pass  # Ignore DLQ parsing errors for now
        
        return result

    def create_processor_from_json(self, name: str, pipeline: List[Dict], options: Dict = None) -> Dict:
        """Create a processor from JSON pipeline data"""
        try:
            # First try to delete existing processor (idempotent)
            try:
                requests.delete(
                    f"{self.base_url}/processor/{name}",
                    auth=self.auth,
                    headers=self.headers
                )
            except requests.RequestException:
                pass  # Ignore delete errors
            
            # Create the processor with the correct payload format
            payload = {
                "name": name,
                "pipeline": pipeline
            }
            
            # Add options if they exist (like dlq configuration)
            if options:
                payload["options"] = options
            
            response = requests.post(
                f"{self.base_url}/processor",
                auth=self.auth,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            return {
                "name": name,
                "operation": "create_processor",
                "status": "created",
                "message": "Processor created successfully"
            }
            
        except requests.RequestException as e:
            return {
                "name": name,
                "operation": "create_processor",
                "status": "failed",
                "message": str(e),
                "http_code": getattr(e.response, 'status_code', None)
            }

    def delete_processor(self, processor_name: str) -> Dict:
        """Delete a processor by name"""
        try:
            # Use the correct endpoint format from MongoDB documentation
            # DELETE /api/atlas/v2/groups/{groupId}/streams/{tenantName}/processor/{processorName}
            response = requests.delete(
                f"{self.base_url}/processor/{processor_name}",
                auth=self.auth,
                headers=self.headers
            )
            response.raise_for_status()
            
            return {
                "name": processor_name,
                "operation": "delete_processor",
                "status": "deleted",
                "message": "Processor deleted successfully"
            }
            
        except requests.RequestException as e:
            return {
                "name": processor_name,
                "operation": "delete_processor",
                "status": "failed",
                "message": str(e),
                "http_code": getattr(e.response, 'status_code', None)
            }
    
    # Connection Operations
    def list_connections(self) -> List[Dict]:
        """Get list of all connections"""
        response = requests.get(
            f"{self.base_url}/connections",
            auth=self.auth,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json().get("results", [])
    
    def create_http_connection(self, name: str, url: str) -> Dict:
        """Create an HTTP connection"""
        try:
            payload = {
                "name": name,
                "type": "Https",
                "url": url
            }
            response = requests.post(
                f"{self.base_url}/connections",
                auth=self.auth,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return {
                "name": name,
                "type": "Https",
                "url": url,
                "operation": "create_connection",
                "status": "created",
                "message": "HTTP connection created successfully"
            }
        except requests.RequestException as e:
            status_code = getattr(e.response, 'status_code', None)
            if status_code == 409:
                return {
                    "name": name,
                    "type": "Https", 
                    "url": url,
                    "operation": "create_connection",
                    "status": "already_exists",
                    "message": "HTTP connection already exists"
                }
            return {
                "name": name,
                "type": "Https",
                "url": url,
                "operation": "create_connection",
                "status": "failed",
                "message": str(e),
                "http_code": status_code
            }
    
    def create_cluster_connection(self, name: str, cluster_name: str) -> Dict:
        """Create a MongoDB cluster connection"""
        try:
            payload = {
                "name": name,
                "type": "Cluster",
                "clusterName": cluster_name
            }
            response = requests.post(
                f"{self.base_url}/connections",
                auth=self.auth,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return {
                "name": name,
                "type": "Cluster",
                "clusterName": cluster_name,
                "operation": "create_connection",
                "status": "created",
                "message": "Cluster connection created successfully"
            }
        except requests.RequestException as e:
            status_code = getattr(e.response, 'status_code', None)
            if status_code == 409:
                return {
                    "name": name,
                    "type": "Cluster",
                    "clusterName": cluster_name,
                    "operation": "create_connection",
                    "status": "already_exists",
                    "message": "Cluster connection already exists"
                }
            return {
                "name": name,
                "type": "Cluster",
                "clusterName": cluster_name,
                "operation": "create_connection",
                "status": "failed",
                "message": str(e),
                "http_code": status_code
            }



def main():
    """Command line interface for Atlas API operations"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Atlas Stream Processing API CLI")
    parser.add_argument("command", choices=["list", "stats", "delete", "start", "stop"], 
                       help="Command to execute")
    parser.add_argument("processor_name", nargs="?", help="Processor name for delete/start/stop commands")
    parser.add_argument("--config", default="../config.txt", help="API configuration file")
    
    args = parser.parse_args()
    
    try:
        api = AtlasStreamProcessingAPI(args.config)
        
        if args.command == "list":
            result = api.get_processor_status()
            print(colorize_json(result))
        elif args.command == "stats":
            result = api.get_processor_stats()
            print(colorize_json(result))
        elif args.command == "delete":
            if not args.processor_name:
                print(colorize_json({"error": "Processor name required for delete command"}))
                sys.exit(1)
            result = api.delete_processor(args.processor_name)
            print(colorize_json(result))
        elif args.command == "start":
            if not args.processor_name:
                print(colorize_json({"error": "Processor name required for start command"}))
                sys.exit(1)
            result = api.start_processor(args.processor_name)
            print(colorize_json(result))
        elif args.command == "stop":
            if not args.processor_name:
                print(colorize_json({"error": "Processor name required for stop command"}))
                sys.exit(1)
            result = api.stop_processor(args.processor_name)
            print(colorize_json(result))
            
    except Exception as e:
        error_result = {"error": str(e)}
        print(colorize_json(error_result))
        sys.exit(1)


if __name__ == "__main__":
    main()
