from tool_ideation import generate_tool
from generate_toc import generate_TOC
from tool_store import load_tool


DOCUMENT_POOL = [
    "Privacy Policy",
    "Terms of Service",
    "Data Processing Agreement",
    "Service Level Agreement",
    "Security Whitepaper",
    "Compliance & Certifications",
]

def main():

    # tool = generate_tool(
    #         model="l2-gpt-4.1-mini", 
    #         temperature=0.7, 
    #         prompt_name="tool_ideation.md",
    #         filename="software_tool_1.json"
    #         )

    # print(tool)

    tool = load_tool("software_tool_1.json")

    toc = generate_TOC(
            tool=tool, 
            document_type=DOCUMENT_POOL[0], 
            prompt_name="toc_generation.md", 
            model="l2-gpt-4.1-nano", 
            temperature=0.2
            )

    print(toc)


if __name__ == "__main__":
    main()