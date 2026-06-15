"""
DB 연결 설정 (SQLite)
- 초기 개발용: 파일 하나(promptforge.db)가 곧 데이터베이스
- 나중에 PostgreSQL로 옮길 때는 DATABASE_URL만 바꾸면 됨
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 환경변수로 덮어쓸 수 있게 (나중에 postgresql://... 로 교체 가능)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "promptforge.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.abspath(DB_PATH)}")

# SQLite는 멀티스레드 접근 시 check_same_thread=False 필요
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI 의존성 주입용 — 요청마다 세션 열고 닫음"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
