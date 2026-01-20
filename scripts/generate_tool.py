import os
from software_whitelisting_assistant.scripts.classes import Tool
import openai
from software_whitelisting_assistant.scripts.llm_client import call_llm, load_prompt
from software_whitelisting_assistant.scripts.artifacts_store import save_tool


def generate_tool(model, temperature, max_tokens, prompt_name) -> Tool:

    prompt = load_prompt(prompt_name)

    tool = call_llm(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        text_format=Tool
    )

    # do once
    # save_tool(Tool.model_validate(tool), tool.name)

    return Tool.model_validate(tool)

    