from software_whitelisting_assistant.scripts.classes import Tool
from software_whitelisting_assistant.scripts.llm_client import call_llm, load_prompt


def generate_tool(
    model: str, 
    temperature: float, 
    max_tokens: int, 
    prompt_name: str
) -> Tool:

    prompt = load_prompt(prompt_name)

    tool = call_llm(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        text_format=Tool
    )

    return Tool.model_validate(tool)

    