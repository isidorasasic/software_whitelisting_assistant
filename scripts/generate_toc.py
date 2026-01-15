from classes import TOC
from llm_client import call_llm, load_prompt


def generate_TOC(tool, document_type, prompt_name, model, temperature) -> TOC:

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
        max_tokens=200,
        # text={
        #     "format": {
        #         "type": "json_schema",
        #         "name": "toc",
        #         "schema": TOC.model_json_schema(),
        #         "description": "Table of contents for a legal document"
        #     }
        # }
        text_format=TOC
    )

    # print(type(response_text))

    return TOC.model_validate(response_text)


