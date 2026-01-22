<!--
Prompt name: section_generation
Version: 3.0
Purpose: Generate a section based on the generated TOC for software legal and compliance documents
What's added: Closing of HTML tags
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
- Write realistic legal prose.
- Keep tone consistent with prior sections.
- Do NOT repeat headings.
- Output ONLY valid HTML.
- The section must contain 1 to 5 paragraphs, with length appropriate for the topic:
  - Short sections: 1–2 concise paragraphs
  - Medium sections: 2–4 paragraphs
  - Long sections: up to 5 paragraphs only if the topic naturally requires it
- Apply the instruction ONLY to this section; do not introduce any other issues.
- Ensure all HTML tags are properly opened and closed.
- Avoid placing block-level tags (like <section> or <div>) inside <p>.

After writing the section content:
- If any issue (ambiguity, contradiction, typo, unclear reference, etc.) was injected,
  list them in JSON under "issues".
- If no issue was injected, return an empty list.

Return the response as JSON with:
{{
  "content": "<HTML of this section>",
  "issues": [
    {{
      "description": "...",
      "severity": "low | medium | high"
    }}
  ]
}}