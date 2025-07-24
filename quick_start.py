"""
Quick start script for the Function Calling Conversation Generator
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    # Map package names to their import names
    required_packages = {
        'openai': 'openai',
        'anthropic': 'anthropic', 
        'google-generativeai': 'google.generativeai',
        'python-dotenv': 'dotenv',
        'PyYAML': 'yaml',
        'requests': 'requests'
    }
    
    # Optional Google Sheets packages
    optional_packages = {
        'gspread': 'gspread',
        'google-auth': 'google.auth',
        'google-auth-oauthlib': 'google_auth_oauthlib'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    # Check optional packages for Google Sheets
    missing_optional = []
    for package_name, import_name in optional_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_optional.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall them with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    
    if missing_optional:
        print("⚠️  Optional Google Sheets packages not installed:")
        for package in missing_optional:
            print(f"   - {package}")
        print("💡 Google Sheets export will be disabled")
        print("   To enable: pip install gspread google-auth google-auth-oauthlib")
    else:
        print("✅ Google Sheets packages are available")
    
    return True

def check_api_keys():
    """Check if API keys are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_keys = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'Anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'Google': os.getenv('GOOGLE_API_KEY')
    }
    
    configured_keys = []
    for provider, key in api_keys.items():
        if key and key != f"your_{provider.lower()}_api_key_here":
            configured_keys.append(provider)
    
    if configured_keys:
        print(f"✅ API keys configured for: {', '.join(configured_keys)}")
        return True
    else:
        print("❌ No API keys configured")
        print("Please edit the .env file and add at least one API key:")
        print("   OPENAI_API_KEY=your_key_here")
        print("   ANTHROPIC_API_KEY=your_key_here")
        print("   GOOGLE_API_KEY=your_key_here")
        return False

def main():
    """Main quick start function"""
    print("=" * 60)
    print("Function Calling Conversation Generator - Quick Start")
    print("=" * 60)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        return
    
    # Check API keys
    print("\n2. Checking API keys...")
    if not check_api_keys():
        print("\n💡 Tip: You only need ONE API key to get started!")
        return
    
    # Check configuration
    print("\n3. Checking configuration...")
    if os.path.exists('config.yaml'):
        print("✅ Configuration file found")
    else:
        print("⚠️  No configuration file found")
        print("Running configuration setup...")
        
        try:
            from config_manager import ConfigManager
            config_manager = ConfigManager()
            if not config_manager.interactive_setup():
                print("Configuration cancelled")
                return
        except Exception as e:
            print(f"Error during configuration: {e}")
            return
    
    # Ready to generate
    print("\n" + "=" * 60)
    print("🚀 READY TO GENERATE!")
    print("=" * 60)
    print("Everything is configured correctly.")
    print("\nNext steps:")
    print("1. Run: python conversation_generator.py")
    print("2. Or reconfigure: python config_manager.py")
    print("\nThe generator will create conversation sets in the 'conversation_sets' folder.")
    
    # Ask if user wants to run generator now
    choice = input("\nWould you like to start generating now? (y/n) [y]: ").strip().lower()
    if choice != 'n':
        print("\nStarting conversation generator...")
        try:
            from conversation_generator import main as generator_main
            generator_main()
        except Exception as e:
            print(f"Error running generator: {e}")
            print("You can try running it manually: python conversation_generator.py")

if __name__ == "__main__":
    main()
