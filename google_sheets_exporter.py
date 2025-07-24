"""
Google Sheets exporter for conversation sets
"""

import gspread
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from google.auth.exceptions import RefreshError
from pathlib import Path
import re


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
    
    def create_or_open_spreadsheet(self, title: str = "Function Calling Conversation Sets") -> Optional[gspread.Spreadsheet]:
        """
        Create a new spreadsheet or open existing one
        
        Args:
            title: Name of the spreadsheet
            
        Returns:
            Spreadsheet object or None if failed
        """
        if not self.gc:
            print("❌ Not authenticated with Google Sheets")
            return None
        
        try:
            # Try to open existing spreadsheet
            try:
                spreadsheet = self.gc.open(title)
                print(f"✅ Opened existing spreadsheet: {title}")
                return spreadsheet
            except gspread.SpreadsheetNotFound:
                # Create new spreadsheet
                spreadsheet = self.gc.create(title)
                print(f"✅ Created new spreadsheet: {title}")
                
                # Share with your email (you'll need to add this manually or via config)
                # spreadsheet.share('your-email@gmail.com', perm_type='user', role='writer')
                
                return spreadsheet
                
        except Exception as e:
            print(f"❌ Failed to create/open spreadsheet: {e}")
            return None
    
    def setup_worksheet_headers(self, worksheet):
        """Setup headers for the conversation sets worksheet"""
        headers = [
            "ID",
            "Title", 
            "User Motive",
            "Domains & Subdomains",
            "Turn 1",
            "Tools 1",
            "Turn 2", 
            "Tools 2",
            "Turn 3",
            "Tools 3", 
            "Turn 4",
            "Tools 4",
            "Turn 5", 
            "Tools 5",
            "Turn 6",
            "Tools 6",
            "Turn 7",
            "Tools 7",
            "Turn 8", 
            "Tools 8",
            "Generated On",
            "Provider",
            "Model",
            "Temperature",
            "File Path"
        ]
        
        # Clear existing content and set headers
        worksheet.clear()
        worksheet.append_row(headers)
        
        # Format header row
        worksheet.format('A1:Y1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
        })
        
        print("✅ Worksheet headers configured")
    
    def parse_conversation_set(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a conversation set markdown file
        
        Args:
            file_path: Path to the conversation set file
            
        Returns:
            Dictionary with parsed conversation data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extract metadata from header
            metadata = {}
            lines = content.split('\n')
            
            for line in lines[:10]:  # Check first 10 lines for metadata
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
            
            # Extract ID from filename
            id_match = re.search(r'conversation_set_(\d+)', file_path)
            conv_id = id_match.group(1) if id_match else "000"
            
            # Extract user motive
            user_motive_match = re.search(r'\*\*User Motive:\*\*\s*(.+?)(?=\*\*|---|\n\n)', content, re.DOTALL)
            user_motive = user_motive_match.group(1).strip() if user_motive_match else ""
            
            # Extract domains
            domains_match = re.search(r'\*\*Domains & Subdomains:\*\*\s*(.+?)(?=\*\*|---|\n\n)', content, re.DOTALL)
            domains = domains_match.group(1).strip() if domains_match else ""
            
            # Extract turns and tools
            turns = []
            tools = []
            
            # Find all numbered sections (### 1., ### 2., etc.)
            turn_pattern = r'### (\d+)\.?\s*\n\n?>\s*(.+?)\n\n\*\*Tools:\*\*\s*(.+?)(?=---|###|\Z)'
            turn_matches = re.findall(turn_pattern, content, re.DOTALL)
            
            for turn_num, turn_content, turn_tools in turn_matches:
                turns.append(turn_content.strip())
                tools.append(turn_tools.strip())
            
            return {
                'id': conv_id,
                'title': title,
                'user_motive': user_motive,
                'domains': domains,
                'turns': turns,
                'tools': tools,
                'metadata': metadata,
                'file_path': file_path
            }
            
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return None
    
    def export_conversation_sets(self, conversation_sets_folder: str = "conversation_sets", 
                                spreadsheet_title: str = "Function Calling Conversation Sets") -> bool:
        """
        Export all conversation sets to Google Sheets
        
        Args:
            conversation_sets_folder: Folder containing conversation set files
            spreadsheet_title: Name of the Google Sheets spreadsheet
            
        Returns:
            True if successful, False otherwise
        """
        if not self.gc:
            print("❌ Not authenticated with Google Sheets")
            return False
        
        # Create or open spreadsheet
        spreadsheet = self.create_or_open_spreadsheet(spreadsheet_title)
        if not spreadsheet:
            return False
        
        # Get or create worksheet
        try:
            worksheet = spreadsheet.worksheet("Conversation Sets")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title="Conversation Sets", rows=1000, cols=26)
        
        # Setup headers
        self.setup_worksheet_headers(worksheet)
        
        # Find all conversation set files
        conversation_files = list(Path(conversation_sets_folder).glob("conversation_set_*.md"))
        
        if not conversation_files:
            print(f"❌ No conversation set files found in {conversation_sets_folder}")
            return False
        
        print(f"📄 Found {len(conversation_files)} conversation set files")
        
        # Parse and export each file
        rows_to_add = []
        successful_exports = 0
        
        for file_path in sorted(conversation_files):
            parsed_data = self.parse_conversation_set(str(file_path))
            if parsed_data:
                # Create row data
                row_data = [
                    parsed_data['id'],
                    parsed_data['title'],
                    parsed_data['user_motive'],
                    parsed_data['domains']
                ]
                
                # Add up to 8 turns and their tools
                for i in range(8):
                    if i < len(parsed_data['turns']):
                        row_data.extend([
                            parsed_data['turns'][i],
                            parsed_data['tools'][i]
                        ])
                    else:
                        row_data.extend(["", ""])  # Empty cells for unused turns
                
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
                successful_exports += 1
        
        # Batch update all rows
        if rows_to_add:
            try:
                worksheet.append_rows(rows_to_add)
                print(f"✅ Successfully exported {successful_exports} conversation sets to Google Sheets")
                print(f"📊 Spreadsheet URL: {spreadsheet.url}")
                return True
            except Exception as e:
                print(f"❌ Failed to write to Google Sheets: {e}")
                return False
        else:
            print("❌ No valid conversation sets to export")
            return False
    
    def export_summary(self, summary_file: str = "conversation_sets/generation_summary.json",
                      spreadsheet_title: str = "Function Calling Conversation Sets") -> bool:
        """
        Export generation summary to a separate worksheet
        
        Args:
            summary_file: Path to the generation summary JSON file
            spreadsheet_title: Name of the Google Sheets spreadsheet
            
        Returns:
            True if successful, False otherwise
        """
        if not self.gc:
            print("❌ Not authenticated with Google Sheets")
            return False
        
        if not os.path.exists(summary_file):
            print(f"❌ Summary file not found: {summary_file}")
            return False
        
        try:
            with open(summary_file, 'r', encoding='utf-8') as file:
                summary_data = json.load(file)
        except Exception as e:
            print(f"❌ Error reading summary file: {e}")
            return False
        
        # Open spreadsheet
        spreadsheet = self.create_or_open_spreadsheet(spreadsheet_title)
        if not spreadsheet:
            return False
        
        # Get or create summary worksheet
        try:
            worksheet = spreadsheet.worksheet("Generation Summary")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title="Generation Summary", rows=100, cols=10)
        
        # Clear and setup summary worksheet
        worksheet.clear()
        
        # Add summary data
        summary_rows = [
            ["Generation Summary", ""],
            ["", ""],
            ["Total Requested", summary_data.get('total_requested', '')],
            ["Total Generated", summary_data.get('total_generated', '')],
            ["Files Created", summary_data.get('files_created', '')],
            ["Provider", summary_data.get('provider', '')],
            ["Model", summary_data.get('model', '')],
            ["Generation Time", summary_data.get('generation_time', '')],
            ["Output Folder", summary_data.get('output_folder', '')],
            ["", ""],
            ["Generated Files:", ""]
        ]
        
        # Add file list
        for file_path in summary_data.get('files', []):
            summary_rows.append([os.path.basename(file_path), file_path])
        
        worksheet.append_rows(summary_rows)
        
        # Format header
        worksheet.format('A1:B1', {
            'textFormat': {'bold': True, 'fontSize': 16},
            'backgroundColor': {'red': 0.8, 'green': 0.9, 'blue': 1.0}
        })
        
        print("✅ Successfully exported generation summary to Google Sheets")
        return True


def main():
    """Main function for testing the Google Sheets exporter"""
    exporter = GoogleSheetsExporter()
    
    if exporter.gc:
        print("🔄 Exporting conversation sets...")
        success = exporter.export_conversation_sets()
        
        if success:
            print("🔄 Exporting generation summary...")
            exporter.export_summary()
            print("🎉 Export completed successfully!")
        else:
            print("❌ Export failed")
    else:
        print("❌ Cannot export - authentication failed")


if __name__ == "__main__":
    main()
