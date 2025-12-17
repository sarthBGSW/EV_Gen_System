# EV Business Field Analysis System 🚗⚡

An AI-powered multi-agent system for generating comprehensive Electric Vehicle (EV) industry analysis reports using LangGraph orchestration.

## Features

- **Multi-Model Support**: Integrates GPT-5, Claude Sonnet, Grok-4, and local models (Llama, DeepSeek, Mistral)
- **LangGraph Workflow**: Orchestrated multi-agent system with research, drafting, and critique nodes
- **Real-time Web Search**: DuckDuckGo integration for latest EV market data
- **Iterative Refinement**: Configurable debate cycles for quality improvement
- **Streamlit UI**: Interactive web interface with live progress tracking

## Architecture

```
Research Agent → Draft Agent → Critique Agent → [Loop] → Final Report
```

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd EV_Gen_System
```

### 2. Create Virtual Environment

```bash
conda create -n EV python=3.11
conda activate EV
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
- Azure OpenAI endpoint and key (for GPT-5, Grok-4)
- Azure Anthropic endpoint and key (for Claude Sonnet)
- Ollama URL (if using local models)

### 5. Run the Application

```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

## Project Structure

```
EV_Gen_System/
├── app.py                 # Main Streamlit application
├── src/
│   ├── config.py         # Configuration and model settings
│   ├── llm_engine.py     # Multi-model LLM interface
│   ├── search_tools.py   # Web search and scraping tools
│   ├── graph_workflow.py # LangGraph workflow definition
│   └── __init__.py
├── storage/              # Generated reports (gitignored)
├── .env                  # Environment variables (gitignored)
├── .env.example          # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Usage

1. Select your preferred AI models from the sidebar:
   - **Drafting Agent**: GPT-5, Claude, or Local Llama
   - **Critique Agent**: DeepSeek or Grok-4

2. Set the number of debate iterations (1-5)

3. Enter your analysis scope (e.g., "EV Battery Swapping Trends in India 2025")

4. Watch the multi-agent system work:
   - Research phase gathers latest data
   - Draft agent creates initial analysis
   - Critic agent provides feedback
   - System iterates to improve quality

5. Download the final report as markdown

## Models Supported

### Cloud Models
- **GPT-5 Mini** (Azure OpenAI)
- **Grok-4 Fast Reasoning** (Azure OpenAI)
- **Claude Sonnet 4.5** (Azure Anthropic)

### Local Models (via Ollama)
- Llama 3.2
- DeepSeek R1 8B
- Mistral

## Dependencies

- streamlit
- langgraph
- langchain-community
- openai
- anthropic
- requests
- beautifulsoup4
- python-dotenv
- ddgs (DuckDuckGo search)

## Security Notes

⚠️ **Never commit your `.env` file!** It contains sensitive API keys.

- Use `.env.example` as a template
- Add `.env` to `.gitignore` (already included)
- For Streamlit Cloud deployment, use Streamlit Secrets management

## Deployment on Streamlit Community Cloud

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your environment variables in **Secrets** (Settings > Secrets)
5. Deploy!

### Streamlit Secrets Format

In Streamlit Cloud, add secrets in TOML format:

```toml
AZURE_AI_ENDPOINT = "https://your-resource.cognitiveservices.azure.com/"
AZURE_AI_KEY = "your-key-here"
AZURE_ANTHROPIC_ENDPOINT = "https://your-resource.services.ai.azure.com/anthropic/v1/messages"
AZURE_ANTHROPIC_KEY = "your-key-here"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
```

## Contributing

Contributions welcome! Please ensure:
- No API keys in commits
- Code follows existing structure
- Test before submitting PR

## License

MIT License

## Author

Developed for EV Business Field Analysis - December 2025
