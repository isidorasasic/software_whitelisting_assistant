import os
from classes import Tool
import openai
from llm_client import call_llm


def main():

    def generate_tool(model, temperature, prompt_name) -> Tool:
        response = call_llm(
            prompt_name=prompt_name,
            model=model,
            temperature=temperature,
            max_tokens=200
        )

        return Tool.model_validate_json(response)


    tool = generate_tool(model="l2-gpt-4o-mini", temperature=0.7, prompt_name="tool_ideation.md")

    print(tool)
    
if __name__ == "__main__":
    main()