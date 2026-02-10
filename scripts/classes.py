from pydantic import BaseModel, Field
from typing import List, Optional


class TOCSection(BaseModel):
    """
    Represents a single section in a table of contents.

    Sections may contain nested subsections, forming a hierarchical structure
    used to drive recursive document generation.
    """
    id: str
    title: str
    subsections: list[TOCSection] = Field(default_factory=list)


class TOC(BaseModel):
    """
    Represents a table of contents for a document.

    Contains top-level sections that define the structure and ordering
    of generated document content.
    """
    id: str
    title: str
    sections: List[TOCSection]


class Section(BaseModel):
    """
    Represents a generated document section.

    Stores cleaned HTML content along with hierarchical metadata
    used for rendering and issue tracking.
    """
    id: str
    title: str
    level: int
    parent_id: str | None
    content_html: str


class Tool(BaseModel):
    """
    Describes a software tool for which documentation is generated.
    """
    name: str
    purpose: str
    category: str
    user_base: str


class SectionLLMOutput(BaseModel):
    """
    Structured output returned by the LLM for a single section.

    Includes generated content and any injected quality issues.
    """
    content: str
    issue: InjectedIssue = None


class InjectedIssue(BaseModel):
    """
    Represents a deliberately injected quality issue in a generated section.
    """
    section_id: str
    section_title: str
    description: str
    severity: Optional[str] = None


TOCSection.model_rebuild()