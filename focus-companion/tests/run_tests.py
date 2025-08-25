#!/usr/bin/env python3
"""
Test runner for Focus Companion application
Runs all unit tests and integration tests
"""

import unittest
import sys
import os
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_all_tests():
    """Run all tests in the tests directory"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

def run_specific_test(test_name):
    """Run a specific test file"""
    test_file = f"test_{test_name}.py"
    test_path = Path(__file__).parent / test_file
    
    if not test_path.exists():
        print(f"Test file {test_file} not found!")
        return 1
    
    # Import and run specific test
    loader = unittest.TestLoader()
    suite = loader.discover(Path(__file__).parent, pattern=test_file)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

def list_available_tests():
    """List all available test files"""
    test_dir = Path(__file__).parent
    test_files = list(test_dir.glob('test_*.py'))
    
    print("Available tests:")
    for test_file in test_files:
        test_name = test_file.stem.replace('test_', '')
        print(f"  - {test_name}")
    
    print(f"\nTotal: {len(test_files)} test files")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'list':
            list_available_tests()
        elif command == 'run':
            if len(sys.argv) > 2:
                test_name = sys.argv[2]
                exit_code = run_specific_test(test_name)
            else:
                print("Please specify a test name: python run_tests.py run <test_name>")
                exit_code = 1
        else:
            print("Unknown command. Use 'list' to see available tests or 'run <test_name>' to run a specific test.")
            exit_code = 1
    else:
        # Run all tests by default
        exit_code = run_all_tests()
    
    sys.exit(exit_code) 