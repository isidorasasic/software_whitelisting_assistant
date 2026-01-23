# Software Whitelisting Assistant – Synthetic Document Generator

**Version: 1.0**
**Author: Isidora Sasic**

## Overview

The **Software Whitelisting Assistant** is a Python-based tool for generating realistic synthetic software documentation. It produces:

- Fictional software tools
- Multiple document types per tool (Privacy Policy, Terms of Service, SLA, etc.)
- Table of Contents (TOC) in JSON format
- Section-level HTML content
- Metadata and issue tracking for quality evaluation

The system is designed to simulate real-world documentation while allowing controlled injection of minor issues (typos, ambiguity, inconsistencies) for testing.

## Project Structure

software_whitelisting_assistant/
├── scripts/
│   ├── generate_tool.py         # Generates fictional software tools
│   ├── generate_toc.py          # Generates TOC JSON for documents
│   ├── generate_sections.py     # Generates HTML sections from TOC
│   ├── generate_dataset.py      # Orchestrates multi-tool, multi-document generation (main orchestrator script)
│   ├── llm_client.py            # LLM interaction wrapper
│   ├── validate.py              # Validators for TOC and HTML
│   ├── artifacts_store.py       # Saving/loading generated files
│   ├── load_config.py           # Loads YAML configuration
│   ├── utils.py                 # Helper functions
│   └── classes.py               # Pydantic data models
├── config/
│   ├── classes.py               # Configuration models
│   └── config.yaml              # Config file for models, temperature, document types, etc.
├── prompts/                     # Prompt templates for TOC, sections, tools
└── data/                        # Generated outputs

## Features

- **Tool Generation** – Generates fictional software tool names, categories, purposes, and typical user bases.
- **TOC Generation** – Produces realistic JSON Table of Contents, with nested sections and unique kebab-case IDs.
- **Section Generation** – LLM produces legal or technical document sections in **HTML**, with 1–5 realistic paragraphs per section.
- **Issue Injection** – Optionally injects a minor issue (typo, ambiguity, contradiction) for testing.
- **Validation** – TOC and HTML validators ensure structural integrity and prevent broken tags.
- **Persistence** – Saves generated documents and TOC JSON in tool-specific folders.
- **Configurable** – All parameters (model, temperature, number of tools, document types) are configurable via `config.yaml`.

## Requirements

See requirements.txt

Install dependencies:

pip install -r requirements.txt

## Usage

Generate documents for all tools

Run:
```bash
python -m software_whitelisting_assistant.scripts.generate_dataset
```

This will:

- Generate 5 fictional tools (configurable).
- For each tool, randomly select document types.
- Generate TOC JSON and HTML sections.
- Assemble sections into a single HTML file per document.
- Save outputs under data/tools/{tool_name}/.

## Config parameters

seed: 42                            # for testing

tools:
  count: 5

documents:
  types:
    - Privacy Policy
    - Terms of Service
    - Data Processing Agreement
    - Service Level Agreement
    - Security Whitepaper
    - Compliance & Certifications
  per_tool: 4

models:
  tool: l2-gpt-4.1-mini
  toc: l2-gpt-4.1
  section: l2-gpt-4.1-nano

prompts:
  tool: tool_ideation_v2.md
  toc: toc_generation_v7.md
  section: section_generation_v3.md

generation:
  temperature:
    tool: 0.9
    toc: 0.5
    section: 0.7
  max_tokens:
    tool: 200
    toc: 2000
    section: 1000

issues:
  min_per_document: 2
  max_per_document: 3

output:
  data_dir: data


## Debugging / Logging

- print_section_console(section) – prints section content and hierarchy.
- print_injected_issues(issues) – lists all injected issues in JSON format.

