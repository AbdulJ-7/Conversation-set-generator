"""
LLM Providers module for handling different AI model APIs
"""

import os
from typing import Dict, Any, Optional
import openai
import anthropic
import google.generativeai as genai


class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 4000):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text using the LLM"""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 4000):
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 4000):
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")


class GoogleProvider(LLMProvider):
    """Google Gemini provider"""
    
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 4000):
        super().__init__(api_key, model, temperature, max_tokens)
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)
        
        # Configure generation parameters
        self.generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            # Combine system and user prompts for Gemini
            combined_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
            
            response = self.model_instance.generate_content(
                combined_prompt,
                generation_config=self.generation_config
            )
            return response.text
        except Exception as e:
            raise Exception(f"Google API error: {str(e)}")


def get_provider(provider_name: str, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 4000) -> LLMProvider:
    """Factory function to get the appropriate LLM provider"""
    
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unsupported provider: {provider_name}. Available providers: {list(providers.keys())}")
    
    return providers[provider_name](api_key, model, temperature, max_tokens)
