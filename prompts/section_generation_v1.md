<!--
Prompt name: section_generation
Version: 2.0
Purpose: Generate a section based on the generated TOC for software legal and compliance documents
-->

You are generating a section of a legal document.

Context:
- Tool name: {tool_name}
- Tool purpose: {purpose}
- Document type: {document_type}
- Section title: {section_title}
- Parent section: {parent_title}
- Previous sections summary:
{previous_summary}
- Issue instruction: {issue_instruction}

Instructions:
- Write realistic legal prose
- Keep tone consistent with prior sections
- Do NOT repeat headings
- Output ONLY valid HTML
- Apply the instruction ONLY to this section
- Do not introduce any other issues
- Length: maximum 5 paragraphs
