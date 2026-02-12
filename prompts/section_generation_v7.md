<!--
Prompt name: section_generation
Version: 7.0
Purpose: Generate a section based on the generated TOC for software legal and compliance documents
What's added: Additional issue instructions
-->

You are generating a section of a legal document.

Context:
- Tool name: {tool_name}
- Tool purpose: {purpose}
- Document type: {document_type}
- Section title: {section_title}
- Parent section: {parent_title}
- Previous sections: {previous_sections}
- Issue instruction: {issue_instruction}

Section Instructions:
- Write realistic legal prose.
- Write only section content; do not write the title.
- Keep the tone and content consistent with prior sections.
- Avoid repeating the wording from the previous sections.
- Avoid starting sentences with phrases such as "This section".
- Output ONLY valid HTML.
- Ensure all HTML tags are properly opened and closed.
- Avoid placing block-level tags (like <section> or <div>) inside <p>.
- The section must contain 1 to 5 paragraphs, with length appropriate for the topic:
  - Short sections: 1–2 concise paragraphs
  - Medium sections: 2–4 paragraphs
  - Long sections: up to 5 paragraphs only if the topic naturally requires it

Return the JSON object with exactly these keys:
- "content": string, HTML of the section.
- "issue": either:
    - null if no issue was injected, OR
    - an object with:
        - "description": string
        - "severity": one of "low", "medium", "high"

Issue handling rules:
- When the issue instruction says NO issue:
  - Do NOT mention issues, errors, problems, ambiguities, inconsistencies, or typos.
  - Do NOT state or imply that the section has no issues.
  - Do NOT describe hypothetical or potential issues.
  - Write the section as a fully correct, clean legal text.
- If the issue instruction explicitly says to inject exactly one issue, you MUST:
  - Inject exactly one issue
  - Describe only that issue
- Never infer or invent an issue.
