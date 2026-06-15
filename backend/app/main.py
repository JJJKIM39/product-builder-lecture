"""
PromptForge Global — 백엔드 API (데이터 layer 1단계)

지금 단계 범위: prompt_templates 조회 + user_inputs/saved_prompts 저장
아직 없음: 인증, 결제(Stripe), 멀티에이전트 — 다음 단계
"""
from __future__ import annotations
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PromptForge Global API", version="0.1.0")

# 프론트(index.html)에서 호출할 수 있게 CORS 허용 (개발용 전체 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


@app.get("/")
def root():
    return {"service": "PromptForge Global API", "status": "ok"}


# ── 템플릿 조회 ──────────────────────────────────────────
@app.get("/templates", response_model=list[schemas.TemplateOut])
def list_templates(category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(models.PromptTemplate)
    if category:
        q = q.filter_by(category=category)
    return q.all()


@app.get("/templates/{slug}", response_model=schemas.TemplateOut)
def get_template(slug: str, db: Session = Depends(get_db)):
    t = db.query(models.PromptTemplate).filter_by(slug=slug).first()
    if not t:
        raise HTTPException(404, "템플릿을 찾을 수 없습니다")
    return t


# ── 유저 입력값 저장 ─────────────────────────────────────
@app.post("/inputs", response_model=schemas.InputOut)
def save_input(payload: schemas.InputCreate, db: Session = Depends(get_db)):
    if not db.get(models.PromptTemplate, payload.template_id):
        raise HTTPException(404, "template_id가 유효하지 않습니다")
    row = models.UserInput(**payload.model_dump())
    db.add(row); db.commit(); db.refresh(row)
    return row


# ── 완성 프롬프트 저장 / 목록 ────────────────────────────
@app.post("/saved", response_model=schemas.SavedOut)
def save_prompt(payload: schemas.SavedCreate, db: Session = Depends(get_db)):
    if not db.get(models.PromptTemplate, payload.template_id):
        raise HTTPException(404, "template_id가 유효하지 않습니다")
    row = models.SavedPrompt(**payload.model_dump())
    db.add(row); db.commit(); db.refresh(row)
    return row


@app.get("/saved", response_model=list[schemas.SavedOut])
def list_saved(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(models.SavedPrompt)
    if user_id:
        q = q.filter_by(user_id=user_id)
    return q.order_by(models.SavedPrompt.updated_at.desc()).all()
