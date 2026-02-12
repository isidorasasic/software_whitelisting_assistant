<!--
Prompt name: tool_ideation
Version: 2.0
Purpose: Generate fictional software tool name and description
-->

Your task is to invent a realistic fictional software tool.

Requirements:
- Do NOT use names of existing software tools.
- It should belong to a clear software category.
- Generate a new, creative, realistic tool name; avoid generic or vague phrasing.
- Do NOT start the tool name with "Data", "Code", "Cloud", or "Enterprise".
- Do NOT mention that the tool is fictional or synthetic.


Return only valid json in this format:
{
  "name": "...",
  "purpose": "...",
  "category": "...",
  "user_base": "..."
}

Field guidance:
- name: Examples:
  - MedTrack Suite
  - Task Master
  - Insight Hub
- purpose: 1–2 sentences describing what the software does
- category: High-level software category
- user_base: Typical users (e.g., SMBs, enterprises, healthcare providers, developers)