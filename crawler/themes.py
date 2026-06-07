#!/usr/bin/env python3
"""
xinvest.site — 당일 주도 테마 분석 (AI 기반)
GitHub Actions에서 매일 장 마감 후 실행됩니다. (평일 16:30 KST)

흐름:
  1. yfinance로 국내 주요 종목 + 코스피/코스닥 지수 수집
  2. Claude API에 데이터 주입 → 테마 분석 JSON 생성
  3. data/themes.json 으로 저장 → 홈 대시보드 themeRankList에 렌더링
"""

import os, json
from datetime import datetime
from anthropic import Anthropic

KST_OFFSET = 9  # UTC+9
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'themes.json')

# ── Claude 클라이언트 ────────────────────────────────────────────────
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── 분석 대상 종목 (실제 운영 시 상위 50개 크롤링 데이터로 대체) ──────
TARGET_STOCKS = {
    "005930.KS": "삼성전자",
    "000660.KS": "SK하이닉스",
    "009150.KS": "삼성전기",
    "035420.KS": "NAVER",
    "005380.KS": "현대차",
    "051910.KS": "LG화학",
    "068270.KS": "셀트리온",
    "214320.KQ": "실리콘투",
    "035720.KS": "카카오",
    "207940.KS": "삼성바이오로직스",
}

INDEX_TICKERS = {
    "^KS11": "코스피",
    "^KQ11": "코스닥",
}


def collect_data():
    """yfinance로 지수 + 종목 데이터 수집"""
    try:
        import yfinance as yf
    except ImportError:
        print("[WARN] yfinance 미설치")
        return [], "지수 데이터 없음"

    print("데이터 수집 중...")

    # 지수
    index_parts = []
    for ticker, name in INDEX_TICKERS.items():
        try:
            df = yf.Ticker(ticker).history(period="2d")
            if len(df) >= 2:
                chg = (df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2] * 100
                index_parts.append(f"{name} {chg:+.2f}%")
        except Exception as e:
            print(f"  지수 {name} 실패: {e}")
    index_summary = ", ".join(index_parts) if index_parts else "지수 데이터 없음"

    # 종목
    stocks = []
    for ticker, name in TARGET_STOCKS.items():
        try:
            df = yf.Ticker(ticker).history(period="2d")
            if len(df) < 2:
                continue
            prev  = df['Close'].iloc[-2]
            close = df['Close'].iloc[-1]
            vol   = df['Volume'].iloc[-1]
            chg   = (close - prev) / prev * 100
            trade = round(close * vol / 1e8, 1)   # 억원 단위 (1억 = 10^8)
            stocks.append({
                "stock_name":    name,
                "change_rate":   f"{chg:+.1f}%",
                "trading_value": f"{trade}억원",
            })
            print(f"  {name}: {chg:+.1f}%, {trade}억원")
        except Exception as e:
            print(f"  {name} 실패: {e}")

    return stocks, index_summary


def analyze(stocks, index_summary):
    """Claude API로 테마 분석 JSON 생성"""
    today = datetime.utcnow().strftime("%Y-%m-%d")

    if not stocks:
        return {
            "date": today,
            "market_summary": "데이터가 입력되지 않았습니다.",
            "themeRankList": []
        }

    prompt = f"""너는 xinvest.site의 주식 테마 분석 엔진이다.

[입력 데이터]
기준일: {today}
지수: {index_summary}
종목: {json.dumps(stocks, ensure_ascii=False)}

[분석 지침]
1. 위 종목들을 산업 섹터/최근 뉴스 테마로 묶어 최대 3개 주도 테마 추출
2. 거래대금 + 상승률 기준으로 각 테마의 대장주/부대장주 분류
3. 각 테마 상승 이유를 주식 초보자도 이해할 수 있는 2줄로 요약
4. strength_score는 1(약함)~5(강함) 정수

[출력 규칙]
- 순수 JSON만 반환 (마크다운 코드블록, 설명, 인사말 완전 금지)
- 아래 구조 정확히 준수, 문법 오류 없을 것

{{"date":"{today}","market_summary":"국장 전체 흐름 1줄","themeRankList":[{{"theme_name":"테마명","strength_score":5,"reason":"상승 이유 2줄","stocks":[{{"stock_name":"종목명","role":"대장주","change_rate":"+0.0%","trading_value":"000억원"}},{{"stock_name":"종목명","role":"부대장주","change_rate":"+0.0%","trading_value":"000억원"}}]}}]}}"""

    print("Claude API 테마 분석 중...")
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = resp.content[0].text.strip()

    # JSON 파싱 검증
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[WARN] JSON 파싱 실패: {e}")
        return {
            "date": today,
            "market_summary": "분석 결과 파싱에 실패했습니다.",
            "themeRankList": []
        }


def main():
    stocks, index_summary = collect_data()
    result = analyze(stocks, index_summary)

    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    count = len(result.get("themeRankList", []))
    print(f"\n✅ 완료: {count}개 테마 → data/themes.json")
    print(f"   요약: {result.get('market_summary', '-')}")


if __name__ == "__main__":
    main()
