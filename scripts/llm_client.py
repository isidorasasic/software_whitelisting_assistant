import os
from typing import TypeVar, Type, Optional
from pydantic import BaseModel
import openai
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# create generic object to be used as a type parameter in structured outputs
T = TypeVar("T", bound=BaseModel)

# Create OpenAI chat client for interaction with models
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("BASE_URL")
)

def call_llm(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    text_format: Optional[Type[T]] = None,
):
    # DEBUG
    # print(inspect.signature(client.responses.create))

    if text_format is None:
        # Plain text generation (for sections)
        response = client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        return response.output_text

    # Structured output generation (for tools and toc)
    response = client.responses.parse(
        model=model,
        input=prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
        text_format=text_format
    )

    # usage = response.usage

    # Token usage testing
    # print("/nInput tokens:", usage.input_tokens)
    # print("Output tokens:", usage.output_tokens)
    # print("Total tokens:", usage.total_tokens)
    # print("/n")

    if text_format is not None:
        if response.output_parsed is None:
            raise ValueError("Expected structured output but got none")
        return response.output_parsed

    return response.output_text

