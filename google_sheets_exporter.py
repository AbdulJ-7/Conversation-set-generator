#!/usr/bin/env python3
"""
Google Sheets exporter for conversation sets
"""

import gspread
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import re
import yaml


class GoogleSheetsExporter:
    """Export conversation sets to Google Sheets"""
    
    def __init__(self, credentials_file: str = "credentials.json"):
        """
        Initialize the Google Sheets exporter
        
        Args:
            credentials_file: Path to the Google service account credentials JSON file
        """
        self.credentials_file = credentials_file
        self.gc = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(
                    f"Credentials file '{self.credentials_file}' not found. "
                    "Please download it from Google Cloud Console."
                )
            
            self.gc = gspread.service_account(filename=self.credentials_file)
            print("✅ Successfully authenticated with Google Sheets API")
            
        except Exception as e:
            print(f"❌ Failed to authenticate with Google Sheets: {e}")
            print("Please check your credentials file and permissions.")
            self.gc = None
    
    def get_service_account_email(self) -> Optional[str]:
        """Get the service account email from credentials"""
        try:
            with open(self.credentials_file, 'r') as f:
                creds_data = json.load(f)
                return creds_data.get('client_email')
        except Exception:
            return None
    
    def open_spreadsheet(self, spreadsheet_url: str) -> Optional[gspread.Spreadsheet]:
        """
        Open an existing spreadsheet by URL
        
        Args:
            spreadsheet_url: URL or ID of existing spreadsheet
            
        Returns:
            Spreadsheet object or None if failed
        """
        if not self.gc:
            print("❌ Not authenticated with Google Sheets")
            return None
        
        try:
            if spreadsheet_url.startswith('https://'):
                spreadsheet = self.gc.open_by_url(spreadsheet_url)
            else:
                # Assume it's a spreadsheet ID
                spreadsheet = self.gc.open_by_key(spreadsheet_url)
            print(f"✅ Opened spreadsheet: {spreadsheet.title}")
            return spreadsheet
        except Exception as e:
            service_email = self.get_service_account_email()
            print(f"❌ Cannot access spreadsheet: {e}")
            print("\n💡 TROUBLESHOOTING:")
            print("1. Make sure the spreadsheet URL is correct")
            if service_email:
                print(f"2. Make sure you've shared the spreadsheet with: {service_email}")
            else:
                print("2. Make sure you've shared the spreadsheet with your service account email")
            print("3. Make sure the service account has 'Editor' permissions")
            print("4. Try opening the spreadsheet URL in your browser to verify it exists")
            return None
    
    def get_or_create_worksheet(self, spreadsheet, worksheet_name: str):
        """Get or create worksheet with given name"""
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            print(f"✅ Using existing worksheet: {worksheet_name}")
            return worksheet
        except gspread.WorksheetNotFound:
            # Create new worksheet
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=26)
            print(f"✅ Created new worksheet: {worksheet_name}")
            return worksheet
    
    def setup_headers(self, worksheet, start_row: int = 1):
        """Setup column headers"""
        headers = [
            "ID", "Title", "User Motive", "Domains & Subdomains",
            "Turn 1", "Tools 1", "Turn 2", "Tools 2",
            "Turn 3", "Tools 3", "Turn 4", "Tools 4",
            "Turn 5", "Tools 5", "Turn 6", "Tools 6",
            "Turn 7", "Tools 7", "Turn 8", "Tools 8",
            "Generated On", "Provider", "Model", "Temperature", "File Path"
        ]
        
        # Only add headers if starting at row 1
        if start_row == 1:
            try:
                # Check if headers already exist
                existing_headers = worksheet.row_values(1)
                if not existing_headers or existing_headers[0] != "ID":
                    worksheet.insert_row(headers, 1)
                    print("✅ Headers added to worksheet")
            except Exception:
                worksheet.insert_row(headers, 1)
                print("✅ Headers added to worksheet")
    
    def parse_conversation_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a conversation set markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extract metadata
            metadata = {}
            lines = content.split('\n')
            for line in lines[:10]:
                if line.startswith('**Generated on:**'):
                    metadata['generated_on'] = line.replace('**Generated on:**', '').strip()
                elif line.startswith('**Provider:**'):
                    metadata['provider'] = line.replace('**Provider:**', '').strip()
                elif line.startswith('**Model:**'):
                    metadata['model'] = line.replace('**Model:**', '').strip()
                elif line.startswith('**Temperature:**'):
                    metadata['temperature'] = line.replace('**Temperature:**', '').strip()
            
            # Extract title
            title_match = re.search(r'# Conversation Set \d+:\s*(.+)', content)
            title = title_match.group(1).strip() if title_match else "Unknown"
            
            # Extract user motive
            motive_match = re.search(r'\*\*User Motive:\*\*\s*(.+)', content)
            user_motive = motive_match.group(1).strip() if motive_match else ""
            
            # Extract domains
            domains_match = re.search(r'\*\*Domains & Subdomains:\*\*\s*(.+)', content)
            domains = domains_match.group(1).strip() if domains_match else ""
            
            # Extract conversation turns and tools
            turns = []
            tools = []
            
            # Find all "User:" and "Tools used:" patterns
            user_pattern = r'User:\s*(.+?)(?=\n\n|\nTools used:|Assistant:)'
            tool_pattern = r'Tools used:\s*(.+?)(?=\n\n|\nUser:|Assistant:)'
            
            user_matches = re.findall(user_pattern, content, re.DOTALL)
            tool_matches = re.findall(tool_pattern, content, re.DOTALL)
            
            # Process up to 8 turns
            for i in range(min(8, len(user_matches))):
                turns.append(user_matches[i].strip())
                tools.append(tool_matches[i].strip() if i < len(tool_matches) else "")
            
            # Pad with empty strings if less than 8 turns
            while len(turns) < 8:
                turns.append("")
                tools.append("")
            
            # Extract ID from filename
            file_id = Path(file_path).stem.replace('conversation_set_', '')
            
            return {
                'id': file_id,
                'title': title,
                'user_motive': user_motive,
                'domains': domains,
                'turns': turns,
                'tools': tools,
                'metadata': metadata
            }
            
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return None
    
    def export_conversation_sets(self, 
                                conversation_sets_folder: str = "conversation_sets",
                                spreadsheet_url: str = None,
                                worksheet_name: str = "Conversation Sets",
                                start_row: int = 2) -> bool:
        """
        Export all conversation sets to Google Sheets
        
        Args:
            conversation_sets_folder: Folder containing conversation set files
            spreadsheet_url: URL of the target spreadsheet
            worksheet_name: Name of the worksheet to write to
            start_row: Row number to start writing data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.gc:
            print("❌ Not authenticated with Google Sheets")
            return False
        
        if not spreadsheet_url:
            print("❌ Spreadsheet URL is required")
            return False
        
        # Open spreadsheet
        spreadsheet = self.open_spreadsheet(spreadsheet_url)
        if not spreadsheet:
            return False
        
        # Get or create worksheet
        worksheet = self.get_or_create_worksheet(spreadsheet, worksheet_name)
        if not worksheet:
            return False
        
        # Setup headers
        self.setup_headers(worksheet, start_row if start_row == 1 else 1)
        
        # Find conversation files
        conversation_files = list(Path(conversation_sets_folder).glob("conversation_set_*.md"))
        if not conversation_files:
            print(f"❌ No conversation set files found in {conversation_sets_folder}")
            return False
        
        print(f"📄 Found {len(conversation_files)} conversation set files")
        
        # Parse files and prepare data
        rows_to_add = []
        for file_path in sorted(conversation_files):
            parsed_data = self.parse_conversation_file(str(file_path))
            if parsed_data:
                # Create row data
                row_data = [
                    parsed_data['id'],
                    parsed_data['title'],
                    parsed_data['user_motive'],
                    parsed_data['domains']
                ]
                
                # Add turns and tools
                for i in range(8):
                    row_data.extend([
                        parsed_data['turns'][i],
                        parsed_data['tools'][i]
                    ])
                
                # Add metadata
                metadata = parsed_data['metadata']
                row_data.extend([
                    metadata.get('generated_on', ''),
                    metadata.get('provider', ''),
                    metadata.get('model', ''),
                    metadata.get('temperature', ''),
                    str(file_path)
                ])
                
                rows_to_add.append(row_data)
        
        # Write data to spreadsheet
        if rows_to_add:
            try:
                # Determine where to write data
                if start_row == 1:
                    # Append after existing data
                    worksheet.append_rows(rows_to_add)
                else:
                    # Write starting from specific row
                    range_start = f"A{start_row}"
                    worksheet.update(range_name=range_start, values=rows_to_add)
                
                print(f"✅ Successfully exported {len(rows_to_add)} conversation sets to Google Sheets")
                print(f"📊 Data written starting from row {start_row}")
                print(f"📊 Spreadsheet URL: {spreadsheet.url}")
                return True
                
            except Exception as e:
                print(f"❌ Failed to write to Google Sheets: {e}")
                return False
        else:
            print("❌ No valid conversation sets to export")
            return False


def main():
    """Main function for testing the Google Sheets exporter"""
    print("🔄 Exporting conversation sets...")
    
    # Load config
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ config.yaml not found")
        return False
    
    # Get Google Sheets settings
    gs_config = config.get('google_sheets', {})
    if not gs_config.get('enabled', False):
        print("❌ Google Sheets export is not enabled in config.yaml")
        return False
    
    # Initialize exporter
    exporter = GoogleSheetsExporter(gs_config.get('credentials_file', 'credentials.json'))
    
    if not exporter.gc:
        print("❌ Authentication failed")
        return False
    
    # Export with configured settings
    success = exporter.export_conversation_sets(
        conversation_sets_folder='conversation_sets',
        spreadsheet_url=gs_config.get('spreadsheet_url'),
        worksheet_name=gs_config.get('worksheet_name', 'Conversation Sets'),
        start_row=gs_config.get('start_row', 2)
    )
    
    if success:
        print('✅ Export completed successfully!')
        return True
    else:
        print('❌ Export failed')
        return False


if __name__ == "__main__":
    main()
