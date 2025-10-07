#!/usr/bin/env python3
"""
Test Case Counter
Counts all test cases in the gen-atomic repository.
"""
import os
import re
from pathlib import Path


def count_test_cases(src_dir: str = None):
    """
    Count all test cases in the repository.
    
    Args:
        src_dir: Source directory path. Defaults to 'src' in current working directory.
    
    Returns:
        tuple: (test_files_info, total_count)
    """
    if src_dir is None:
        # Get the repository root
        script_dir = Path(__file__).parent.absolute()
        src_dir = script_dir / "src"
    else:
        src_dir = Path(src_dir)
    
    test_files = []
    total_count = 0
    
    # Find all files with TestCase classes
    for py_file in src_dir.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check if file contains test cases
                if 'TestCase' in content and 'def test_' in content:
                    # Count test methods
                    test_methods = re.findall(r'^\s*def (test_\w+)\(', content, re.MULTILINE)
                    if test_methods:
                        rel_path = py_file.relative_to(src_dir)
                        test_files.append({
                            'file': str(rel_path),
                            'full_path': str(py_file),
                            'count': len(test_methods),
                            'methods': test_methods
                        })
                        total_count += len(test_methods)
        except Exception as e:
            print(f"Warning: Could not read {py_file}: {e}")
            continue
    
    # Sort by file path
    test_files.sort(key=lambda x: x['file'])
    
    return test_files, total_count


def print_test_summary(test_files, total_count):
    """Print a formatted summary of test cases."""
    print("=" * 80)
    print("TEST CASE COUNT SUMMARY")
    print("=" * 80)
    print()
    
    for test_file in test_files:
        print(f"{test_file['file']}: {test_file['count']} test case(s)")
        for method in test_file['methods']:
            print(f"  - {method}")
        print()
    
    print("=" * 80)
    print(f"TOTAL TEST CASES: {total_count}")
    print("=" * 80)


def main():
    """Main entry point."""
    test_files, total_count = count_test_cases()
    print_test_summary(test_files, total_count)
    return total_count


if __name__ == "__main__":
    main()
