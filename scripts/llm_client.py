import os
from pathlib import Path
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create OpenAI chat client for interaction with models
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("BASE_URL")
)

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"

def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def call_llm(
    prompt_name: str,
    model: str,
    temperature: float,
    max_tokens: int,
) -> str:
    prompt = load_prompt(prompt_name)
    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    return response.output_text

