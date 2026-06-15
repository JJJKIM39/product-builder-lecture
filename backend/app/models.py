"""
DB 테이블 정의 (지침서 4번 — 3종 테이블)

1) prompt_templates : 분야별(금융/마케팅/...) 전문가 프롬프트 기본 프레임워크
2) user_inputs      : 유저가 대시보드에서 선택한 변수 값
3) saved_prompts    : 유저가 저장한 커스텀 완성본 프롬프트
"""
from __future__ import annotations
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


def _now():
    return datetime.now(timezone.utc)


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id:            Mapped[int]  = mapped_column(primary_key=True)
    category:      Mapped[str]  = mapped_column(String(40), index=True)   # finance | marketing | ...
    slug:          Mapped[str]  = mapped_column(String(60), unique=True)  # finance-stock-report
    name:          Mapped[str]  = mapped_column(String(120))
    description:   Mapped[str]  = mapped_column(String(255), default="")
    # 마스터 프롬프트 본문 ({placeholder} 토큰 포함)
    template_body: Mapped[str]  = mapped_column(Text)
    # 대시보드에 렌더링할 입력 필드 스키마 (데모의 SCHEMAS와 동일 구조)
    fields_schema: Mapped[list] = mapped_column(JSON, default=list)
    # 국가별 공식 출처 치환 맵 {"KR": "...", "US": "..."} — 없으면 빈 dict
    locale_sources: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at:    Mapped[datetime] = mapped_column(DateTime, default=_now)

    inputs:        Mapped[List["UserInput"]]   = relationship(back_populates="template")
    saved:         Mapped[List["SavedPrompt"]] = relationship(back_populates="template")


class UserInput(Base):
    __tablename__ = "user_inputs"

    id:          Mapped[int] = mapped_column(primary_key=True)
    # 인증 붙이기 전까지 nullable (익명 세션 허용)
    user_id:     Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("prompt_templates.id"))
    # 유저가 고른 변수 값 {"company": "삼성전자", "country": "KR", ...}
    input_values: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at:  Mapped[datetime] = mapped_column(DateTime, default=_now)

    template:    Mapped["PromptTemplate"] = relationship(back_populates="inputs")


class SavedPrompt(Base):
    __tablename__ = "saved_prompts"

    id:          Mapped[int] = mapped_column(primary_key=True)
    user_id:     Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("prompt_templates.id"))
    title:       Mapped[str] = mapped_column(String(120), default="제목 없음")
    # 완성된 프롬프트 텍스트 전문
    final_prompt: Mapped[str] = mapped_column(Text)
    # 저장 시점의 변수 값 스냅샷
    input_values: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at:  Mapped[datetime] = mapped_column(DateTime, default=_now)
    updated_at:  Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)

    template:    Mapped["PromptTemplate"] = relationship(back_populates="saved")
