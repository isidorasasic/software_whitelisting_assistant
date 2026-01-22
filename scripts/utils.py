import re
import html
from typing import List
from typing import Iterable, Mapping
from software_whitelisting_assistant.scripts.classes import TOCSection, Section, TOC


def normalize_name(name: str) -> str:
    """
    Convert name into a filesystem-safe folder name.
    """
    name = name.lower().strip()
    name = name.replace("&", "and")
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_-]+", "_", name)

    return name


def build_section_index(sections: Iterable[Section]) -> dict[str, Section]:
    """Build a lookup dict of sections by id."""
    
    return {s.id: s for s in sections}


def assemble_sections_from_toc(
    toc_sections: list[TOCSection],
    section_by_id: Mapping[str, Section], *,
    strict: bool = False
) -> str:
    """
    Render nested HTML <section> elements based on the TOC tree.
    - toc_sections: top-level TOC nodes
    - section_by_id: mapping from section id -> Section
    - strict: if True, raise KeyError when a TOC node has no matching Section;
      if False, skip it.
    """
    
    parts: list[str] = []

    def render_node(node: TOCSection) -> str:
        sec = section_by_id.get(node.id)
        if sec is None:
            if strict:
                raise KeyError(f"No Section found for TOC id '{node.id}'")
            return ""  # skip this node (and its subtree)

        inner_parts = [sec.content_html]
        for child in node.subsections or []:
            child_html = render_node(child)
            if child_html:
                inner_parts.append(child_html)

        level_attr = f' data-level="{sec.level}"' if getattr(sec, "level", None) is not None else ""
        return (
            f'<section id="{html.escape(sec.id, quote=True)}"{level_attr}>'
            + "\n".join(inner_parts)
            + "</section>"
        )

    for node in toc_sections:
        rendered = render_node(node)
        if rendered:
            parts.append(rendered)

    return "\n\n".join(parts)


# def render_toc_nav(toc_sections: List["TOCSection"]) -> str:
#     def render_node(node: "TOCSection") -> str:
#         kids = node.subsections or [] 
#         children_html = "".join(render_node(c) for c in kids)
#         link = f'<a href="#{html.escape(node.id, quote=True)}">{html.escape(node.title)}</a>'

#         if children_html:
#             return f"<li>{link}<ul>{children_html}</ul></li>"
        
#         return f"<li>{link}</li>"

#     items = "".join(render_node(n) for n in toc_sections)
#     return f'<nav class="toc"><ul>{items}</ul></nav>'

def build_full_html(
    toc: TOC,
    sections: List[Section], *,
    strict: bool = False
) -> str: 
    section_by_id: Mapping[str, Section] = {s.id: s for s in sections}
    body_html = assemble_sections_from_toc(toc.sections, section_by_id, strict=strict)
    # toc_nav = render_toc_nav(toc.sections)

    return (
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8" />
        <title>{html.escape(toc.title)}</title>
        </head>
        <body>
        {body_html}
        </body>
        </html>
        """.strip()
    )

