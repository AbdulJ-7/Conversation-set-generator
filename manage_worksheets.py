#!/usr/bin/env python3
"""
Google Sheets Worksheet Manager
Helps manage worksheets in your Google Sheets spreadsheet
"""

import sys
from pathlib import Path
import yaml

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from google_sheets_exporter import GoogleSheetsExporter

def main():
    """Main worksheet management function"""
    print("📊 Google Sheets Worksheet Manager")
    print("=" * 50)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    gs_config = config['google_sheets']
    spreadsheet_title = gs_config['spreadsheet_title']
    spreadsheet_url = gs_config['spreadsheet_url']
    
    print(f"📋 Configured to use worksheet: '{spreadsheet_title}'")
    print(f"🔗 Spreadsheet URL: {spreadsheet_url}")
    
    # Initialize exporter
    exporter = GoogleSheetsExporter(gs_config['credentials_file'])
    
    if not exporter.gc:
        print("❌ Authentication failed")
        return
    
    # Open spreadsheet
    spreadsheet = exporter.create_or_open_spreadsheet(spreadsheet_title, spreadsheet_url)
    if not spreadsheet:
        print("❌ Failed to open spreadsheet")
        return
    
    print(f"✅ Opened spreadsheet: '{spreadsheet.title}'")
    
    # List all worksheets
    worksheets = spreadsheet.worksheets()
    print(f"\n📊 Found {len(worksheets)} worksheet(s):")
    for i, ws in enumerate(worksheets, 1):
        print(f"   {i}. '{ws.title}' ({ws.row_count} rows, {ws.col_count} cols)")
    
    # Check if target worksheet exists
    target_worksheet_name = spreadsheet_title  # "Epsilon"
    target_exists = any(ws.title == target_worksheet_name for ws in worksheets)
    
    if target_exists:
        print(f"\n✅ Target worksheet '{target_worksheet_name}' already exists!")
        print("   The conversation data will be exported to this worksheet.")
    else:
        print(f"\n❓ Target worksheet '{target_worksheet_name}' does not exist.")
        print("   Options:")
        print("   1. Create new worksheet named 'Epsilon'")
        print("   2. Use an existing worksheet")
        print("   3. Rename an existing worksheet to 'Epsilon'")
        
        choice = input("\nWhat would you like to do? (1/2/3): ").strip()
        
        if choice == "1":
            # Create new worksheet
            new_ws = spreadsheet.add_worksheet(title=target_worksheet_name, rows=1000, cols=26)
            print(f"✅ Created new worksheet: '{target_worksheet_name}'")
            
        elif choice == "2":
            # Use existing worksheet - show options
            print("\nSelect an existing worksheet to use:")
            for i, ws in enumerate(worksheets, 1):
                print(f"   {i}. '{ws.title}'")
            
            try:
                ws_choice = int(input(f"Enter worksheet number (1-{len(worksheets)}): ").strip())
                if 1 <= ws_choice <= len(worksheets):
                    selected_ws = worksheets[ws_choice - 1]
                    print(f"\n💡 To use '{selected_ws.title}', update your config.yaml:")
                    print(f"   spreadsheet_title: \"{selected_ws.title}\"")
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid input")
                
        elif choice == "3":
            # Rename existing worksheet
            print("\nSelect a worksheet to rename to 'Epsilon':")
            for i, ws in enumerate(worksheets, 1):
                print(f"   {i}. '{ws.title}'")
            
            try:
                ws_choice = int(input(f"Enter worksheet number (1-{len(worksheets)}): ").strip())
                if 1 <= ws_choice <= len(worksheets):
                    selected_ws = worksheets[ws_choice - 1]
                    old_name = selected_ws.title
                    selected_ws.update_title(target_worksheet_name)
                    print(f"✅ Renamed '{old_name}' to '{target_worksheet_name}'")
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid input")
        else:
            print("❌ Invalid choice")
    
    print(f"\n🎉 Ready to export! Run: uv run python conversation_generator.py")

if __name__ == "__main__":
    main()
