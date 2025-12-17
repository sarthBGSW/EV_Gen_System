import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Auth
    AZURE_AI_KEY = os.getenv("AZURE_AI_KEY")
    AZURE_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
    AZURE_ANTHROPIC_KEY = os.getenv("AZURE_ANTHROPIC_KEY")
    AZURE_ANTHROPIC_ENDPOINT = os.getenv("AZURE_ANTHROPIC_ENDPOINT")
    
    # API Versions
    AZURE_API_VERSION = "2024-05-01-preview"  # For GPT-5 and Grok
    AZURE_ANTHROPIC_VERSION = "2023-06-01"    # For Claude
    
    # Model Names (Deployment Names in Azure)
    MODEL_GPT5 = "gpt-5-mini"
    MODEL_GROK4 = "grok-4-fast-reasoning"
    MODEL_CLAUDE = "claude-sonnet-4-5"
    
    # Full Endpoints with API versions
    GPT5_ENDPOINT = f"{os.getenv('AZURE_AI_ENDPOINT')}openai/deployments/gpt-5-mini/chat/completions?api-version=2024-05-01-preview"
    GROK4_ENDPOINT = f"{os.getenv('AZURE_AI_ENDPOINT')}openai/deployments/grok-4-fast-reasoning/chat/completions?api-version=2024-05-01-preview"
    
    # Local Models
    LOCAL_LLAMA = "llama3.2:latest"
    LOCAL_DEEPSEEK = "deepseek-r1:8b"
    LOCAL_MISTRAL = "mistral:latest"