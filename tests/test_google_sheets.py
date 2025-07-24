"""
Test script for Google Sheets export functionality
"""

import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_google_sheets_import():
    """Test if Google Sheets packages can be imported"""
    print("🔄 Testing Google Sheets package imports...")
    
    try:
        import gspread
        print("✅ gspread imported successfully")
    except ImportError:
        print("❌ gspread not found - install with: pip install gspread")
        return False
    
    try:
        import google.auth
        print("✅ google.auth imported successfully")
    except ImportError:
        print("❌ google-auth not found - install with: pip install google-auth")
        return False
    
    try:
        import google_auth_oauthlib
        print("✅ google-auth-oauthlib imported successfully")
    except ImportError:
        print("❌ google-auth-oauthlib not found - install with: pip install google-auth-oauthlib")
        return False
    
    return True


def test_credentials_file():
    """Test if credentials file exists"""
    print("\n🔄 Testing credentials file...")
    
    creds_file = "credentials.json"
    if os.path.exists(creds_file):
        print(f"✅ Credentials file found: {creds_file}")
        return True
    else:
        print(f"❌ Credentials file not found: {creds_file}")
        print("💡 Download credentials.json from Google Cloud Console")
        print("   See GOOGLE_SHEETS_SETUP.md for detailed instructions")
        return False


def test_google_sheets_exporter():
    """Test Google Sheets exporter initialization"""
    print("\n🔄 Testing Google Sheets exporter...")
    
    try:
        from google_sheets_exporter import GoogleSheetsExporter
        print("✅ GoogleSheetsExporter imported successfully")
        
        # Try to initialize (will fail without credentials, but tests import)
        if os.path.exists("credentials.json"):
            exporter = GoogleSheetsExporter()
            if exporter.gc:
                print("✅ Google Sheets authentication successful!")
                return True
            else:
                print("❌ Google Sheets authentication failed")
                print("💡 Check your credentials and Google Cloud setup")
                return False
        else:
            print("⚠️  Cannot test authentication without credentials.json")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import GoogleSheetsExporter: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing Google Sheets exporter: {e}")
        return False


def test_config_integration():
    """Test Google Sheets configuration integration"""
    print("\n🔄 Testing configuration integration...")
    
    try:
        import yaml
        
        with open("config.yaml", 'r') as file:
            config = yaml.safe_load(file)
        
        google_sheets_config = config.get('google_sheets', {})
        
        if google_sheets_config:
            print("✅ Google Sheets configuration found in config.yaml")
            print(f"   Enabled: {google_sheets_config.get('enabled', False)}")
            print(f"   Spreadsheet title: {google_sheets_config.get('spreadsheet_title', 'Not set')}")
            print(f"   Credentials file: {google_sheets_config.get('credentials_file', 'Not set')}")
            return True
        else:
            print("❌ Google Sheets configuration not found in config.yaml")
            print("💡 Run: python config_manager.py to configure Google Sheets")
            return False
            
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False


def main():
    """Main test function"""
    print("=" * 70)
    print("Google Sheets Export - Test Suite")
    print("=" * 70)
    
    tests = [
        ("Package Imports", test_google_sheets_import),
        ("Credentials File", test_credentials_file),
        ("Exporter Functionality", test_google_sheets_exporter),
        ("Configuration Integration", test_config_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASSED" if result else "FAILED"))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, "CRASHED"))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅" if result == "PASSED" else "❌"
        print(f"{status} {test_name}: {result}")
    
    passed = sum(1 for _, result in results if result == "PASSED")
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Google Sheets export is ready to use.")
    elif passed >= 2:  # Imports and config work
        print("⚠️  Partial setup - check credentials and authentication.")
        print("💡 See GOOGLE_SHEETS_SETUP.md for complete setup instructions.")
    else:
        print("❌ Setup incomplete - install packages and configure credentials.")
        print("💡 See GOOGLE_SHEETS_SETUP.md for setup instructions.")


if __name__ == "__main__":
    main()
