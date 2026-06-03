# SocialGen

A beginner-friendly command-line social media content generator using LangChain and your choice of API providers.

## Features

- Prompts for platform, topic, and tone
- Supports Meta, Instagram, LinkedIn, and YouTube
- Generates a social media post using your choice of:
  - **OpenAI** (ChatGPT via API)
  - **NVIDIA** (free API endpoint)
  - **Ollama** (local 8B models, completely free and offline)
- Keeps API keys private using `.env`

## Setup

1. Create a virtual environment (recommended):

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Configure `.env` for your chosen provider:

   ### Option A: OpenAI
   ```text
   API_PROVIDER=openai
   API_KEY=your_openai_api_key_here
   MODEL_NAME=openai:gpt-4o-mini
   ```

   ### Option B: NVIDIA Free API
   ```text
   API_PROVIDER=nvidia
   API_KEY=your_nvidia_api_key_here
   NVIDIA_API_URL=https://api.nvidia.com/v1/chat/completions
   MODEL_NAME=nvidia-model-name
   ```

   ### Option C: Ollama (Local - Recommended for Free & Offline)
   First, install Ollama from [ollama.ai](https://ollama.ai), then:
   ```text
   API_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   MODEL_NAME=llama2:8b
   ```

   Available 8B models on Ollama:
   - `llama2:8b`
   - `mistral:8b`
   - `neural-chat:8b`
   - `zephyr:8b`
   - `orca:8b`

## Usage

### Using Ollama
1. Start Ollama server:
   ```powershell
   ollama serve
   ```

2. In another terminal, download your model:
   ```powershell
   ollama pull llama2:8b
   ```

3. Run the generator:
   ```powershell
   python socialgen.py
   ```

### Using OpenAI or NVIDIA
Just run:
```powershell
python socialgen.py
```

Then enter:
- Platform: Meta, Instagram, LinkedIn, or YouTube
- Topic: what the post should be about
- Tone: e.g. professional, friendly, fun

## Notes

- API keys are never printed or exposed.
- The script exits with an error if configuration is missing.
- Ollama runs completely offline and is free.
