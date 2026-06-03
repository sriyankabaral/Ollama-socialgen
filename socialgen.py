#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from openai import OpenAIError, RateLimitError

# Load environment variables from .env file
load_dotenv()

API_PROVIDER = os.getenv("API_PROVIDER", "openai").strip().lower()
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "openai:gpt-4o-mini")
NVIDIA_API_URL = os.getenv("NVIDIA_API_URL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

if API_PROVIDER != "ollama" and (not API_KEY or API_KEY == "your_api_key_here"):
    print("Error: API_KEY is missing or still the placeholder. Please add your API key to the .env file.")
    raise SystemExit(1)

if API_PROVIDER not in {"openai", "nvidia", "ollama"}:
    print("Error: API_PROVIDER must be either 'openai', 'nvidia', or 'ollama'.")
    raise SystemExit(1)

# Supported social media platforms
SUPPORTED_PLATFORMS = ["Meta", "Instagram", "LinkedIn", "YouTube"]


def get_platform() -> str:
    """Ask the user to choose a supported platform."""
    print("Choose a social media platform:")
    for index, platform in enumerate(SUPPORTED_PLATFORMS, start=1):
        print(f"{index}. {platform}")

    while True:
        choice = input("Enter the number or name of the platform: ").strip()

        if choice.isdigit():
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(SUPPORTED_PLATFORMS):
                return SUPPORTED_PLATFORMS[selected_index]

        if choice.title() in SUPPORTED_PLATFORMS:
            return choice.title()

        print("Invalid choice. Please enter a valid platform number or name.")


def main() -> None:
    """Run the social media content generator."""
    print("Welcome to SocialGen: your social media post generator!")

    platform = get_platform()
    topic = input("What is the topic of your post? ").strip()
    tone = input("What tone should the post use? (e.g., professional, friendly, fun): ").strip()

    if not topic:
        print("Error: Topic cannot be empty.")
        raise SystemExit(1)

    if not tone:
        print("Error: Tone cannot be empty.")
        raise SystemExit(1)

    system_message = SystemMessage(
        content="You are a helpful assistant that writes social media content."
    )
    human_message = HumanMessage(
        content=(
            f"Create a social media post for {platform} about {topic} "
            f"in a {tone} tone."
        )
    )

    if API_PROVIDER == "openai":
        try:
            llm = init_chat_model(
                model=MODEL_NAME,
                openai_api_key=API_KEY,
                temperature=0.7,
            )
        except Exception as exc:
            print("Error: failed to initialize the OpenAI model.")
            print("Make sure you installed dependencies with: pip install -r requirements.txt")
            print(f"Details: {exc}")
            raise SystemExit(1)

        try:
            response = llm.generate(messages=[[system_message, human_message]])
            result = response.generations[0][0].text
        except RateLimitError as exc:
            print("Error: OpenAI quota or rate limit exceeded. Check your OpenAI billing, usage, or API key.")
            print(f"Details: {exc}")
            raise SystemExit(1)
        except OpenAIError as exc:
            print("Error: OpenAI API returned an error. Verify your API key and account status.")
            print(f"Details: {exc}")
            raise SystemExit(1)
        except Exception as exc:
            print("Unexpected error while generating the post.")
            print(f"Details: {exc}")
            raise SystemExit(1)
    elif API_PROVIDER == "ollama":
        try:
            from langchain_ollama import OllamaLLM
            llm = OllamaLLM(
                model=MODEL_NAME,
                base_url=OLLAMA_BASE_URL,
                temperature=0.7,
            )
        except Exception as exc:
            print("Error: failed to initialize the Ollama model.")
            print("Make sure Ollama is running with: ollama serve")
            print(f"Make sure the model is available: ollama pull {MODEL_NAME}")
            print(f"Details: {exc}")
            raise SystemExit(1)

        try:
            prompt_text = f"{system_message.content}\n\n{human_message.content}"
            result = llm.invoke(prompt_text)
        except Exception as exc:
            print("Unexpected error while generating the post with Ollama.")
            print(f"Details: {exc}")
            raise SystemExit(1)
    else:
        if not NVIDIA_API_URL:
            print("Error: NVIDIA_API_URL is required when API_PROVIDER=nvidia.")
            raise SystemExit(1)

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_message.content},
                {"role": "user", "content": human_message.content},
            ],
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(NVIDIA_API_URL, json=payload, headers=headers, timeout=30)
        except requests.RequestException as exc:
            print("Error: failed to call the NVIDIA API.")
            print(f"Details: {exc}")
            raise SystemExit(1)

        if response.status_code != 200:
            print(f"Error: NVIDIA API returned {response.status_code}.")
            try:
                print(response.json())
            except ValueError:
                print(response.text)
            raise SystemExit(1)

        data = response.json()
        if isinstance(data, dict) and "choices" in data:
            try:
                result = data["choices"][0]["message"]["content"]
            except Exception:
                result = str(data)
        else:
            result = str(data)

    print("\n--- Generated Social Media Post ---")
    print(result)


if __name__ == "__main__":
    main()
