#!/usr/bin/env python3
"""
Test script for the dynamic prompt generation system
"""

import sys
import os
import yaml

# Add the parent directory to the path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import get_conversation_generator_prompt, load_config


def test_dynamic_prompt():
    """Test the dynamic prompt generation"""
    print("=" * 60)
    print("Testing Dynamic Prompt Generation")
    print("=" * 60)
    
    # Change to parent directory to match expected working directory
    original_cwd = os.getcwd()
    try:
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Load current config
        config = load_config()
        print(f"✅ Config loaded successfully")
        print(f"   Provider: {config['llm']['provider']}")
        print(f"   Batch size: {config['generation']['batch_size']}")
        print(f"   Total sets: {config['generation']['num_conversation_sets']}")
        print(f"   Available tools: {len(config['available_tools'])}")
        
        # Generate dynamic prompt
        prompt = get_conversation_generator_prompt()
        print(f"\n✅ Dynamic prompt generated successfully")
        print(f"   Prompt length: {len(prompt)} characters")
        
        # Check if dynamic elements are included
        batch_size = str(config['generation']['batch_size'])
        total_sets = str(config['generation']['num_conversation_sets'])
        
        checks = [
            (f"Generate {batch_size} unique" in prompt, f"Batch size ({batch_size}) in prompt"),
        (config['available_tools'][0] in prompt, "First tool in prompt"),
        ("User Motive:" in prompt, "Example conversation format in prompt"),
        ("Tools:" in prompt, "Tool usage format in prompt")
    ]
    
    print("\n📋 Dynamic Content Verification:")
    for check, description in checks:
        status = "✅" if check else "❌"
        print(f"   {status} {description}")
    
    # Show a snippet of the generated prompt
    print(f"\n📝 Prompt Preview (first 300 chars):")
    print("-" * 60)
    print(prompt[:300] + "...")
    print("-" * 60)
    
        if all(check for check, _ in checks):
            print("\n🎉 All tests passed! Dynamic prompt system is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Please check the configuration.")
    finally:
        os.chdir(original_cwd)

if __name__ == "__main__":
    test_dynamic_prompt()
