from pathlib import Path
import random
from software_whitelisting_assistant.scripts.generate_tool import generate_tool
from software_whitelisting_assistant.scripts.generate_toc import generate_TOC
from software_whitelisting_assistant.scripts.generate_sections import generate_sections_from_toc, assemble_sections_to_html, summarize_previous_sections, save_issue_metadata
from software_whitelisting_assistant.scripts.artifacts_store import save_toc, save_tool, save_html, save_metadata
from software_whitelisting_assistant.scripts.load_config import load_config
from software_whitelisting_assistant.scripts.utils import normalize_name, build_full_html
from software_whitelisting_assistant.scripts.validate import validate_toc, validate_html
from pydantic import ValidationError

def main():

    # Load configuration
    config = load_config("config.yaml")
    print("Loaded configuration:")
    print(config.model_dump_json(indent=2))

    # Set seed (for testing)
    # random.seed(config.seed)
    # print(f"Seed set to {config.seed}")

    # Generate tools
    output_folder = Path(__file__).parent.parent / "data"
    output_folder.mkdir(parents=True, exist_ok=True)

    tools = []
    for i in range(config.tools.count): 
    # for i in range(1):
        print(f"[Tool] Generating Tool {i+1}...")
        tool = generate_tool(
            model=config.models.tool,         
            temperature=config.generation.temperature.tool,
            max_tokens=config.generation.max_tokens.tool,
            prompt_name=config.prompts.tool
        )
        tools.append(tool)

        tool_name = normalize_name(tool.name)

        # Save tools to output folder
        save_tool(tool, tool_name, output_folder)      

    print(f"[Info] Total tools generated: {len(tools)}")

    for tool in tools:
        print(tool.model_dump_json(indent=2))

    # --------------------------------------------------
    # 3. Generate documents per tool
    # --------------------------------------------------
    for tool in tools:

        tool_name = normalize_name(tool.name)
        tool_dir = output_folder / tool_name
        tool_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nGenerating documents for tool: {tool.name}")

        # Pick 4 distinct document types
        doc_types = random.sample(config.documents.types, k=config.documents.per_tool)

        for document_type in doc_types:
            print(f"  → {document_type}")

            doc_name = normalize_name(document_type)

            # -----------------------------
            # TOC
            # -----------------------------
            toc = generate_TOC(
                tool=tool,
                document_type=document_type,
                prompt_name=config.prompts.toc,
                model=config.models.toc,
                temperature=config.generation.temperature.toc,
                max_tokens=config.generation.max_tokens.toc
            )

            if isinstance(toc, str):
                print("Raw LLM output:\n", toc)

            # ---- Validate & save ----
            validate_toc(toc)
            save_toc(toc, tool_dir, f"toc_{doc_name}")

            # -----------------------------
            # Sections / HTML
            # -----------------------------
            sections, collected_issues = generate_sections_from_toc(
                tool=tool,
                toc=toc,
                document_type=document_type,
                model=config.models.section,
                temperature=config.generation.temperature.section,
                max_tokens=config.generation.max_tokens.section,
                prompt_name=config.prompts.section
            )

            # ---- Assemble full HTML document ----
            full_html = build_full_html(toc, sections)

            # ---- Validate & save ----
            validate_html(full_html)
            save_html(
                html=full_html,
                tool_dir=tool_dir,
                document_name=toc.id,
            )

            # -----------------------------
            # Metadata
            # -----------------------------
            save_metadata(
                tool=tool,
                toc=toc,
                document_type=document_type,
                tool_dir=tool_dir,
                model_tool=config.models.tool,
                model_toc=config.models.toc,
                model_section=config.models.section,
                temperature_tool=config.generation.temperature.tool,
                temperature_toc=config.generation.temperature.toc,
                temperature_section=config.generation.temperature.section,
                max_tokens_tool=config.generation.max_tokens.tool,
                max_tokens_toc=config.generation.max_tokens.toc,
                max_tokens_section=config.generation.max_tokens.section,
                issue_sections=collected_issues
            )

    print("\nDataset generation complete ✔")


if __name__ == "__main__":
    main()