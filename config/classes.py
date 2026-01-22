from pydantic import BaseModel, Field
from typing import List


class ToolConfig(BaseModel):
    count: int = Field(gt=0)


class DocumentsConfig(BaseModel):
    types: List[str]
    per_tool: int


class ModelConfig(BaseModel):
    tool: str
    toc: str
    section: str


class TemperatureConfig(BaseModel):
    tool: float
    toc: float
    section: float


class PromptConfig(BaseModel):
    tool: str
    toc: str
    section: str


class MaxTokensConfig(BaseModel):
    tool: int
    toc: int
    section: int


class GenerationConfig(BaseModel):
    temperature: TemperatureConfig
    max_tokens: MaxTokensConfig


class IssueConfig(BaseModel):
    min_per_document: int = Field(ge=0)
    max_per_document: int = Field(ge=0)


class OutputConfig(BaseModel):
    data_dir: str = "data"


class AppConfig(BaseModel):
    seed: int
    tools: ToolConfig
    documents: DocumentsConfig
    models: ModelConfig
    prompts: PromptConfig
    generation: GenerationConfig
    issues: IssueConfig
    output: OutputConfig
