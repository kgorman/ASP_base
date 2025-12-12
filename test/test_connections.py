#!/usr/bin/env python3
"""
Unit tests for Atlas Stream Processing connections.

Run with: python3 -m pytest test_connections.py -v
"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from test_connection import StreamProcessingTester


class TestAtlasConnections(unittest.TestCase):
    """Test Atlas Stream Processing connections."""
    
    def setUp(self):
        """Set up test environment."""
        self.tester = StreamProcessingTester()
        self.test_processors = []
    
    def tearDown(self):
        """Clean up after tests."""
        self.tester.cleanup_test_processors()
    
    def test_sp_tool_exists(self):
        """Test that the sp tool exists and is executable."""
        self.assertTrue(self.tester.sp_tool.exists(), "SP tool not found")
        
        # Test basic sp command
        result = self.tester.run_sp_command("--help")
        self.assertEqual(result.returncode, 0, "SP tool not working")
        self.assertIn("Stream Processing", result.stdout)
    
    def test_connection_exists(self):
        """Test that the Cluster01 connection exists."""
        result = self.tester.run_sp_command("instances", "connections", "list")
        self.assertEqual(result.returncode, 0, "Could not list connections")
        self.assertIn("Cluster01", result.stdout, "Cluster01 connection not found")
    
    def test_processor_creation(self):
        """Test that we can create test processors."""
        # Test writer processor creation
        success = self.tester.create_processor("connection_test_writer.json")
        self.assertTrue(success, "Failed to create writer processor")
        
        # Verify processor exists
        self.assertTrue(
            self.tester.processor_exists("connection_test_writer"),
            "Writer processor not found after creation"
        )
    
    def test_processor_lifecycle(self):
        """Test complete processor lifecycle: create, start, stop, delete."""
        processor_name = "connection_test_writer"
        
        # Create
        success = self.tester.create_processor("connection_test_writer.json")
        self.assertTrue(success, "Failed to create processor")
        
        # Start
        success = self.tester.start_processor(processor_name)
        self.assertTrue(success, "Failed to start processor")
        
        # Stop
        success = self.tester.stop_processor(processor_name)
        self.assertTrue(success, "Failed to stop processor")
        
        # Delete
        success = self.tester.delete_processor(processor_name)
        self.assertTrue(success, "Failed to delete processor")
        
        # Verify it's gone
        self.assertFalse(
            self.tester.processor_exists(processor_name),
            "Processor still exists after deletion"
        )
    
    def test_json_processor_files(self):
        """Test that processor JSON files are valid."""
        test_dir = Path(__file__).parent
        
        for json_file in ["connection_test_writer.json", "connection_test_reader.json"]:
            file_path = test_dir / json_file
            self.assertTrue(file_path.exists(), f"{json_file} not found")
            
            # Test JSON validity
            with open(file_path) as f:
                try:
                    config = json.load(f)
                    self.assertIn("name", config, f"{json_file} missing 'name' field")
                    self.assertIn("pipeline", config, f"{json_file} missing 'pipeline' field")
                    self.assertIsInstance(config["pipeline"], list, f"{json_file} pipeline is not a list")
                except json.JSONDecodeError as e:
                    self.fail(f"{json_file} contains invalid JSON: {e}")


class TestConnectionIntegration(unittest.TestCase):
    """Integration tests for full connection workflow."""
    
    @classmethod
    def setUpClass(cls):
        """Set up integration test environment."""
        cls.tester = StreamProcessingTester()
    
    @classmethod 
    def tearDownClass(cls):
        """Clean up integration test environment."""
        cls.tester.cleanup_test_processors()
    
    def test_write_read_cycle(self):
        """Test complete write-read cycle to verify connection."""
        # This is a longer integration test
        print("\n🧪 Running full write-read integration test...")
        
        # Create and start writer
        success = self.tester.create_processor("connection_test_writer.json")
        self.assertTrue(success, "Failed to create writer processor")
        
        success = self.tester.start_processor("connection_test_writer")
        self.assertTrue(success, "Failed to start writer processor")
        
        # Let it run briefly
        import time
        time.sleep(10)
        
        # Stop writer
        success = self.tester.stop_processor("connection_test_writer")
        self.assertTrue(success, "Failed to stop writer processor")
        
        # Create and start reader
        success = self.tester.create_processor("connection_test_reader.json")
        self.assertTrue(success, "Failed to create reader processor")
        
        success = self.tester.start_processor("connection_test_reader")
        self.assertTrue(success, "Failed to start reader processor")
        
        # Let it process
        time.sleep(10)
        
        # Stop reader
        success = self.tester.stop_processor("connection_test_reader")
        self.assertTrue(success, "Failed to stop reader processor")
        
        print("✅ Write-read cycle completed successfully")


if __name__ == "__main__":
    # Run specific test classes
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--integration":
        # Run only integration tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestConnectionIntegration)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)
    else:
        # Run all tests
        unittest.main(verbosity=2)
