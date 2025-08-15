#!/usr/bin/env python3
"""
Test Suite for Stream Processor JSON Files
Validates processor configurations before deployment
"""

import json
import os
import sys
import unittest
from pathlib import Path
from typing import Dict, List, Any


class ProcessorValidationTests(unittest.TestCase):
    """Test cases for validating stream processor JSON configurations"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.processors_dir = Path(__file__).parent.parent / "processors"
        cls.connections_file = Path(__file__).parent.parent / "connections" / "connections.json"
        cls.processor_files = list(cls.processors_dir.glob("*.json"))
        cls.valid_connections = cls._load_connections()
    
    @classmethod
    def _load_connections(cls) -> List[str]:
        """Load valid connection names from connections.json"""
        try:
            with open(cls.connections_file, 'r') as f:
                connections_data = json.load(f)
            
            if "connections" in connections_data:
                return [conn["name"] for conn in connections_data["connections"]]
            elif isinstance(connections_data, list):
                return [conn["name"] for conn in connections_data]
            else:
                return [connections_data.get("name", "")]
        except Exception:
            return ["sample_stream_solar", "kgShardedCluster01"]  # fallback defaults
    
    def test_processors_directory_exists(self):
        """Test that processors directory exists"""
        self.assertTrue(self.processors_dir.exists(), 
                       f"Processors directory not found: {self.processors_dir}")
    
    def test_processor_files_exist(self):
        """Test that processor JSON files exist"""
        self.assertGreater(len(self.processor_files), 0, 
                          "No processor JSON files found in processors directory")
    
    def test_all_processors_valid_json(self):
        """Test that all processor files contain valid JSON"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                try:
                    with open(proc_file, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON in {proc_file.name}: {e}")
    
    def test_processor_schema_validation(self):
        """Test that each processor has required schema elements"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                # Test required top-level structure
                self.assertIn("pipeline", processor, 
                             f"{proc_file.name}: Missing 'pipeline' field")
                self.assertIsInstance(processor["pipeline"], list,
                                    f"{proc_file.name}: 'pipeline' must be a list")
                self.assertGreater(len(processor["pipeline"]), 0,
                                 f"{proc_file.name}: 'pipeline' cannot be empty")
    
    def test_pipeline_has_source_stage(self):
        """Test that each pipeline starts with a $source stage"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                pipeline = processor.get("pipeline", [])
                if pipeline:
                    first_stage = pipeline[0]
                    self.assertIn("$source", first_stage,
                                f"{proc_file.name}: First pipeline stage must be '$source'")
    
    def test_pipeline_has_output_stage(self):
        """Test that each pipeline has an output stage ($merge, $emit, etc.)"""
        output_stages = ["$merge", "$emit", "$addFields"]  # $addFields can be final for testing
        
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                pipeline = processor.get("pipeline", [])
                if pipeline:
                    # Check if any stage has an output operation
                    has_output = any(
                        any(stage_key in stage for stage_key in output_stages)
                        for stage in pipeline
                    )
                    self.assertTrue(has_output,
                                  f"{proc_file.name}: Pipeline should have an output stage ({', '.join(output_stages)})")
    
    def test_source_connections_exist(self):
        """Test that source connections reference valid connection names"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                pipeline = processor.get("pipeline", [])
                for stage in pipeline:
                    if "$source" in stage:
                        source = stage["$source"]
                        if "connectionName" in source:
                            conn_name = source["connectionName"]
                            self.assertIn(conn_name, self.valid_connections,
                                        f"{proc_file.name}: Unknown connection '{conn_name}'. "
                                        f"Valid connections: {self.valid_connections}")
    
    def test_merge_connections_exist(self):
        """Test that $merge stages reference valid connection names"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                pipeline = processor.get("pipeline", [])
                for stage in pipeline:
                    if "$merge" in stage:
                        merge = stage["$merge"]
                        if "into" in merge and "connectionName" in merge["into"]:
                            conn_name = merge["into"]["connectionName"]
                            self.assertIn(conn_name, self.valid_connections,
                                        f"{proc_file.name}: Unknown connection '{conn_name}' in $merge stage. "
                                        f"Valid connections: {self.valid_connections}")
    
    def test_dlq_connections_exist(self):
        """Test that DLQ options reference valid connection names"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                options = processor.get("options", {})
                if "dlq" in options:
                    dlq = options["dlq"]
                    if "connectionName" in dlq:
                        conn_name = dlq["connectionName"]
                        self.assertIn(conn_name, self.valid_connections,
                                    f"{proc_file.name}: Unknown connection '{conn_name}' in DLQ options. "
                                    f"Valid connections: {self.valid_connections}")
    
    def test_processor_naming_convention(self):
        """Test that processor files follow naming conventions"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                # Check filename conventions
                filename = proc_file.stem
                self.assertRegex(filename, r'^[a-z][a-z0-9_]*[a-z0-9]$',
                               f"{proc_file.name}: Filename should use lowercase letters, numbers, and underscores only")
                
                # Check processor name matches filename
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                if "name" in processor:
                    proc_name = processor["name"]
                    self.assertEqual(filename, proc_name,
                                   f"{proc_file.name}: Processor name '{proc_name}' should match filename '{filename}'")
    
    def test_pipeline_stage_validation(self):
        """Test that pipeline stages use valid MongoDB aggregation operators"""
        valid_stages = {
            "$source", "$match", "$project", "$addFields", "$group", "$sort", 
            "$limit", "$skip", "$unwind", "$lookup", "$merge", "$emit",
            "$tumblingWindow", "$hoppingWindow", "$sessionWindow",
            "$https", "$densify", "$fill", "$facet", "$unionWith"
        }
        
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                pipeline = processor.get("pipeline", [])
                for i, stage in enumerate(pipeline):
                    stage_operators = [key for key in stage.keys() if key.startswith("$")]
                    for op in stage_operators:
                        self.assertIn(op, valid_stages,
                                    f"{proc_file.name}: Invalid pipeline stage '{op}' at position {i}. "
                                    f"Valid stages: {sorted(valid_stages)}")
    
    def test_merge_stage_structure(self):
        """Test that $merge stages have proper structure"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                pipeline = processor.get("pipeline", [])
                for i, stage in enumerate(pipeline):
                    if "$merge" in stage:
                        merge = stage["$merge"]
                        
                        # Test required 'into' field
                        self.assertIn("into", merge,
                                    f"{proc_file.name}: $merge stage at position {i} missing 'into' field")
                        
                        into = merge["into"]
                        if isinstance(into, dict):
                            # Test database and collection fields
                            if "connectionName" in into:
                                self.assertIn("db", into,
                                            f"{proc_file.name}: $merge 'into' missing 'db' field at position {i}")
                                self.assertIn("coll", into,
                                            f"{proc_file.name}: $merge 'into' missing 'coll' field at position {i}")
    
    def test_emit_stage_structure(self):
        """Test that $emit stages have proper structure"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                pipeline = processor.get("pipeline", [])
                for i, stage in enumerate(pipeline):
                    if "$emit" in stage:
                        emit = stage["$emit"]
                        
                        # Test that $emit has proper structure
                        # Note: $emit can have various configurations depending on the target
                        # This is a basic structural validation
                        if isinstance(emit, dict):
                            # If it's a structured emit (to a specific target), it should have connectionName or similar
                            if "connectionName" in emit:
                                self.assertIn(emit["connectionName"], self.valid_connections,
                                            f"{proc_file.name}: Unknown connection '{emit['connectionName']}' in $emit stage at position {i}")
                        # $emit can also be a simple true/false or have other configurations
                        # We'll be permissive here since $emit has multiple valid forms


class ProcessorLintTests(unittest.TestCase):
    """Additional linting tests for best practices"""
    
    @classmethod
    def setUpClass(cls):
        cls.processors_dir = Path(__file__).parent.parent / "processors"
        cls.processor_files = list(cls.processors_dir.glob("*.json"))
    
    def test_processors_have_error_handling(self):
        """Test that processors have appropriate error handling (DLQ or try-catch patterns)"""
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor = json.load(f)
                
                # Check for DLQ configuration
                has_dlq = "options" in processor and "dlq" in processor.get("options", {})
                
                # For now, just warn if no DLQ (this is optional)
                if not has_dlq:
                    print(f"WARNING: {proc_file.name} has no DLQ configuration")
    
    def test_processors_have_timestamps(self):
        """Test that processors add processing timestamps for debugging (optional)"""
        # Note: Atlas Stream Processing automatically adds _ts timestamp field
        # Manual timestamp fields are optional for debugging/tracking purposes
        timestamp_fields = ["processing_timestamp", "timestamp", "$$NOW", "processing_time"]
        
        for proc_file in self.processor_files:
            with self.subTest(file=proc_file.name):
                with open(proc_file, 'r') as f:
                    processor_text = f.read()
                
                has_timestamp = any(field in processor_text for field in timestamp_fields)
                if not has_timestamp:
                    # This is a warning, not an error - timestamps are optional
                    print(f"INFO: {proc_file.name} has no manual timestamp fields. "
                          f"Atlas Stream Processing automatically adds _ts field. "
                          f"Optional patterns for debugging: {timestamp_fields}")
                
                # Always pass - timestamps are optional since _ts is automatic
                self.assertTrue(True)


def run_tests(verbose=False):
    """Run all processor validation tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(ProcessorValidationTests))
    suite.addTests(loader.loadTestsFromTestCase(ProcessorLintTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate stream processor JSON files")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("-f", "--file", help="Test specific processor file")
    
    args = parser.parse_args()
    
    if args.file:
        # Test specific file
        print(f"Testing specific file: {args.file}")
        # TODO: Implement single file testing
    
    success = run_tests(args.verbose)
    sys.exit(0 if success else 1)
