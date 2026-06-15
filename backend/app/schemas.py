"""
Pydantic 스키마 — API 요청/응답 형태 정의
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemplateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category: str
    slug: str
    name: str
    description: str
    template_body: str
    fields_schema: list
    locale_sources: dict


class InputCreate(BaseModel):
    template_id: int
    user_id: Optional[str] = None
    input_values: dict


class InputOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    template_id: int
    user_id: Optional[str]
    input_values: dict
    created_at: datetime


class SavedCreate(BaseModel):
    template_id: int
    user_id: Optional[str] = None
    title: str = "제목 없음"
    final_prompt: str
    input_values: dict = {}


class SavedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    template_id: int
    user_id: Optional[str]
    title: str
    final_prompt: str
    input_values: dict
    created_at: datetime
    updated_at: datetime
