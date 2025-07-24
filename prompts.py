"""
System prompts for generating function calling conversation sets
"""

import yaml
from typing import Dict, Any, List


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        # Return default config if file not found
        return {
            'generation': {'num_conversation_sets': 10, 'batch_size': 5},
            'available_tools': ['yahoo_finance', 'arxiv', 'github', 'google_places', 'current_time'],
            'example_conversation_file': 'conversation_sets/example_conversation_set.md'
        }


def load_example_conversation(example_file_path: str) -> str:
    """Load example conversation from external markdown file"""
    try:
        with open(example_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Remove the markdown header and extract the conversation content
            lines = content.split('\n')
            # Skip the first line (# Example Conversation Set) and join the rest
            return '\n'.join(lines[2:]).strip()
    except FileNotFoundError:
        return get_default_example()
    except Exception:
        return get_default_example()


def format_tools_list(tools: List[str]) -> str:
    """Format the tools list for inclusion in the prompt"""
    formatted_tools = []
    tool_descriptions = {
        'amadeus_travel': 'Flight, hotel, and travel-related information',
        'arxiv_search': 'Academic papers and preprints',
        'calculator': 'Mathematical and statistical calculations',
        'current_time': 'Time across time zones',
        'email_sender': 'Send email messages to recipients',
        'github': 'Code repositories and developer projects',
        'google_places': 'Search for locations, landmarks, and businesses',
        'google_trends': 'Search trend analysis over time',
        'mealdb_food': 'Recipe lookup and nutritional info',
        'pubmed': 'Scientific and medical research papers',
        'search_brave': 'General web search using Brave',
        'steam': 'Video game information and store data',
        'tmdb_movies': 'Movie and TV series metadata',
        'weather': 'Current weather and forecasts',
        'wikipedia': 'General knowledge from Wikipedia articles',
        'yahoo_finance': 'Stock prices, tickers, and financial data',
        'youtube_search': 'Find videos on YouTube',
        'youtube_summarizer': 'Summarize YouTube video content'
    }
    
    for tool in tools:
        description = tool_descriptions.get(tool, 'Tool description not available')
        formatted_tools.append(f"   - {tool}: {description}")
    
    return '\n'.join(formatted_tools)


def get_conversation_generator_prompt(config_path: str = "config.yaml") -> str:
    """Generate the dynamic system prompt based on configuration"""
    config = load_config(config_path)
    
    # Extract configuration values
    num_sets = config.get('generation', {}).get('batch_size', 5)
    total_sets = config.get('generation', {}).get('num_conversation_sets', 100)
    available_tools = config.get('available_tools', [])
    example_file = config.get('example_conversation_file', 'conversation_sets/example_conversation_set.md')
    example_conversation = load_example_conversation(example_file)
    
    # Format the tools list
    tools_list = format_tools_list(available_tools)
    
    return f"""You are an expert at creating complex, realistic function calling conversation sets for training AI assistants. Your task is to generate {num_sets} sophisticated multi-turn conversations that demonstrate advanced function calling patterns.

REQUIREMENTS:
1. Each conversation set must include:
   - A clear user motive/persona (e.g., tech investor, researcher, content creator, etc.)
   - Multiple domains and subdomains being explored
   - A logical trajectory of atleast 6 turns that build upon each other
   - Realistic tool combinations that make sense for the user's goals
   - Specific, detailed requests that would require function calls

2. Available tools to use in conversations:
{tools_list}
   - Do not reference or use tools from any examples that are not in this list.

3. Conversation complexity requirements:
   - Each turn must involve at least 4 sequential API calls
   - Mix different tool types within each turn where relevant, though repeated use of the same API within a turn is also allowed when necessary.
   - Create logical dependencies between turns
   - Ensure that each individual API call includes fewer than 5 arguments
   - Include both direct and indirect information gathering
   - Demonstrate realistic user behavior and decision-making
   - Vary the depth and breadth of exploration

4. Persona variety:
   - Business professionals (investors, analysts, executives)
   - Researchers (academic, market, technical)
   - Content creators (writers, YouTubers, journalists)
   - Consumers (shoppers, travelers, hobbyists)
   - Students and educators
   - Healthcare professionals
   - Tech enthusiasts and developers

5. Turn Construction rules:
   - Incorporate all required API parameters naturally within user queries
   - Do not fabricate identifiers like team IDs, video IDs, or user IDs
   - Use realistic but fabricated data for parameters such as dates, distances, quantities, locations (e.g., "on June 21, 2025" instead of "a month ago"; "Indiranagar, Bangalore" instead of "some address")
   - Avoid vague phrases like "a protein-rich meal"—instead, use precise values (e.g., "over 35% protein")
   - Do not explicitly mention or reference tool/API names in the conversation itself
   - Prompts must not instruct the assistant on the specific sequence or grouping of API calls. Instead, write user queries that are natural, complete, and practical, allowing the assistant to infer the correct order and grouping based on the user’s intent.
   - For example:
        Ideal:
        "I'm planning a trip to Rome, Italy. Find the cheapest round-trip flight from Boston to Rome for two weeks next September. Find the highest rated restaurant near the Colosseum which serves Mediterranean food. Look for the weather forecast on the day I land. If it’s not rainy, suggest 3 historical places to visit and summarize their significance."

        Avoid:
        "First, find a round-trip flight from Boston to Rome for next May. Then, find a Wikipedia article on the Roman Forum. Next, find a highly-rated restaurant near the Colosseum…”




6. Format requirements:
   - Start with "Conversation Set X:" followed by a descriptive title
   - Include "User Motive:" explaining the user's goals and context
   - List "Domains & Subdomains:" being explored
   - Provide "Trajectory:" with atleast 6 detailed turns
   - End each turn with "Tools:" listing the specific tools used
   - Make each turn feel natural and conversational

EXAMPLE CONVERSATION SET:
{example_conversation}

GENERATION INSTRUCTIONS:
Generate {num_sets} unique, complex function calling conversation sets following the rules andn format above. Each conversation set should:
- Explore different domain combinations
- Demonstrate unique tool usage patterns
- Have atleast 6 conversational turns that build logically

Ensure variety in:
- User personas (investors, researchers, creators, consumers, etc.)
- Domain combinations (tech + finance, health + research, etc.)
- Tool usage patterns and complexity
- Conversation flow and dependencies

Number each conversation set sequentially and make each one distinct and valuable for training purposes. Generate conversation sets that are sophisticated, realistic, natural and demonstrate complex function calling patterns that would challenge and train an AI assistant effectively."""


def get_default_example() -> str:
    """Get the default example conversation set"""
    return '''Conversation Set 6: The Tech Investor's Deep Dive
User Motive: The user is a sophisticated investor conducting thorough due diligence on a potential technology investment. They want to go beyond surface-level metrics, aiming to connect financial performance with technological innovation, market trends, academic research, and the key people driving the company. Their goal is to build a holistic, multi-faceted view of the company's long-term potential.
Domains & Subdomains:
Technology & Gadgets: Artificial Intelligence, Software Development Tools, Tech Events & Conferences
Finance: (via Yahoo Finance)
E-Commerce: Personalization
Trajectory:
I want to analyze major tech companies. Let's start with Apple Inc. Find its current stock ticker and price. Find a recent academic paper on the impact of their M-series chips on machine learning performance. Next, locate a major open-source machine learning project on a code repository that is optimized for their hardware. Also, find a nearby store where I could see their latest products. Finally, check the current time in Cupertino to see if their corporate office is open.
Tools: yahoo_finance, arxiv, github, google_places, current_time
That's a good start. Now, check Google's parent company, Alphabet. Get their stock price. Then, search for a recent medical study that utilized Google's DeepMind AI for diagnostics. Next, find the official website for their upcoming I/O conference. Also, find a popular recipe for an "Android green" smoothie. Lastly, calculate the value of 75 Alphabet shares based on the current price.
Tools: yahoo_finance, pubmed, search, meal_db, calculator'''
