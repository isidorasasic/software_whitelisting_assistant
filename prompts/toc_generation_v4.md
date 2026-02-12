<!--
Prompt name: toc_generation
Version: 4.0
Purpose: Generate a structured table of contents (TOC) for software legal and compliance documents
-->

You are an expert legal and technical documentation architect for software products.

Your task is to generate a clear, realistic, and well-structured table of contents
for a software document.

Document type: {document_type}

Tool context:
- Name: {tool_name}
- Purpose: {purpose}
- Category: {category}
- Typical users: {user_base}

Requirements:
- The TOC must be realistic for the given document type and structure
- Section ordering must be logical and industry-appropriate
- Section titles must be concise and professional
- Avoid overly generic or vague section names
- Do NOT include any section content, only section titles
- Do NOT mention that this is fictional or synthetic
- Do NOT truncate strings
- Ensure all quotes are closed
- Do not restrict the TOC for 2 levels, it should represent realistic document structure
- In case subsection is empty, do not rassign NULL, but an empty list instead

Output format:
You must return ONLY valid JSON object that matches the following structure:

- id: string
- title: string
- sections: array of section objects

Each section object:
- id: string
- title: string
- anchor: string
- subsections: optional array of section objects

Rules:
- Use kebab-case for all section IDs (e.g., "data-retention-policy")
- IDs must be unique within the document
- The title field should be a human-readable section heading
- Generate number of sections that is appropriate for the document type but no more than 20
- Do NOT include numbering in section titles
- Do NOT include markdown, comments, or explanatory text




