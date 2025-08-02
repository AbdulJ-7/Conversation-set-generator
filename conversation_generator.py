"""
Function Calling Conversation Generator

This script generates complex function calling conversation sets using various LLMs
to assist human annotators in creating training data.
"""

import os
import yaml
import json
import re
from typing import Dict, List, Any
from pathlib import Path
from dotenv import load_dotenv
import time
from datetime import datetime

from llm_providers import get_provider
from prompts import get_conversation_generator_prompt
from google_sheets_exporter import GoogleSheetsExporter


class ConversationGenerator:
    """Main class for generating function calling conversation sets"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the generator with configuration"""
        self.config_path = config_path  # Store config path for dynamic prompt generation
        self.config = self._load_config(config_path)
        self._load_environment()
        self.provider = self._initialize_provider()
        self.output_folder = Path(self.config['generation']['output_folder'])
        self._ensure_output_folder()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{config_path}' not found")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")
    
    def _load_environment(self):
        """Load environment variables from .env file"""
        load_dotenv()
        
        # Get API key for the selected provider
        provider_name = self.config['llm']['provider']
        api_key_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'google': 'GOOGLE_API_KEY'
        }
        
        api_key_name = api_key_map.get(provider_name)
        if not api_key_name:
            raise ValueError(f"Unsupported provider: {provider_name}")
        
        self.api_key = os.getenv(api_key_name)
        if not self.api_key:
            raise ValueError(f"API key '{api_key_name}' not found in environment variables")
    
    def _initialize_provider(self):
        """Initialize the LLM provider"""
        return get_provider(
            provider_name=self.config['llm']['provider'],
            api_key=self.api_key,
            model=self.config['llm']['model'],
            temperature=self.config['llm']['temperature'],
            max_tokens=self.config['llm']['max_tokens']
        )
    
    def _ensure_output_folder(self):
        """Create output folder if it doesn't exist"""
        self.output_folder.mkdir(exist_ok=True)
        print(f"Output folder: {self.output_folder.absolute()}")
    
    def _parse_conversation_sets(self, generated_text: str) -> List[str]:
        """Parse individual conversation sets from generated text"""
        # Split by "Conversation Set" pattern
        pattern = r'Conversation Set \d+:'
        parts = re.split(pattern, generated_text)
        
        # Remove empty first part and reconstruct conversation sets
        conversation_sets = []
        matches = re.findall(pattern, generated_text)
        
        for i, match in enumerate(matches):
            if i + 1 < len(parts):
                conversation_set = match + parts[i + 1]
                conversation_sets.append(conversation_set.strip())
        
        return conversation_sets
    
    def _save_conversation_set(self, conversation_set: str, index: int):
        """Save a single conversation set to a markdown file with unique identifier"""
        # Extract title from conversation set for filename
        title_match = re.search(r'Conversation Set \d+:\s*(.+?)(?:\n|$)', conversation_set)
        if title_match:
            title = title_match.group(1).strip()
            # Clean title for filename
            clean_title = re.sub(r'[^\w\s-]', '', title)
            clean_title = re.sub(r'\s+', '_', clean_title)
            filename = f"conversation_set_{index:03d}_{clean_title[:50]}.md"
        else:
            filename = f"conversation_set_{index:03d}.md"
        
        filepath = self.output_folder / filename
        
        # Format conversation set as proper markdown
        formatted_content = self._format_as_markdown(conversation_set, index)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(formatted_content)
        
        print(f"Saved: {filename}")
        return filepath
    
    def _format_as_markdown(self, conversation_set: str, index: int) -> str:
        """Format conversation set as proper markdown with metadata"""
        # Extract the title
        title_match = re.search(r'Conversation Set \d+:\s*(.+?)(?:\n|$)', conversation_set)
        title = title_match.group(1).strip() if title_match else f"Conversation Set {index}"
        
        # Generate metadata header
        metadata = f"""# Conversation Set {index:03d}: {title}

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Provider:** {self.config['llm']['provider']}  
**Model:** {self.config['llm']['model']}  
**Temperature:** {self.config['llm']['temperature']}  

---

"""
        
        # Clean up and format the main content
        content = conversation_set.strip()
        
        # Replace section headers with proper markdown formatting
        content = re.sub(r'^User Motive:', '**User Motive:**', content, flags=re.MULTILINE)
        content = re.sub(r'^Domains & Subdomains:', '**Domains & Subdomains:**', content, flags=re.MULTILINE)
        content = re.sub(r'^Trajectory:', '**Trajectory:**', content, flags=re.MULTILINE)
        
        # Format tool lists
        content = re.sub(r'^Tools:', '**Tools:**', content, flags=re.MULTILINE)
        
        return metadata + content
    
    def generate_batch(self, batch_size: int, start_index: int = 1) -> List[str]:
        """Generate a batch of conversation sets"""
        # Generate dynamic system prompt based on current config
        system_prompt = get_conversation_generator_prompt(self.config_path)
        
        print(f"Generating batch of {batch_size} conversation sets...")
        print(f"Provider: {self.config['llm']['provider']} ({self.config['llm']['model']})")
        
        try:
            generated_text = self.provider.generate(
                system_prompt=system_prompt,
                user_prompt=""  # No separate user prompt needed
            )
            
            # Parse individual conversation sets
            conversation_sets = self._parse_conversation_sets(generated_text)
            
            # Save each conversation set
            saved_files = []
            for i, conversation_set in enumerate(conversation_sets):
                if conversation_set.strip():  # Only save non-empty sets
                    filepath = self._save_conversation_set(conversation_set, start_index + i)
                    saved_files.append(str(filepath))
            
            return saved_files
            
        except Exception as e:
            print(f"Error generating batch: {e}")
            return []
    
    def generate_all(self) -> Dict[str, Any]:
        """Generate all requested conversation sets"""
        total_sets = self.config['generation']['num_conversation_sets']
        batch_size = self.config['generation']['batch_size']
        
        print(f"Starting generation of {total_sets} conversation sets...")
        print(f"Batch size: {batch_size}")
        print("-" * 50)
        
        all_files = []
        generated_count = 0
        batch_count = 0
        
        while generated_count < total_sets:
            batch_count += 1
            remaining = total_sets - generated_count
            current_batch_size = min(batch_size, remaining)
            
            print(f"\nBatch {batch_count}: Generating {current_batch_size} sets...")
            
            batch_files = self.generate_batch(current_batch_size, generated_count + 1)
            all_files.extend(batch_files)
            generated_count += len(batch_files)
            
            print(f"Batch {batch_count} complete: {len(batch_files)} sets generated")
            print(f"Total progress: {generated_count}/{total_sets}")
            
            # Add delay between batches to respect API limits
            if generated_count < total_sets:
                delay = 2  # 2 second delay between batches
                print(f"Waiting {delay} seconds before next batch...")
                time.sleep(delay)
        
        # Generate summary for console display only
        summary = {
            "total_requested": total_sets,
            "total_generated": generated_count,
            "files_created": len(all_files),
            "output_folder": str(self.output_folder.absolute()),
            "provider": self.config['llm']['provider'],
            "model": self.config['llm']['model'],
            "generation_time": datetime.now().isoformat(),
            "files": all_files
        }
        
        print("\n" + "=" * 50)
        print("GENERATION COMPLETE!")
        print(f"Total conversation sets generated: {generated_count}")
        print(f"Files created: {len(all_files)}")
        print(f"Output folder: {self.output_folder.absolute()}")
        print(f"Provider: {self.config['llm']['provider']} ({self.config['llm']['model']})")
        print(f"Temperature: {self.config['llm']['temperature']}")
        print(f"Generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Export to Google Sheets if enabled (conversation sets only)
        self._export_to_google_sheets()
        
        print("=" * 50)
        
        return summary
    
    def _export_to_google_sheets(self):
        """Export conversation sets to Google Sheets if enabled"""
        google_sheets_config = self.config.get('google_sheets', {})
        
        if not google_sheets_config.get('enabled', False):
            print("📊 Google Sheets export is disabled")
            return
        
        print("\n🔄 Exporting to Google Sheets...")
        
        try:
            exporter = GoogleSheetsExporter(
                credentials_file=google_sheets_config.get('credentials_file', 'credentials.json')
            )
            
            spreadsheet_url = google_sheets_config.get('spreadsheet_url', '')
            
            # Export conversation sets only
            success = exporter.export_conversation_sets(
                conversation_sets_folder=str(self.output_folder),
                spreadsheet_url=spreadsheet_url if spreadsheet_url else None,
                worksheet_name=google_sheets_config.get('worksheet_name'),
                start_row=google_sheets_config.get('start_row', 2)
            )
            
            if success:
                print("✅ Google Sheets export completed successfully!")
            else:
                print("❌ Google Sheets export failed")
                
        except Exception as e:
            print(f"❌ Google Sheets export error: {e}")
            print("💡 You can manually export later using: python google_sheets_exporter.py")


def main():
    """Main function to run the conversation generator"""
    try:
        # Initialize generator
        generator = ConversationGenerator()
        
        # Generate all conversation sets
        summary = generator.generate_all()
        
        return summary
        
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    main()
