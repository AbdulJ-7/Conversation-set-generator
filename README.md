# Function Calling Conversation Generator

A comprehensive tool for generating complex function calling conversation sets using various Large Language Models (OpenAI GPT, Anthropic Claude, Google Gemini) to assist human annotators in creating training data.

## Features

- **Multi-LLM Support**: OpenAI GPT-4o, Anthropic Claude, Google Gemini
- **Configurable Generation**: Customize number of sets, temperature, batch size
- **Interactive Configuration**: Easy setup with guided configuration
- **Batch Processing**: Efficient generation with API rate limiting
- **Structured Output**: Well-formatted conversation sets with metadata
- **Robust Error Handling**: Graceful handling of API errors and retries

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   Edit the `.env` file and add your API key(s):
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Configure Settings**
   ```bash
   python config_manager.py
   ```
   This will launch an interactive configuration wizard.

4. **Generate Conversation Sets**
   ```bash
   python conversation_generator.py
   ```

5. **Export to Google Sheets (Optional)**
   ```bash
   # Enable in config first, then generate
   python config_manager.py  # Enable Google Sheets export
   python conversation_generator.py  # Auto-exports to Google Sheets
   
   # Or export manually
   python google_sheets_exporter.py
   ```

## Configuration Options

### LLM Settings
- **Provider**: Choose between `openai`, `anthropic`, or `google`
- **Model**: Select specific model (e.g., `gpt-4o`, `claude-3-5-sonnet-20241022`, `gemini-1.5-pro`)
- **Temperature**: Control creativity (0.0 - 1.0)
- **Max Tokens**: Maximum response length

### Generation Settings
- **Number of Sets**: How many conversation sets to generate
- **Batch Size**: Sets per API call (affects performance and cost)

### Google Sheets Export
- **Enabled**: Toggle automatic export to Google Sheets
- **Spreadsheet Title**: Name of the Google Sheets spreadsheet
- **Credentials File**: Path to Google service account credentials
- **Export Summary**: Include generation summary worksheet
- **Output Folder**: Where to save generated files

## Available Function Calling Tools

The generator creates conversations using these tools:
- `yahoo_finance` - Stock prices and financial data
- `arxiv` - Academic papers and research
- `github` - Code repositories and projects
- `google_places` - Location-based searches
- `current_time` - Time in different locations
- `pubmed` - Medical/scientific literature
- `search` - General web search
- `meal_db` - Recipe and food information
- `calculator` - Mathematical calculations
- `steam` - Gaming information
- `youtube_search` - Finding videos
- `youtube_summarize` - Video summaries
- `weather` - Weather information
- `email_sender` - Email functionality
- `wiki` - Wikipedia articles
- `google_trends` - Search trends
- `tmdb` - Movie/TV information

## Google Sheets Export

The generator can automatically export conversation sets to Google Sheets for easy collaboration and analysis.

### Setup Google Sheets Export

1. **Follow the setup guide**: See `GOOGLE_SHEETS_SETUP.md` for detailed instructions
2. **Enable in config**: Run `python config_manager.py` and enable Google Sheets export
3. **Add credentials**: Download `credentials.json` from Google Cloud Console
4. **Generate and export**: Run `python conversation_generator.py` for automatic export

### What Gets Exported

- **Conversation Sets Worksheet**: All conversation data in structured columns
- **Generation Summary Worksheet**: Metadata and file statistics
- **Automatic Formatting**: Headers, colors, and proper data types

### Manual Export

```bash
# Export existing conversation sets
python google_sheets_exporter.py

# Test Google Sheets setup
python tests/test_google_sheets.py
```

## Example Output

Each generated conversation set includes:
- **User Motive**: Clear persona and goals
- **Domains & Subdomains**: Areas being explored
- **Trajectory**: Multi-turn conversation flow
- **Tool Usage**: Specific tools for each turn

Example structure:
```
Conversation Set 1: The Tech Investor's Deep Dive
User Motive: A sophisticated investor conducting due diligence...
Domains & Subdomains: Technology & Gadgets, Finance, E-Commerce
Trajectory:
1. Analyze Apple Inc. stock and M-series chip research...
   Tools: yahoo_finance, arxiv, github
2. Compare with Google's Alphabet performance...
   Tools: yahoo_finance, pubmed, search
...
```

## File Structure

```
prompt_generator/
├── conversation_generator.py    # Main generation script
├── config_manager.py           # Interactive configuration
├── llm_providers.py            # LLM provider implementations
├── prompts.py                  # System prompts and templates
├── config.yaml                 # Configuration file
├── .env                        # API keys (create this)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── conversation_sets/          # Generated output (created automatically)
    ├── conversation_set_001_*.txt
    ├── conversation_set_002_*.txt
    └── generation_summary.json
```

## Usage Examples

### Basic Usage
```bash
# Use default configuration
python conversation_generator.py
```

### Custom Configuration
```bash
# Interactive setup
python config_manager.py

# Then generate
python conversation_generator.py
```

### Different LLM Providers

**OpenAI GPT-4o:**
```yaml
llm:
  provider: "openai"
  model: "gpt-4o"
  temperature: 0.7
```

**Anthropic Claude:**
```yaml
llm:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.7
```

**Google Gemini:**
```yaml
llm:
  provider: "google"
  model: "gemini-1.5-pro"
  temperature: 0.7
```

## Output Files

Generated conversation sets are saved in the specified output folder with:
- **Individual Files**: Each conversation set in a separate `.txt` file
- **Metadata Headers**: Generation timestamp, model info, settings
- **Summary File**: `generation_summary.json` with batch statistics
- **Descriptive Filenames**: Based on conversation set titles

## Error Handling

The tool includes robust error handling for:
- API rate limits and timeouts
- Invalid API keys
- Network connectivity issues
- Malformed responses
- Configuration errors

## Cost Considerations

- **Batch Size**: Smaller batches = more API calls but better error recovery
- **Max Tokens**: Higher values increase cost per request
- **Model Choice**: Different models have different pricing
- **Temperature**: Doesn't affect cost but affects output quality

## Contributing

Feel free to extend the tool by:
- Adding new LLM providers to `llm_providers.py`
- Enhancing prompts in `prompts.py`
- Adding new configuration options
- Improving error handling and logging

## License

This project is open source and available under the MIT License.
