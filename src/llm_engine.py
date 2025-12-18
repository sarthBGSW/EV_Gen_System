import os
import requests
import json
from openai import AzureOpenAI, OpenAI
from src.config import Config

class ModelFactory:
    def __init__(self):
        # 1. Setup Azure OpenAI Client (For GPT-5 & Grok if hosted on Azure OpenAI standard)
        self.azure_client = AzureOpenAI(
            api_key=Config.AZURE_AI_KEY,
            api_version=Config.AZURE_API_VERSION,
            azure_endpoint=Config.AZURE_ENDPOINT
        )
        
        # 2. Setup Ollama Client (Local)
        self.ollama_client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama" # Required but unused
        )

    def generate(self, model_name, prompt, system_role="You are an expert analyst.", temperature=0.7):
        """
        Universal function to call ANY model (Azure, Claude-Special, or Local)
        """
        print(f"🤖 Calling Model: {model_name}...")

        try:
            # --- ROUTE 1: AZURE CLAUDE (Special REST API) ---
            if "claude" in model_name.lower():
                headers = {
                    "x-api-key": Config.AZURE_ANTHROPIC_KEY,
                    "content-type": "application/json",
                    "anthropic-version": Config.AZURE_ANTHROPIC_VERSION
                }
                # Claude uses system as a top-level parameter, not in messages
                payload = {
                    "model": model_name,
                    "max_tokens": 4096,
                    "system": system_role,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
                # Azure Anthropic endpoints usually differ slightly, using requests for raw control
                response = requests.post(Config.AZURE_ANTHROPIC_ENDPOINT, headers=headers, json=payload)
                if response.status_code == 200:
                    return response.json()['content'][0]['text']
                else:
                    return f"Error Claude: {response.text}"

            # For other models, use standard message format with system role
            messages = [
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ]

            # --- ROUTE 2: LOCAL OLLAMA ---
            if model_name in [Config.LOCAL_DEEPSEEK, Config.LOCAL_LLAMA, Config.LOCAL_MISTRAL]:
                try:
                    response = self.ollama_client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        temperature=temperature
                    )
                    return response.choices[0].message.content
                except Exception as ollama_error:
                    return f"❌ Local Model Error ({model_name}): Cannot connect to Ollama. Make sure Ollama is running locally at http://localhost:11434. Note: Local models don't work on Streamlit Cloud. Error: {str(ollama_error)}"

            # --- ROUTE 3: AZURE OPENAI STANDARD (GPT-5, GROK) ---
            else:
                # GPT-5-mini only supports temperature=1 (default)
                # Other models can use custom temperature
                if "gpt-5" in model_name.lower():
                    response = self.azure_client.chat.completions.create(
                        model=model_name, 
                        messages=messages
                        # No temperature parameter for GPT-5
                    )
                else:
                    # For Grok and other models
                    response = self.azure_client.chat.completions.create(
                        model=model_name, 
                        messages=messages,
                        temperature=temperature
                    )
                return response.choices[0].message.content

        except Exception as e:
            return f"❌ Model Generation Error ({model_name}): {str(e)}"

# Test function
if __name__ == "__main__":
    engine = ModelFactory()
    # Test Local
    print(engine.generate(Config.LOCAL_LLAMA, "Hello, who are you?"))