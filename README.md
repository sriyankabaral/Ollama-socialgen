# SocialGen

A beginner-friendly command-line social media content generator using local Ollama models.

## Features

- Prompts for platform, topic, and tone
- Supports Meta, Instagram, LinkedIn, and YouTube
- Generates a social media post using local Ollama models (free and offline)
- Keeps configuration private using `.env`

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

3. Configure `.env` for Ollama:

   ```text
   API_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   MODEL_NAME=tinyllama
   ```

   Or use another local Ollama model you have installed.

## Usage

1. Start Ollama server:
   ```powershell
   ollama serve
   ```

2. In another terminal, download the model if needed:
   ```powershell
   ollama pull tinyllama
   ```

3. Run the generator:
   ```powershell
   python socialgen.py
   ```

Then enter:
- Platform: Meta, Instagram, LinkedIn, or YouTube
- Topic: what the post should be about
- Tone: e.g. professional, friendly, fun

## Notes

- No external API key is required for Ollama.
- The script exits with an error if configuration is missing.
- Ollama runs completely offline and is free.
