import os
from pathlib import Path
from typing import TypeVar, Type, Optional, Dict, Any
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
from software_whitelisting_assistant.scripts.classes import TOC
import inspect

# Load environment variables from .env file
load_dotenv()

# create generic object to be used as a type parameter in structured outputs
T = TypeVar("T", bound=BaseModel)

# Create OpenAI chat client for interaction with models
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("BASE_URL")
)

# prompt path
PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"

def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def call_llm(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    text_format: Optional[Type[T]] = None
):
    # DEBUG
    # print(inspect.signature(client.responses.create))

    if text_format is None:
        # Plain text generation
        response = client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        return response.output_text

    response = client.responses.parse(
        model=model,
        input=prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
        text_format=text_format
    )

    usage = response.usage

    print("/nInput tokens:", usage.input_tokens)
    print("Output tokens:", usage.output_tokens)
    print("Total tokens:", usage.total_tokens)
    print("/n")

    if text_format is not None:
        if response.output_parsed is None:
            raise ValueError("Expected structured output but got none")
        return response.output_parsed

    return response.output_text

