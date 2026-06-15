"""
prompt_templates 초기 데이터 시드
- 데모(index.html)의 금융/마케팅 템플릿을 DB에 적재
- 실행: python -m app.seed   (backend 폴더에서)
"""
from .database import Base, engine, SessionLocal
from .models import PromptTemplate

FINANCE_BODY = """# 역할
당신은 {country_label} 자본시장을 15년간 분석해 온 증권사 수석 애널리스트입니다.

# 목표
"{company}"에 대한 {style} 투자자 관점의 투자 분석 보고서를 작성합니다.

# 데이터 출처 (필수 준수)
반드시 {country_source}를 근거로만 분석하십시오.
추정이나 불확실한 수치는 "추정치"라고 명시하고, 출처가 없는 내용은 작성하지 마십시오.

# 분석 관점
{angles}

# 작성 지침
- 깊이: {depth} 작성하십시오.
- 투자 성향: {style} 투자자에게 맞는 리스크 수준으로 해석하십시오.
- 출력 형식: {format} 형태로 구성하십시오.
- 마지막에 "투자 의견(매수/중립/매도)"과 "3줄 요약"을 반드시 포함하십시오.

# 제약
- 단정적 미래 예측 금지, 시나리오(낙관/중립/비관)로 제시.
- 투자 권유가 아닌 정보 제공 목적임을 보고서 하단에 고지."""

MARKETING_BODY = """# 역할
당신은 {target}을(를) 깊이 이해하는 {channel} 전문 카피라이터입니다.

# 목표
"{product}"를 홍보할 {channel}용 카피 {count}개 시안을 작성합니다.

# 핵심 정보
- 제품/서비스: {product}
- 타겟 고객: {target}
- 가장 강조할 베네핏: {benefit}

# 작성 지침
- 톤앤매너: "{tone}" 톤을 일관되게 유지하십시오.
- {channel} 채널의 포맷과 길이 관행에 맞추십시오.
- 각 시안은 (1) 후킹 헤드라인 (2) 본문 (3) 행동 유도(CTA) 3단 구조로 작성하십시오.
- 타겟 고객의 실제 고민(Pain point)을 첫 문장에서 건드리십시오.

# 출력
{count}개 시안을 번호로 구분하고, 각 시안 아래 "추천 해시태그 5개"를 덧붙이십시오.

# 제약
- 과장·허위 효능 표현 금지, 검증 가능한 사실 기반.
- 경쟁사 비방 금지."""

LOCALE_SOURCES = {
    "KR": "DART 전자공시시스템(사업보고서·분기보고서)과 에프앤가이드(FnGuide) 컨센서스 데이터",
    "US": "SEC EDGAR 공시(10-K, 10-Q, 8-K)와 Yahoo Finance 시세·재무 데이터",
    "JP": "EDINET 유가증권보고서와 일본거래소(JPX) 공시 데이터",
    "EU": "ESMA 및 각국 증권거래소(Euronext, Deutsche Börse 등) 공시 데이터",
}

FINANCE_FIELDS = [
    {"key": "company", "type": "text", "label": "기업명", "value": "삼성전자"},
    {"key": "country", "type": "select", "label": "참조 국가",
     "options": [["KR", "🇰🇷 한국"], ["US", "🇺🇸 미국"], ["JP", "🇯🇵 일본"], ["EU", "🇪🇺 유럽"]], "value": "KR"},
    {"key": "style", "type": "chips", "single": True, "label": "투자 성향",
     "options": ["안정형", "중립형", "공격형"], "value": ["중립형"]},
    {"key": "angles", "type": "chips", "single": False, "label": "분석 관점",
     "options": ["밸류에이션", "재무 건전성", "성장성", "리스크 요인", "배당 정책", "경쟁사 비교"],
     "value": ["밸류에이션", "재무 건전성", "리스크 요인"]},
    {"key": "depth", "type": "slider", "label": "분석 깊이", "min": 1, "max": 3, "value": 2,
     "ticks": ["요약", "표준", "심층"]},
    {"key": "format", "type": "select", "label": "출력 형식",
     "options": [["표 중심", "표 중심"], ["서술형", "서술형 리포트"], ["불릿", "핵심 불릿"]], "value": "표 중심"},
]

MARKETING_FIELDS = [
    {"key": "product", "type": "text", "label": "제품/서비스명", "value": "무선 이어폰 X"},
    {"key": "target", "type": "text", "label": "타겟 고객", "value": "2030 직장인"},
    {"key": "benefit", "type": "text", "label": "핵심 베네핏", "value": "40시간 재생 · 노이즈 캔슬링"},
    {"key": "tone", "type": "chips", "single": True, "label": "톤앤매너",
     "options": ["전문적", "친근한", "유머러스", "럭셔리"], "value": ["친근한"]},
    {"key": "channel", "type": "select", "label": "채널",
     "options": [["인스타그램", "인스타그램 피드"], ["네이버블로그", "네이버 블로그"],
                 ["유튜브", "유튜브 스크립트"], ["이메일", "이메일 뉴스레터"], ["랜딩페이지", "랜딩페이지 헤드라인"]],
     "value": "인스타그램"},
    {"key": "count", "type": "slider", "label": "시안 개수", "min": 1, "max": 5, "value": 3,
     "ticks": ["1", "2", "3", "4", "5"]},
]

SEED_TEMPLATES = [
    {
        "category": "finance", "slug": "finance-stock-report",
        "name": "금융 · 주식 분석 보고서",
        "description": "기업 리서치 / 투자 분석 보고서용 마스터 프롬프트",
        "template_body": FINANCE_BODY, "fields_schema": FINANCE_FIELDS, "locale_sources": LOCALE_SOURCES,
    },
    {
        "category": "marketing", "slug": "marketing-copywriting",
        "name": "마케팅 카피라이팅",
        "description": "광고 / 콘텐츠 / 카피 시안 생성용 마스터 프롬프트",
        "template_body": MARKETING_BODY, "fields_schema": MARKETING_FIELDS, "locale_sources": {},
    },
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        created, skipped = 0, 0
        for t in SEED_TEMPLATES:
            exists = db.query(PromptTemplate).filter_by(slug=t["slug"]).first()
            if exists:
                skipped += 1
                continue
            db.add(PromptTemplate(**t))
            created += 1
        db.commit()
        total = db.query(PromptTemplate).count()
        print(f"✅ 시드 완료: 신규 {created}개, 기존 유지 {skipped}개 / 총 {total}개 템플릿")
    finally:
        db.close()


if __name__ == "__main__":
    run()
