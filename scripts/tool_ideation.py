import random
from pathlib import Path
import os
from classes import Tool
import openai
from dotenv import load_dotenv

# DOCUMENT_POOL = [
#     "Privacy Policy",
#     "Terms of Service",
#     "Data Processing Agreement",
#     "Service Level Agreement",
#     "Security Whitepaper",
#     "Compliance & Certifications",
# ]

def main():

    PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"

    def load_prompt(name: str) -> str:
        path = PROMPTS_DIR / name
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8")

    def generate_tool(model, temperature) -> Tool:

        prompt = load_prompt("tool_ideation.md")

        # Load environment variables from .env file
        load_dotenv()

        # Create OpenAI chat client for interaction with models
        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("BASE_URL")
        )

        # Create AI agent
        response = client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature,
            max_output_tokens=200
        )

        print(response.output_text)

    generate_tool(model="l2-gpt-4o-mini", temperature=0.7)

if __name__ == "__main__":
    main()