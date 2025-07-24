"""
Test runner for the Function Calling Conversation Generator

This script runs all tests in the test suite.
"""

import sys
import os

# Add the parent directory to the path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    """Run all available tests"""
    print("=" * 70)
    print("Function Calling Conversation Generator - Test Suite")
    print("=" * 70)
    
    test_results = []
    
    # Test 1: System tests
    print("\n" + "=" * 50)
    print("Running System Tests")
    print("=" * 50)
    try:
        from test_system import main as test_system_main
        test_system_main()
        test_results.append(("System Tests", "PASSED"))
    except Exception as e:
        print(f"❌ System tests failed: {e}")
        test_results.append(("System Tests", "FAILED"))
    
    # Test 2: Dynamic prompt tests
    print("\n" + "=" * 50)
    print("Running Dynamic Prompt Tests")
    print("=" * 50)
    try:
        from test_dynamic_prompt import main as test_dynamic_prompt_main
        test_dynamic_prompt_main()
        test_results.append(("Dynamic Prompt Tests", "PASSED"))
    except Exception as e:
        print(f"❌ Dynamic prompt tests failed: {e}")
        test_results.append(("Dynamic Prompt Tests", "FAILED"))
    
    # Test 3: Google Sheets tests (optional)
    print("\n" + "=" * 50)
    print("Running Google Sheets Tests")
    print("=" * 50)
    try:
        from test_google_sheets import main as test_google_sheets_main
        test_google_sheets_main()
        test_results.append(("Google Sheets Tests", "PASSED"))
    except Exception as e:
        print(f"❌ Google Sheets tests failed: {e}")
        test_results.append(("Google Sheets Tests", "FAILED"))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, result in test_results:
        status = "✅" if result == "PASSED" else "❌"
        print(f"{status} {test_name}: {result}")
    
    print("\n" + "=" * 70)
    passed = sum(1 for _, result in test_results if result == "PASSED")
    total = len(test_results)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
