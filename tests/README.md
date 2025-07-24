# Tests

This folder contains the test suite for the Function Calling Conversation Generator.

## Test Files

- **`test_system.py`** - General system tests for dynamic prompt generation, file loading, and basic functionality
- **`test_dynamic_prompt.py`** - Specific tests for prompt customization and configuration loading
- **`run_tests.py`** - Test runner that executes all tests in the suite
- **`__init__.py`** - Makes the tests directory a Python package

## Running Tests

### Run All Tests
```bash
# From the main project directory
python tests/run_tests.py
```

### Run Individual Tests
```bash
# System tests
python tests/test_system.py

# Dynamic prompt tests  
python tests/test_dynamic_prompt.py
```

## Test Requirements

The tests require:
- All project dependencies installed (`pip install -r requirements.txt`)
- The `conversation_sets/example_conversation_set.md` file to exist
- A valid `config.yaml` file in the project root

## What the Tests Check

### System Tests (`test_system.py`)
- ✅ Dynamic prompt generation functionality
- ✅ External example file loading
- ✅ Conversation generator initialization
- ✅ Error handling for missing API keys

### Dynamic Prompt Tests (`test_dynamic_prompt.py`)
- ✅ Configuration file loading
- ✅ Batch size inclusion in prompts
- ✅ Tool list integration
- ✅ Example conversation formatting
- ✅ Dynamic content verification

## Test Output

Tests use emoji indicators:
- ✅ Test passed
- ❌ Test failed  
- ⚠️ Test warning

## Notes

- Tests automatically handle working directory changes
- No API keys required for basic functionality tests
- Tests are designed to run without actual LLM API calls
- All tests should pass on a properly configured system
