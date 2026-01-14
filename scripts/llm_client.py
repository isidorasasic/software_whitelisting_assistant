import os

import openai

from dotenv import load_dotenv

def main():

    # Load environment variables from .env file
    load_dotenv()

    # Create OpenAI chat client for interaction with models
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("BASE_URL")
    )

    # Create AI agent
    response = client.responses.create(
        model="l2-gpt-4o-mini",
        instructions="You are a helpful assistant.",
        input="Write me a short poem.",
        max_output_tokens=5000
    )

    print(response.output_text)



if __name__ == "__main__":
    main()


# def call_llm(
#     prompt: str,
#     model: str,
#     temperature: float,
#     max_tokens: int,
# ) -> str:
#     response = client.responses.create(
#         model=model,
#         input=prompt,
#         temperature=temperature,
#         max_output_tokens=max_tokens,
#     )
#     return response.output_text
