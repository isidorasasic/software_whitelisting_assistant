from pydantic import BaseModel, Field
from typing import List, Optional


class TOCSection(BaseModel):
    id: str
    title: str
    subsections: list[TOCSection] = Field(default_factory=list)


class TOC(BaseModel):
    id: str
    title: str
    sections: List[TOCSection]


class Section(BaseModel):
    id: str
    title: str
    level: int
    parent_id: str | None
    content_html: str

class Document(BaseModel):
    title: str
    sections: List[Section]


class Tool(BaseModel):
    name: str
    purpose: str
    category: str
    user_base: str


class SectionLLMOutput(BaseModel):
    content: str
    issues: List[InjectedIssue] = []


class InjectedIssue(BaseModel):
    section_id: str
    section_title: str
    description: str
    severity: Optional[str] = None


TOCSection.model_rebuild()