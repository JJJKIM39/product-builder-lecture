# PromptForge Global — 백엔드 (데이터 layer)

FastAPI + SQLite 기반. 현재 단계는 **데이터 layer 1단계**입니다.

## 구현된 것
- DB 3종 테이블: `prompt_templates`, `user_inputs`, `saved_prompts`
- 금융 / 마케팅 마스터 프롬프트 템플릿 시드 데이터
- 조회·저장 API (인증 없음 — 익명 허용)

## 아직 없는 것 (다음 단계)
- 회원가입 / 로그인 (인증)
- 결제 (Stripe)
- 멀티 에이전트 (CrewAI / LangGraph)
- 프론트(index.html)와 API 연결

## 실행 방법

```bash
cd backend
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 1) DB 생성 + 템플릿 시드
./venv/bin/python -m app.seed

# 2) API 서버 실행
./venv/bin/uvicorn app.main:app --reload --port 8001
```

서버 실행 후 `http://127.0.0.1:8001/docs` 에서 API 문서를 확인할 수 있습니다.

## API 요약
| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/templates` | 전체 템플릿 목록 (`?category=finance` 필터) |
| GET | `/templates/{slug}` | 특정 템플릿 + 필드 스키마 |
| POST | `/inputs` | 유저가 고른 변수 값 저장 |
| POST | `/saved` | 완성된 프롬프트 저장 |
| GET | `/saved` | 저장된 프롬프트 목록 (`?user_id=` 필터) |

## 배포 메모
GitHub Pages는 정적 호스팅이라 이 백엔드를 못 올립니다.
실제 배포 시 Railway / Render / Fly.io 등 Python 호스팅이 필요하며,
그때 `DATABASE_URL` 환경변수를 PostgreSQL 주소로 바꾸면 SQLite → PostgreSQL 전환됩니다.
