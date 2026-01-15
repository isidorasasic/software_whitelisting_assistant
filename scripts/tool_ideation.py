import os
from classes import Tool
import openai
from llm_client import call_llm, load_prompt
from tool_store import save_tool


def generate_tool(model, temperature, prompt_name, filename) -> Tool:

    prompt = load_prompt(prompt_name)

    tool = call_llm(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=200,
        # text_format=Tool
    )

    # do once
    save_tool(Tool.model_validate_json(tool), filename)

    return Tool.model_validate_json(tool)

    