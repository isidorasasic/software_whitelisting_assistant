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
- The section must contain from 1 to at most 5 paragraphs
- Paragraph length should reflect real-world legal and policy documents:
  - Short sections: 1–2 concise paragraphs
  - Medium sections: 2–4 paragraphs
  - Longer sections: up to 5 paragraphs only if the topic naturally requires it

After writing the section content:
- If you injected any issue (ambiguity, contradiction, typo, unclear reference, etc.),
  list them in JSON under "issues".
- If no issue was injected, return an empty list.

Return the response as JSON with:
{{
  "content": "<HTML>",
  "issues": [
    {{
      "description": "...",
      "severity": "low | medium | high"
    }}
  ]
}}