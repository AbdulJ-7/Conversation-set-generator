"""
Interactive configuration tool for the Function Calling Conversation Generator
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages configuration for the conversation generator"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load existing configuration or create default"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'llm': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.7,
                'max_tokens': 4000
            },
            'generation': {
                'num_conversation_sets': 100,
                'output_folder': 'conversation_sets',
                'batch_size': 5
            },
            'models': {
                'openai': ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo'],
                'anthropic': ['claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 'claude-3-opus-20240229'],
                'google': ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
            },
            'available_tools': [
                'yahoo_finance', 'arxiv', 'github', 'google_places', 'current_time',
                'pubmed', 'search', 'meal_db', 'calculator', 'steam',
                'youtube_search', 'youtube_summarize', 'weather', 'email_sender',
                'wiki', 'google_trends', 'tmdb'
            ],
            'example_conversation_file': 'conversation_sets/example_conversation_set.md',
            'google_sheets': {
                'enabled': False,
                'spreadsheet_title': 'Function Calling Conversation Sets',
                'credentials_file': 'credentials.json',
                'export_summary': True
            }
        }
    
    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file, default_flow_style=False, sort_keys=False)
        print(f"Configuration saved to {self.config_path}")
    
    def interactive_setup(self):
        """Interactive configuration setup"""
        print("=" * 60)
        print("Function Calling Conversation Generator - Configuration")
        print("=" * 60)
        
        # LLM Provider Selection
        print("\n1. LLM Provider Selection:")
        providers = list(self.config['models'].keys())
        for i, provider in enumerate(providers, 1):
            current = " (current)" if provider == self.config['llm']['provider'] else ""
            print(f"   {i}. {provider.title()}{current}")
        
        try:
            choice = input(f"\nSelect provider (1-{len(providers)}) [current: {self.config['llm']['provider']}]: ").strip()
            if choice and choice.isdigit() and 1 <= int(choice) <= len(providers):
                selected_provider = providers[int(choice) - 1]
                self.config['llm']['provider'] = selected_provider
                print(f"Selected provider: {selected_provider}")
        except (ValueError, IndexError):
            print("Invalid selection, keeping current provider")
        
        # Model Selection
        current_provider = self.config['llm']['provider']
        available_models = self.config['models'][current_provider]
        
        print(f"\n2. Model Selection for {current_provider.title()}:")
        for i, model in enumerate(available_models, 1):
            current = " (current)" if model == self.config['llm']['model'] else ""
            print(f"   {i}. {model}{current}")
        
        try:
            choice = input(f"\nSelect model (1-{len(available_models)}) [current: {self.config['llm']['model']}]: ").strip()
            if choice and choice.isdigit() and 1 <= int(choice) <= len(available_models):
                selected_model = available_models[int(choice) - 1]
                self.config['llm']['model'] = selected_model
                print(f"Selected model: {selected_model}")
        except (ValueError, IndexError):
            print("Invalid selection, keeping current model")
        
        # Temperature Setting
        print(f"\n3. Temperature Setting (0.0 - 1.0):")
        print(f"   Current: {self.config['llm']['temperature']}")
        print("   Lower values = more focused, Higher values = more creative")
        
        temp_input = input(f"Enter temperature [current: {self.config['llm']['temperature']}]: ").strip()
        if temp_input:
            try:
                temperature = float(temp_input)
                if 0.0 <= temperature <= 1.0:
                    self.config['llm']['temperature'] = temperature
                    print(f"Temperature set to: {temperature}")
                else:
                    print("Temperature must be between 0.0 and 1.0, keeping current value")
            except ValueError:
                print("Invalid temperature value, keeping current value")
        
        # Number of Conversation Sets
        print(f"\n4. Number of Conversation Sets:")
        print(f"   Current: {self.config['generation']['num_conversation_sets']}")
        
        num_input = input(f"Enter number of sets [current: {self.config['generation']['num_conversation_sets']}]: ").strip()
        if num_input:
            try:
                num_sets = int(num_input)
                if num_sets > 0:
                    self.config['generation']['num_conversation_sets'] = num_sets
                    print(f"Number of sets set to: {num_sets}")
                else:
                    print("Number must be positive, keeping current value")
            except ValueError:
                print("Invalid number, keeping current value")
        
        # Batch Size
        print(f"\n5. Batch Size (sets per API call):")
        print(f"   Current: {self.config['generation']['batch_size']}")
        print("   Smaller batches = more API calls but better error recovery")
        
        batch_input = input(f"Enter batch size [current: {self.config['generation']['batch_size']}]: ").strip()
        if batch_input:
            try:
                batch_size = int(batch_input)
                if batch_size > 0:
                    self.config['generation']['batch_size'] = batch_size
                    print(f"Batch size set to: {batch_size}")
                else:
                    print("Batch size must be positive, keeping current value")
            except ValueError:
                print("Invalid batch size, keeping current value")
        
        # Output Folder
        print(f"\n6. Output Folder:")
        print(f"   Current: {self.config['generation']['output_folder']}")
        
        folder_input = input(f"Enter output folder name [current: {self.config['generation']['output_folder']}]: ").strip()
        if folder_input:
            self.config['generation']['output_folder'] = folder_input
            print(f"Output folder set to: {folder_input}")
        
        # Max Tokens
        print(f"\n7. Max Tokens:")
        print(f"   Current: {self.config['llm']['max_tokens']}")
        print("   Higher values allow longer responses but cost more")
        
        tokens_input = input(f"Enter max tokens [current: {self.config['llm']['max_tokens']}]: ").strip()
        if tokens_input:
            try:
                max_tokens = int(tokens_input)
                if max_tokens > 0:
                    self.config['llm']['max_tokens'] = max_tokens
                    print(f"Max tokens set to: {max_tokens}")
                else:
                    print("Max tokens must be positive, keeping current value")
            except ValueError:
                print("Invalid max tokens value, keeping current value")
        
        # Google Sheets Export
        print(f"\n8. Google Sheets Export:")
        print(f"   Current status: {'Enabled' if self.config.get('google_sheets', {}).get('enabled', False) else 'Disabled'}")
        print("   Automatically export conversation sets to Google Sheets")
        
        sheets_choice = input("Enable Google Sheets export? (y/n) [n]: ").strip().lower()
        if sheets_choice == 'y':
            if 'google_sheets' not in self.config:
                self.config['google_sheets'] = {}
            
            self.config['google_sheets']['enabled'] = True
            
            # Spreadsheet title
            current_title = self.config['google_sheets'].get('spreadsheet_title', 'Function Calling Conversation Sets')
            title_input = input(f"Spreadsheet title [current: {current_title}]: ").strip()
            if title_input:
                self.config['google_sheets']['spreadsheet_title'] = title_input
            
            # Credentials file
            current_creds = self.config['google_sheets'].get('credentials_file', 'credentials.json')
            creds_input = input(f"Credentials file path [current: {current_creds}]: ").strip()
            if creds_input:
                self.config['google_sheets']['credentials_file'] = creds_input
            
            print("✅ Google Sheets export enabled!")
            print("💡 Make sure to configure your Google Cloud credentials (see setup instructions)")
        else:
            if 'google_sheets' not in self.config:
                self.config['google_sheets'] = {}
            self.config['google_sheets']['enabled'] = False
            print("Google Sheets export disabled")
        
        # Example Conversation Set
        print(f"\n9. Example Conversation Set:")
        print("   This is used as a reference in the generated prompts")
        if 'example_conversation_set' in self.config:
            example_preview = self.config['example_conversation_set'][:200] + "..." if len(self.config['example_conversation_set']) > 200 else self.config['example_conversation_set']
            print(f"   Current: {example_preview}")
        else:
            print("   Current: Using default example")
        
        edit_example = input("Would you like to edit the example conversation set? (y/n) [n]: ").strip().lower()
        if edit_example == 'y':
            print("\nPaste your new example conversation set (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "" and len(lines) > 0 and lines[-1] == "":
                    break
                lines.append(line)
            
            if lines:
                # Remove the last empty line if it exists
                if lines and lines[-1] == "":
                    lines.pop()
                new_example = '\n'.join(lines)
                if new_example.strip():
                    self.config['example_conversation_set'] = new_example.strip()
                    print("Example conversation set updated!")
                else:
                    print("No content entered, keeping current example")
            else:
                print("No content entered, keeping current example")
        
        # Summary
        print("\n" + "=" * 60)
        print("CONFIGURATION SUMMARY:")
        print("=" * 60)
        print(f"Provider: {self.config['llm']['provider']}")
        print(f"Model: {self.config['llm']['model']}")
        print(f"Temperature: {self.config['llm']['temperature']}")
        print(f"Max Tokens: {self.config['llm']['max_tokens']}")
        print(f"Conversation Sets: {self.config['generation']['num_conversation_sets']}")
        print(f"Batch Size: {self.config['generation']['batch_size']}")
        print(f"Output Folder: {self.config['generation']['output_folder']}")
        print(f"Available Tools: {len(self.config.get('available_tools', []))} tools configured")
        print(f"Example Conversation: {'Custom' if 'example_conversation_set' in self.config else 'Default'}")
        print("=" * 60)
        
        # Save confirmation
        save_choice = input("\nSave this configuration? (y/n) [y]: ").strip().lower()
        if save_choice != 'n':
            self.save_config()
            return True
        else:
            print("Configuration not saved")
            return False
    
    def check_api_keys(self):
        """Check if required API keys are set"""
        from dotenv import load_dotenv
        load_dotenv()
        
        provider = self.config['llm']['provider']
        api_key_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'google': 'GOOGLE_API_KEY'
        }
        
        required_key = api_key_map.get(provider)
        if not required_key:
            print(f"Unknown provider: {provider}")
            return False
        
        api_key = os.getenv(required_key)
        if not api_key or api_key == f"your_{provider}_api_key_here":
            print(f"\n⚠️  WARNING: {required_key} not found or not set properly!")
            print(f"Please add your {provider.title()} API key to the .env file:")
            print(f"{required_key}=your_actual_api_key_here")
            return False
        
        print(f"✅ {required_key} is configured")
        return True


def main():
    """Main function for configuration management"""
    config_manager = ConfigManager()
    
    # Interactive setup
    if config_manager.interactive_setup():
        print("\n✅ Configuration completed successfully!")
        
        # Check API keys
        print("\nChecking API key configuration...")
        if config_manager.check_api_keys():
            print("✅ API key is properly configured")
            print("\nYou can now run: python conversation_generator.py")
        else:
            print("❌ Please configure your API key before running the generator")
    else:
        print("Configuration cancelled")


if __name__ == "__main__":
    main()
