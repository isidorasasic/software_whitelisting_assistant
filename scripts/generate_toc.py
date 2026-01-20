from software_whitelisting_assistant.scripts.classes import TOC
from software_whitelisting_assistant.scripts.llm_client import call_llm, load_prompt
from software_whitelisting_assistant.scripts.artifacts_store import save_toc


def generate_TOC(tool, document_type, prompt_name, model, temperature, toolname) -> TOC:

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
        max_tokens=1200,
        text_format=TOC
    )

    # print(type(response_text))
    save_toc(TOC.model_validate(response_text), toolname)

    return TOC.model_validate(response_text)


