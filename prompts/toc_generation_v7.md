<!--
Prompt name: toc_generation
Version: 7.0
Purpose: Generate a structured table of contents (TOC) for software legal and compliance documents
What's added: Lower the limit for number of sections
-->

You are an expert legal and technical documentation architect for software products.

Your task is to generate a clear, realistic, and well-structured table of contents (TOC)
for a software document.

Document type: {document_type}

Tool context:
- Name: {tool_name}
- Purpose: {purpose}
- Category: {category}
- Typical users: {user_base}

Requirements:
- The TOC must be realistic for the given document type and structure.
- Section ordering must be logical and industry-appropriate.
- Section titles must be concise and professional.
- Include all relevant subtopics for a realistic document structure.
- Nest sections naturally as they would appear in a real policy.
- Do not restrict TOC depth — use multiple levels if appropriate.
- If a section has no subsections, use an empty array [].
- Do not truncate strings or leave dangling quotes.
- Use kebab-case for all section IDs (e.g., "data-retention-policy").
- IDs must be unique within the document.
- Do NOT include numbering in section titles.
- Generate a realistic number of sections, but no more than 15.

Output format:
You must return ONLY valid JSON object that matches the following structure:

- Top-level object:

id: string
title: string
sections: array of section objects (≥ 1)

- Each section object:

id: string
title: string
subsections: optional array of section objects






