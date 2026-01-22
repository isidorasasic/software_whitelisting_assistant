from software_whitelisting_assistant.scripts.classes import Tool, TOC
from software_whitelisting_assistant.scripts.llm_client import call_llm, load_prompt
from pydantic import ValidationError


def generate_TOC(
    tool: Tool, 
    document_type: str, 
    prompt_name: str, 
    model: str, 
    temperature: float, 
    max_tokens: int
) -> TOC:

    prompt = load_prompt(prompt_name).format(
        document_type=document_type,
        tool_name=tool.name,
        purpose=tool.purpose,
        category=tool.category,
        user_base=tool.user_base
    )

    response_text = call_llm(
        prompt=prompt, 
        model=model, 
        temperature=temperature, 
        max_tokens=max_tokens,
        text_format=TOC
    )

    try:
        toc = TOC.model_validate(response_text)
        return toc
    except ValidationError as e:
        print("TOC validation failed:", e)
        return response_text

