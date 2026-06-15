#!/usr/bin/env python3
"""
xinvest.site — 경제지표 & 기업실적 캘린더 크롤러 v2
GitHub Actions에서 매일 04:00 KST에 실행됩니다.

변경 사항:
- yfinance ticker.info 제거 (429 차단 원인) → 회사명 하드코딩
- 경제 지표: 스크래핑 → 공개 확정 일정 하드코딩 (FOMC·CPI·NFP 등)
- yfinance earnings_dates만 사용 (IP 차단 우회)
"""

import json, time, random, os, re
from datetime import datetime, timedelta, timezone, date

KST    = timezone(timedelta(hours=9))
TODAY  = datetime.now(KST).date()
PAST   = date(TODAY.year, 1, 1)       # 올해 1월 1일부터
CUTOFF = date(TODAY.year, 12, 31)     # 올해 12월 31일까지
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'calendar.json')

# ── 회사명 사전 (ticker.info 호출 없이 사용) ─────────────────────────────────
COMPANY_NAMES = {
    # US
    "AAPL": "Apple Inc.", "MSFT": "Microsoft", "NVDA": "NVIDIA",
    "GOOGL": "Alphabet (Google)", "AMZN": "Amazon", "META": "Meta Platforms",
    "TSLA": "Tesla", "JPM": "JPMorgan Chase", "V": "Visa", "WMT": "Walmart",
    "XOM": "ExxonMobil", "BAC": "Bank of America", "AMD": "AMD",
    "NFLX": "Netflix", "DIS": "Disney", "COIN": "Coinbase", "GS": "Goldman Sachs",
    "INTC": "Intel", "ORCL": "Oracle", "CRM": "Salesforce", "ADBE": "Adobe",
    "QCOM": "Qualcomm", "MU": "Micron Technology", "AVGO": "Broadcom",
    "ARM": "Arm Holdings", "UBER": "Uber", "SHOP": "Shopify",
    "PLTR": "Palantir", "SMCI": "Super Micro Computer", "MSTR": "MicroStrategy",
    # KR
    "005930": "삼성전자", "000660": "SK하이닉스", "035420": "NAVER",
    "051910": "LG화학", "005380": "현대차", "035720": "카카오",
    "068270": "셀트리온", "000270": "기아", "207940": "삼성바이오로직스",
    "006400": "삼성SDI", "373220": "LG에너지솔루션", "003550": "LG",
    "012330": "현대모비스", "105560": "KB금융", "055550": "신한지주",
}

US_TICKERS = [
    "AAPL","MSFT","NVDA","GOOGL","AMZN","META","TSLA","JPM",
    "V","WMT","XOM","BAC","AMD","NFLX","DIS","COIN","GS",
    "INTC","ORCL","CRM","ADBE","QCOM","MU","AVGO","ARM",
    "UBER","SHOP","PLTR","SMCI","MSTR",
]
KR_TICKERS = [
    "005930.KS","000660.KS","035420.KS","051910.KS","005380.KS",
    "035720.KS","068270.KS","000270.KS","207940.KS","006400.KS",
    "373220.KS","003550.KS","012330.KS","105560.KS","055550.KS",
]

def delay(lo=2.0, hi=5.0):
    time.sleep(random.uniform(lo, hi))

def safe_float(val):
    try:
        return round(float(re.sub(r'[^\d.\-]', '', str(val))), 4)
    except:
        return None

def date_ok(d):
    if isinstance(d, str):
        try: d = date.fromisoformat(d[:10])
        except: return False
    return PAST <= d <= CUTOFF

# ── 1. 기업 실적 (yfinance — earnings_dates만 사용) ──────────────────────────

def fetch_earnings():
    try:
        import yfinance as yf
    except ImportError:
        print("[WARN] yfinance 미설치")
        return []

    results = []

    for sym in US_TICKERS + KR_TICKERS:
        base   = sym.split(".")[0]
        country = "KR" if (".KS" in sym or ".KQ" in sym) else "US"
        name   = COMPANY_NAMES.get(base, base)

        try:
            tk = yf.Ticker(sym)
            df = tk.get_earnings_dates(limit=16)  # 과거 4분기 + 미래 4분기 커버

            if df is None or df.empty:
                delay(0.5, 1.5)
                continue

            for ts, row in df.iterrows():
                try:
                    d = ts.date() if hasattr(ts, 'date') else date.fromisoformat(str(ts)[:10])
                except:
                    continue

                if not date_ok(d):
                    continue

                results.append({
                    "id":           f"earn_{base}_{d}",
                    "type":         "earnings",
                    "ticker":       base,
                    "name":         name,
                    "country":      country,
                    "date":         d.strftime("%Y-%m-%d"),
                    "timing":       "TBD",
                    "eps_estimate": safe_float(row.get("EPS Estimate")),
                    "eps_actual":   safe_float(row.get("Reported EPS")),
                })

        except Exception as e:
            print(f"  [{sym}] {e}")

        delay(1.5, 3.5)   # 넉넉히 딜레이

    print(f"[Earnings] {len(results)}개 수집")
    return results


# ── 2. 경제 지표 — 공개 확정 일정 하드코딩 ──────────────────────────────────
#
#  FOMC · CPI · NFP · PPI · GDP · 한국은행 기준금리는
#  수개월 전에 공개 발표되는 확정 일정입니다.
#  스크래핑보다 안정적이고 정확합니다.
#  매년 1월 초에 이 섹션만 업데이트하면 됩니다.
# ─────────────────────────────────────────────────────────────────────────────

FIXED_ECONOMIC_SCHEDULE = [
    # ── 2026 FOMC 금리 결정 ──────────────────────────
    {"id":"fomc_2026-01-28","name":"FOMC 금리 결정","country":"US","date":"2026-01-28","datetime":"2026-01-28 04:00","importance":3,"previous":4.25,"forecast":4.25,"actual":4.25},
    {"id":"fomc_2026-03-18","name":"FOMC 금리 결정","country":"US","date":"2026-03-18","datetime":"2026-03-18 04:00","importance":3,"previous":4.25,"forecast":4.0,"actual":4.0},
    {"id":"fomc_2026-04-29","name":"FOMC 금리 결정","country":"US","date":"2026-04-29","datetime":"2026-04-29 04:00","importance":3,"previous":4.0,"forecast":4.0,"actual":4.0},
    {"id":"fomc_2026-06-17","name":"FOMC 금리 결정","country":"US","date":"2026-06-17","datetime":"2026-06-17 04:00","importance":3,"previous":4.0,"forecast":None,"actual":None},
    {"id":"fomc_2026-07-29","name":"FOMC 금리 결정","country":"US","date":"2026-07-29","datetime":"2026-07-29 04:00","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"fomc_2026-09-16","name":"FOMC 금리 결정","country":"US","date":"2026-09-16","datetime":"2026-09-16 04:00","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"fomc_2026-10-28","name":"FOMC 금리 결정","country":"US","date":"2026-10-28","datetime":"2026-10-28 04:00","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"fomc_2026-12-09","name":"FOMC 금리 결정","country":"US","date":"2026-12-09","datetime":"2026-12-09 04:00","importance":3,"previous":None,"forecast":None,"actual":None},

    # ── 2026 CPI 물가지수 ──────────────────────────────
    # CPI 발표일 = 데이터 기준월 다음달 (BLS 공식 일정, 2026 검증 완료)
    {"id":"cpi_2026-06-10","name":"CPI 물가지수","country":"US","date":"2026-06-10","datetime":"2026-06-10 21:30","importance":3,"previous":2.8,"forecast":None,"actual":None},
    {"id":"cpi_2026-07-14","name":"CPI 물가지수","country":"US","date":"2026-07-14","datetime":"2026-07-14 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"cpi_2026-08-12","name":"CPI 물가지수","country":"US","date":"2026-08-12","datetime":"2026-08-12 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"cpi_2026-09-11","name":"CPI 물가지수","country":"US","date":"2026-09-11","datetime":"2026-09-11 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"cpi_2026-10-14","name":"CPI 물가지수","country":"US","date":"2026-10-14","datetime":"2026-10-14 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"cpi_2026-11-10","name":"CPI 물가지수","country":"US","date":"2026-11-10","datetime":"2026-11-10 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"cpi_2026-12-10","name":"CPI 물가지수","country":"US","date":"2026-12-10","datetime":"2026-12-10 21:30","importance":3,"previous":None,"forecast":None,"actual":None},

    # ── 2026 비농업고용 NFP ────────────────────────────
    {"id":"nfp_2026-06-05","name":"비농업고용(NFP)","country":"US","date":"2026-06-05","datetime":"2026-06-05 21:30","importance":3,"previous":180000,"forecast":None,"actual":None},
    {"id":"nfp_2026-07-02","name":"비농업고용(NFP)","country":"US","date":"2026-07-02","datetime":"2026-07-02 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"nfp_2026-08-07","name":"비농업고용(NFP)","country":"US","date":"2026-08-07","datetime":"2026-08-07 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"nfp_2026-09-04","name":"비농업고용(NFP)","country":"US","date":"2026-09-04","datetime":"2026-09-04 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"nfp_2026-10-02","name":"비농업고용(NFP)","country":"US","date":"2026-10-02","datetime":"2026-10-02 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"nfp_2026-11-06","name":"비농업고용(NFP)","country":"US","date":"2026-11-06","datetime":"2026-11-06 21:30","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"nfp_2026-12-04","name":"비농업고용(NFP)","country":"US","date":"2026-12-04","datetime":"2026-12-04 21:30","importance":3,"previous":None,"forecast":None,"actual":None},

    # ── 2026 PPI 생산자물가 (BLS 공식 일정, CPI와 별도 — 2026 검증 완료) ──
    {"id":"ppi_2026-06-11","name":"PPI 생산자물가","country":"US","date":"2026-06-11","datetime":"2026-06-11 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ppi_2026-07-15","name":"PPI 생산자물가","country":"US","date":"2026-07-15","datetime":"2026-07-15 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ppi_2026-08-13","name":"PPI 생산자물가","country":"US","date":"2026-08-13","datetime":"2026-08-13 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ppi_2026-09-10","name":"PPI 생산자물가","country":"US","date":"2026-09-10","datetime":"2026-09-10 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ppi_2026-10-15","name":"PPI 생산자물가","country":"US","date":"2026-10-15","datetime":"2026-10-15 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ppi_2026-11-13","name":"PPI 생산자물가","country":"US","date":"2026-11-13","datetime":"2026-11-13 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ppi_2026-12-15","name":"PPI 생산자물가","country":"US","date":"2026-12-15","datetime":"2026-12-15 21:30","importance":2,"previous":None,"forecast":None,"actual":None},

    # ── 2026 소매판매 ──────────────────────────────────
    {"id":"retail_2026-06-17","name":"소매판매","country":"US","date":"2026-06-17","datetime":"2026-06-17 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"retail_2026-07-16","name":"소매판매","country":"US","date":"2026-07-16","datetime":"2026-07-16 21:30","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"retail_2026-08-14","name":"소매판매","country":"US","date":"2026-08-14","datetime":"2026-08-14 21:30","importance":2,"previous":None,"forecast":None,"actual":None},

    # ── 2026 GDP 성장률 ────────────────────────────────
    {"id":"gdp_2026-06-25","name":"GDP 성장률 (1분기 확정)","country":"US","date":"2026-06-25","datetime":"2026-06-25 21:30","importance":3,"previous":2.1,"forecast":None,"actual":None},
    {"id":"gdp_2026-09-24","name":"GDP 성장률 (2분기 확정)","country":"US","date":"2026-09-24","datetime":"2026-09-24 21:30","importance":3,"previous":None,"forecast":None,"actual":None},

    # ── 2026 ISM 제조업 PMI ───────────────────────────
    {"id":"ism_2026-06-01","name":"ISM 제조업 PMI","country":"US","date":"2026-06-01","datetime":"2026-06-01 23:00","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ism_2026-07-01","name":"ISM 제조업 PMI","country":"US","date":"2026-07-01","datetime":"2026-07-01 23:00","importance":2,"previous":None,"forecast":None,"actual":None},
    {"id":"ism_2026-08-03","name":"ISM 제조업 PMI","country":"US","date":"2026-08-03","datetime":"2026-08-03 23:00","importance":2,"previous":None,"forecast":None,"actual":None},

    # ── 한국은행 기준금리 결정 ─────────────────────────
    {"id":"bok_2026-05-28","name":"한국은행 기준금리 결정","country":"KR","date":"2026-05-28","datetime":"2026-05-28 10:00","importance":3,"previous":2.5,"forecast":2.25,"actual":None},
    {"id":"bok_2026-07-09","name":"한국은행 기준금리 결정","country":"KR","date":"2026-07-09","datetime":"2026-07-09 10:00","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"bok_2026-08-27","name":"한국은행 기준금리 결정","country":"KR","date":"2026-08-27","datetime":"2026-08-27 10:00","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"bok_2026-10-15","name":"한국은행 기준금리 결정","country":"KR","date":"2026-10-15","datetime":"2026-10-15 10:00","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"bok_2026-11-26","name":"한국은행 기준금리 결정","country":"KR","date":"2026-11-26","datetime":"2026-11-26 10:00","importance":3,"previous":None,"forecast":None,"actual":None},

    # ── ECB 기준금리 결정 ──────────────────────────────
    {"id":"ecb_2026-06-11","name":"ECB 기준금리 결정","country":"EU","date":"2026-06-11","datetime":"2026-06-11 21:15","importance":3,"previous":1.75,"forecast":1.5,"actual":None},
    {"id":"ecb_2026-07-23","name":"ECB 기준금리 결정","country":"EU","date":"2026-07-23","datetime":"2026-07-23 21:15","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"ecb_2026-09-10","name":"ECB 기준금리 결정","country":"EU","date":"2026-09-10","datetime":"2026-09-10 21:15","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"ecb_2026-10-29","name":"ECB 기준금리 결정","country":"EU","date":"2026-10-29","datetime":"2026-10-29 21:15","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"ecb_2026-12-17","name":"ECB 기준금리 결정","country":"EU","date":"2026-12-17","datetime":"2026-12-17 21:15","importance":3,"previous":None,"forecast":None,"actual":None},

    # ── BOJ 금리 결정 ──────────────────────────────────
    {"id":"boj_2026-06-16","name":"BOJ 금리 결정","country":"JP","date":"2026-06-16","datetime":"2026-06-16 12:00","importance":3,"previous":0.75,"forecast":0.75,"actual":None},
    {"id":"boj_2026-07-31","name":"BOJ 금리 결정","country":"JP","date":"2026-07-31","datetime":"2026-07-31 12:00","importance":3,"previous":None,"forecast":None,"actual":None},
    {"id":"boj_2026-09-18","name":"BOJ 금리 결정","country":"JP","date":"2026-09-18","datetime":"2026-09-18 12:00","importance":3,"previous":None,"forecast":None,"actual":None},
]

def fetch_economic():
    """공개 확정 일정에서 범위 내 이벤트 필터링"""
    results = []
    for ev in FIXED_ECONOMIC_SCHEDULE:
        if date_ok(ev["date"]):
            results.append({**ev, "type": "economic"})
    print(f"[Economic] {len(results)}개 수집 (확정 일정 기반)")
    return results


# ── 메인 ──────────────────────────────────────────────────────────────────────

def main():
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")
    print(f"\n{'='*55}")
    print(f"  xinvest 캘린더 크롤러 v2  [{now_kst}]")
    print(f"  수집 범위: {PAST} ~ {CUTOFF}")
    print(f"{'='*55}\n")

    all_events = []

    print("[1/2] 기업 실적 크롤링 (yfinance)...")
    all_events.extend(fetch_earnings())

    print("\n[2/2] 경제 지표 로드 (확정 일정)...")
    all_events.extend(fetch_economic())

    # 중복 제거
    seen, unique = set(), []
    for ev in all_events:
        if ev["id"] not in seen:
            seen.add(ev["id"])
            unique.append(ev)

    # 날짜 정렬
    unique.sort(key=lambda x: x.get("datetime") or x.get("date", ""))

    output = {
        "updated_at": datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "range_from": PAST.strftime("%Y-%m-%d"),
        "range_to":   CUTOFF.strftime("%Y-%m-%d"),
        "count":      len(unique),
        "events":     unique,
    }

    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*55}")
    print(f"  ✅ 완료: {len(unique)}개 → data/calendar.json")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    main()
