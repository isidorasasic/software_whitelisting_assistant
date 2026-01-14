from pydantic import BaseModel
from typing import List

class TOC(BaseModel):
    id: str
    title: str
    content: str

class Section(BaseModel):
    id: str
    title: str
    content: str

class Document(BaseModel):
    title: str
    sections: List[Section]

class Tool(BaseModel):
    name: str
    purpose: str
    category: str
    user_base: str
