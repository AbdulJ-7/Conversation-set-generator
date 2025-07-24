"""
Test script to verify the dynamic prompt system and markdown file generation
"""

import sys
import os

# Add the parent directory to the path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import get_conversation_generator_prompt, load_example_conversation
from conversation_generator import ConversationGenerator


def test_dynamic_prompt():
    """Test dynamic prompt generation"""
    print("=" * 60)
    print("Testing Dynamic Prompt Generation")
    print("=" * 60)
    
    # Test prompt generation
    prompt = get_conversation_generator_prompt()
    
    print("✅ Dynamic prompt generated successfully")
    print(f"Prompt length: {len(prompt)} characters")
    
    # Check if example conversation is loaded
    if "Tech Investor's Deep Dive" in prompt:
        print("✅ Example conversation loaded from external file")
    else:
        print("❌ Example conversation not found in prompt")
    
    # Check if tools are included
    if "yahoo_finance: Stock prices" in prompt:
        print("✅ Tool descriptions included")
    else:
        print("❌ Tool descriptions not found")
    
    return prompt


def test_example_file():
    """Test external example file loading"""
    print("\n" + "=" * 60)
    print("Testing Example File Loading")
    print("=" * 60)
    
    # Change to parent directory to match expected working directory
    original_cwd = os.getcwd()
    try:
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        example_path = "conversation_sets/example_conversation_set.md"
        if os.path.exists(example_path):
            print("✅ Example file exists")
            
            example_content = load_example_conversation(example_path)
            if example_content and len(example_content) > 100:
                print("✅ Example content loaded successfully")
                print(f"Content length: {len(example_content)} characters")
            else:
                print("❌ Example content is empty or too short")
        else:
            print("❌ Example file does not exist")
    finally:
        os.chdir(original_cwd)


def test_conversation_generator_init():
    """Test conversation generator initialization"""
    print("\n" + "=" * 60)
    print("Testing Conversation Generator")
    print("=" * 60)
    
    try:
        # Test without API key (just initialization)
        generator = ConversationGenerator()
        print("❌ Generator initialized without API key (this should fail)")
    except ValueError as e:
        if "API key" in str(e):
            print("✅ Generator correctly requires API key")
        else:
            print(f"❌ Unexpected error: {e}")
    except Exception as e:
        print(f"⚠️  Other error during initialization: {e}")


def main():
    """Main test function"""
    print("Function Calling Conversation Generator - Test Suite")
    
    # Test dynamic prompt
    prompt = test_dynamic_prompt()
    
    # Test example file
    test_example_file()
    
    # Test generator initialization
    test_conversation_generator_init()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("✅ = Test passed")
    print("❌ = Test failed") 
    print("⚠️  = Test warning")
    print("\nTo run the full generator, configure your API keys in .env file")
    print("and run: python conversation_generator.py")


if __name__ == "__main__":
    main()
