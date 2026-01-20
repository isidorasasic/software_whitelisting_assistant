from pathlib import Path
import random
from software_whitelisting_assistant.scripts.generate_tool import generate_tool
from software_whitelisting_assistant.scripts.generate_toc import generate_TOC
from software_whitelisting_assistant.scripts.generate_sections import generate_sections_from_toc, summarize_previous_sections, save_issue_metadata
from software_whitelisting_assistant.scripts.artifacts_store import load_tool, load_toc, save_tool
from software_whitelisting_assistant.scripts.load_config import load_config
from software_whitelisting_assistant.scripts.utils import normalize_tool_name
# from software_whitelisting_assistant.scripts.set_seed import set_seed


DOCUMENT_POOL = [
    "Privacy Policy",
    "Terms of Service",
    "Data Processing Agreement",
    "Service Level Agreement",
    "Security Whitepaper",
    "Compliance & Certifications",
]

# ----------------------------
# CONFIG
# ----------------------------
DATA_DIR = Path("data")
NUM_TOOLS = 5
DOCUMENTS_PER_TOOL = 4

# Models
TOC_MODEL = "l2-gpt-4.1-nano"
SECTION_MODEL = "l2-gpt-4.1-nano"
TOC_TEMPERATURE = 0.2
SECTION_TEMPERATURE = 0.7

# Prompts
TOC_PROMPT = "prompts/toc_generation_v3.txt"
SECTION_PROMPT = "prompts/section_generation.txt"
TOOL_PROMPT = "prompts/tool_ideation.txt"

MIN_ISSUES = 2
MAX_ISSUES = 3


def main():

    document_type=DOCUMENT_POOL[0]

    # tool = generate_tool(
    #         model="l2-gpt-4.1-mini", 
    #         temperature=0.7, 
    #         prompt_name="tool_ideation.md",
    #         toolname="software_tool_1"
    #         )

    # print(tool)

    tool = load_tool("software_tool_1")

    # folder = make_tool_folder(tool.name)

    # toc = generate_TOC(
    #         tool=tool, 
    #         document_type=DOCUMENT_POOL[0], 
    #         prompt_name="toc_generation_v4.md", 
    #         model=TOC_MODEL, 
    #         temperature=0.2,
    #         toolname="software_tool_1"
    #         )
    
    toc = load_toc("software_tool_1")

    # ---- SECTION GENERATION ----
    # generated_sections = generate_sections_from_toc(
    #     toc=toc,
    #     tool=tool,
    #     document_type=document_type,
    #     model=SECTION_MODEL,
    #     temperature=SECTION_TEMPERATURE,
    #     prompt_name="section_generation_v2.md"
    # )

    # ---- SUMMARIZE PREVIOUS (optional for long documents) ----
    # memory = summarize_previous_sections(
    #     previous_sections=[s.content_html for s in generated_sections],
    #     model=SECTION_MODEL
    # )

    # ---- SAVE SECTIONS ----
    # for section in generated_sections:
    #     html_path = folder / f"{section.id}.html"
    #     html_path.write_text(section.content_html, encoding="utf-8")

    # ---- SAVE METADATA ----
    # save_metadata(
    #     folder=folder,
    #     toc=toc,
    #     sections=generated_sections,
    #     issue_sections=issue_sections
    # )


    # Load configuration
    config = load_config("config.yaml")
    print("Loaded configuration:")
    print(config.model_dump_json(indent=2))

    # Set seed
    random.seed(config.seed)
    print(f"Seed set to {config.seed}")

    # Generate tools
    output_folder = Path(__file__).parent.parent / "data"
    output_folder.mkdir(parents=True, exist_ok=True)

    tools = []
    # for i in range(config.tools_count):
    for i in range(1):  
        print(f"[Tool] Generating Tool {i+1}...")
        tool = generate_tool(
            model=config.models.tool,         
            temperature=config.generation.temperature.tool,
            max_tokens=config.generation.max_tokens.tool,
            prompt_name=config.prompts.tool
        )
        tools.append(tool)

        tool_name = normalize_tool_name(tool.name)

        # Save tools to output folder
        save_tool(tool, tool_name, output_folder)

    print(f"[Info] Total tools generated: {len(tools)}")

    for tool in tools:
        print(tool.model_dump_json(indent=2))

    # for tool in generate_tool(config):
    #     save_tool_metadata(tool)

    #     for doc_type in select_document_types(tool, config):
    #         toc = generate_TOC(...)
    #         validate_toc(toc)
    #         save_toc(tool, doc_type, toc)

    #         sections = generate_sections_from_toc(...)
    #         validate_section_coverage(toc, sections)
    #         validate_html_sections(sections)

            # html = render_document(toc, sections)
            # save_html(tool, doc_type, html)


if __name__ == "__main__":
    main()