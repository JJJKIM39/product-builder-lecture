#!/usr/bin/env python3
"""
xinvest.site — 경제지표 & 기업실적 캘린더 크롤러
GitHub Actions에서 매일 04:00 KST에 실행됩니다.
결과물: ../data/calendar.json
"""

import json
import time
import random
import os
import re
from datetime import datetime, timedelta, timezone, date

import requests
from bs4 import BeautifulSoup

# ── 상수 ─────────────────────────────────────────────────────────────────────

KST      = timezone(timedelta(hours=9))
TODAY    = datetime.now(KST).date()
CUTOFF   = TODAY + timedelta(weeks=8)   # 8주 앞까지 수집
OUTPUT   = os.path.join(os.path.dirname(__file__), '..', 'data', 'calendar.json')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
]

# 주요 미국 기업 티커 (실적 대상)
US_TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "JPM",
    "V",    "WMT",  "XOM",  "BAC",  "AMD",  "NFLX", "DIS",  "COIN",
    "GS",   "INTC", "ORCL", "CRM",  "ADBE", "QCOM", "MU",   "AVGO",
    "ARM",  "UBER", "SHOP", "PLTR", "SMCI", "MSTR",
]

# 주요 한국 기업 티커
KR_TICKERS = [
    "005930.KS",  # 삼성전자
    "000660.KS",  # SK하이닉스
    "035420.KS",  # NAVER
    "051910.KS",  # LG화학
    "005380.KS",  # 현대차
    "035720.KS",  # 카카오
    "068270.KS",  # 셀트리온
    "000270.KS",  # 기아
    "207940.KS",  # 삼성바이오로직스
    "006400.KS",  # 삼성SDI
    "373220.KS",  # LG에너지솔루션
    "003550.KS",  # LG
    "012330.KS",  # 현대모비스
    "105560.KS",  # KB금융
    "055550.KS",  # 신한지주
]

# ── 유틸 ─────────────────────────────────────────────────────────────────────

def headers():
    return {
        "User-Agent":      random.choice(USER_AGENTS),
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection":      "keep-alive",
        "Referer":         "https://www.google.com/",
    }

def delay(lo=1.5, hi=4.0):
    t = random.uniform(lo, hi)
    time.sleep(t)

def safe_float(val):
    if val is None:
        return None
    try:
        cleaned = re.sub(r'[^\d.\-+]', '', str(val))
        return round(float(cleaned), 4) if cleaned else None
    except:
        return None

def date_in_range(d):
    """date 또는 문자열(YYYY-MM-DD)이 TODAY~CUTOFF 범위인지 확인"""
    if isinstance(d, str):
        try:
            d = date.fromisoformat(d[:10])
        except:
            return False
    return TODAY <= d <= CUTOFF

# ── 1. 기업 실적 (yfinance) ──────────────────────────────────────────────────

def fetch_earnings() -> list:
    """yfinance로 주요 기업 실적 발표 날짜 수집"""
    try:
        import yfinance as yf
    except ImportError:
        print("[WARN] yfinance 미설치 — pip install yfinance")
        return []

    results = []
    all_tickers = US_TICKERS + KR_TICKERS

    for sym in all_tickers:
        try:
            ticker  = yf.Ticker(sym)
            info    = ticker.fast_info   # fast_info가 quota 부하 낮음
            country = "KR" if (".KS" in sym or ".KQ" in sym) else "US"

            # 종목명 취득
            try:
                name = ticker.info.get("longName") or ticker.info.get("shortName") or sym
            except:
                name = sym

            # 실적 날짜 목록
            try:
                earn_df = ticker.earnings_dates   # 과거+미래 포함
            except:
                earn_df = None

            if earn_df is not None and not earn_df.empty:
                for ts, row in earn_df.iterrows():
                    try:
                        d = ts.date() if hasattr(ts, 'date') else date.fromisoformat(str(ts)[:10])
                    except:
                        continue

                    if not date_in_range(d):
                        continue

                    eps_est = safe_float(row.get("EPS Estimate"))
                    eps_act = safe_float(row.get("Reported EPS"))

                    results.append({
                        "id":          f"earn_{sym}_{d}",
                        "type":        "earnings",
                        "ticker":      sym.split(".")[0],
                        "name":        name,
                        "country":     country,
                        "date":        d.strftime("%Y-%m-%d"),
                        "timing":      "TBD",     # yfinance 미제공 시 TBD
                        "eps_estimate": eps_est,
                        "eps_actual":  eps_act,
                    })

            delay(0.5, 1.5)   # 짧게 (yfinance는 로컬 파싱 위주)

        except Exception as e:
            print(f"  [{sym}] 오류: {e}")
            delay(2.0, 4.0)

    print(f"[Earnings] {len(results)}개 수집")
    return results


# ── 2. 경제 지표 — 네이버 페이 증권 ─────────────────────────────────────────

def fetch_naver_economic() -> list:
    """
    네이버 페이 증권 > 세계 경제 지표 캘린더 크롤링
    URL: https://finance.naver.com/marketindex/worldEconomicCalendar.naver
    """
    results = []
    session = requests.Session()

    # 주 단위로 요청 (월요일 기준)
    checked = set()
    cur = TODAY - timedelta(days=TODAY.weekday())   # 이번 주 월요일
    end = CUTOFF

    while cur <= end:
        week_key = cur.strftime("%Y%m%d")
        if week_key in checked:
            cur += timedelta(weeks=1)
            continue
        checked.add(week_key)

        url = "https://finance.naver.com/marketindex/worldEconomicCalendar.naver"
        params = {"date": week_key}

        try:
            resp = session.get(url, headers=headers(), params=params, timeout=20)
            resp.encoding = "utf-8"

            if resp.status_code != 200:
                print(f"  [Naver Eco] HTTP {resp.status_code} / 주: {week_key}")
                delay(3, 6)
                cur += timedelta(weeks=1)
                continue

            soup = BeautifulSoup(resp.text, "lxml")

            # 날짜별 그룹 블록 파싱
            # 네이버는 날짜별 <div class="date_area"> 구조 사용
            date_blocks = soup.select("div.date_area, .economicCal_area")

            if not date_blocks:
                # fallback: 테이블 직접 파싱
                rows = soup.select("table tbody tr")
                _parse_naver_table_rows(rows, results, cur)
            else:
                for block in date_blocks:
                    date_txt = block.select_one(".tit_date, .date")
                    if not date_txt:
                        continue
                    try:
                        # 형식: "06.10(화)" → 같은 해 month.day
                        raw = date_txt.get_text(strip=True)[:5]   # "06.10"
                        mo, da = raw.split(".")
                        row_date = date(cur.year, int(mo), int(da))
                    except:
                        row_date = cur

                    rows = block.select("tr")
                    for row in rows:
                        _parse_naver_eco_row(row, row_date, results)

            delay(2.0, 4.5)

        except Exception as e:
            print(f"  [Naver Eco] 예외: {e}")
            delay(4, 8)

        cur += timedelta(weeks=1)

    print(f"[Naver Economic] {len(results)}개 수집")
    return results


def _parse_naver_eco_row(row, row_date: date, results: list):
    """네이버 경제 지표 테이블 행 파싱 (selector 유연 처리)"""
    try:
        cells = row.find_all("td")
        if len(cells) < 3:
            return

        # 지표명
        name_el = (row.select_one(".tit_item, .item_name, td:nth-child(2) a")
                   or row.select_one("td:nth-child(1)"))
        name = name_el.get_text(strip=True) if name_el else ""
        if not name or len(name) < 2:
            return

        # 국가 (국기 이미지 alt 또는 클래스)
        flag_el = row.select_one("img[src*='country'], span.flag, .ico_flag")
        country = "US"
        if flag_el:
            alt = flag_el.get("alt", "")
            src = flag_el.get("src", "")
            if "kr" in alt.lower() or "kor" in src.lower():
                country = "KR"
            elif "eu" in alt.lower() or "eur" in src.lower():
                country = "EU"
            elif "jp" in alt.lower() or "jpn" in src.lower():
                country = "JP"
            elif "cn" in alt.lower() or "chn" in src.lower():
                country = "CN"

        # 중요도 (★ 개수 or 클래스)
        imp_el = row.select_one(".ico_star, .imp, .star_wrap")
        importance = 1
        if imp_el:
            star_imgs = imp_el.find_all("img", alt="★") or imp_el.find_all(class_=re.compile(r"star|active"))
            importance = min(3, max(1, len(star_imgs) or 1))

        # 시각
        time_el = row.select_one(".time, td.num:first-child")
        time_str = time_el.get_text(strip=True) if time_el else "00:00"
        if not re.match(r"\d{2}:\d{2}", time_str):
            time_str = "00:00"

        # 전기치 / 예상치 / 실제치
        nums = [c.get_text(strip=True) for c in cells if c.get_text(strip=True)]
        prev_val = safe_float(nums[-3]) if len(nums) >= 3 else None
        fore_val = safe_float(nums[-2]) if len(nums) >= 2 else None
        act_val  = safe_float(nums[-1]) if len(nums) >= 1 else None

        if not date_in_range(row_date):
            return

        results.append({
            "id":         f"eco_naver_{row_date}_{len(results)}",
            "type":       "economic",
            "name":       name,
            "country":    country,
            "datetime":   f"{row_date.strftime('%Y-%m-%d')} {time_str}",
            "date":       row_date.strftime("%Y-%m-%d"),
            "importance": importance,
            "previous":   prev_val,
            "forecast":   fore_val,
            "actual":     act_val,
        })
    except Exception:
        pass


def _parse_naver_table_rows(rows, results: list, week_start: date):
    """fallback: 단순 테이블 rows 파싱"""
    for row in rows:
        _parse_naver_eco_row(row, week_start, results)


# ── 3. 연준 FOMC 일정 ────────────────────────────────────────────────────────

def fetch_fomc() -> list:
    """
    연준 공식 사이트에서 FOMC 회의 일정 크롤링
    URL: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
    """
    results = []
    MONTHS = {
        "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
        "July":7,"August":8,"September":9,"October":10,"November":11,"December":12
    }

    try:
        url  = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
        resp = requests.get(url, headers=headers(), timeout=20)
        soup = BeautifulSoup(resp.text, "lxml")

        # 연도별 패널
        for panel in soup.select(".panel.panel-default, .fomc-meeting"):
            header = panel.select_one(".panel-heading h4, .panel-title")
            if not header:
                continue
            year_match = re.search(r"\d{4}", header.get_text())
            if not year_match:
                continue
            year = int(year_match.group())
            if year < TODAY.year:
                continue

            # 회의 행
            for row in panel.select("tr"):
                cells = row.find_all(["td", "th"])
                if not cells:
                    continue
                cell_text = cells[0].get_text(strip=True) if cells else ""

                # 예: "January 28-29*" 또는 "March 18-19"
                m = re.match(r"([A-Za-z]+)\s+(\d+)[-–](\d+)\*?", cell_text)
                if not m:
                    # 단일일: "January 29"
                    m2 = re.match(r"([A-Za-z]+)\s+(\d+)\*?", cell_text)
                    if not m2:
                        continue
                    month_name, day2 = m2.group(1), int(m2.group(2))
                else:
                    month_name, day2 = m.group(1), int(m.group(3))

                month_num = MONTHS.get(month_name)
                if not month_num:
                    continue

                try:
                    meet_date = date(year, month_num, day2)
                except ValueError:
                    continue

                if not date_in_range(meet_date):
                    continue

                # 발표 당일 오후 2시(ET) = 03:00 KST 다음날 이지만 편의상 당일 표기
                results.append({
                    "id":         f"fomc_{meet_date}",
                    "type":       "economic",
                    "name":       "FOMC 금리 결정",
                    "country":    "US",
                    "datetime":   f"{meet_date.strftime('%Y-%m-%d')} 03:00",
                    "date":       meet_date.strftime("%Y-%m-%d"),
                    "importance": 3,
                    "previous":   None,
                    "forecast":   None,
                    "actual":     None,
                })

        delay()

    except Exception as e:
        print(f"[FOMC] 크롤링 오류: {e}")

    print(f"[FOMC] {len(results)}개 수집")
    return results


# ── 4. BLS 주요 지표 일정 (CPI / NFP) ────────────────────────────────────────

def fetch_bls_schedule() -> list:
    """
    미국 노동통계국(BLS) 공개 캘린더에서 CPI·비농업고용 발표일 수집
    https://www.bls.gov/schedule/news_release/home.htm
    """
    results = []
    TARGETS = {
        "Consumer Price Index":    ("CPI 물가지수",    2),
        "Employment Situation":    ("비농업고용(NFP)", 3),
        "Producer Price Index":    ("PPI 생산자물가",  2),
        "Retail Sales":            ("소매판매",        2),
        "GDP":                     ("GDP 성장률",       3),
    }

    try:
        url  = "https://www.bls.gov/schedule/news_release/home.htm"
        resp = requests.get(url, headers=headers(), timeout=20)
        soup = BeautifulSoup(resp.text, "lxml")

        for row in soup.select("table tr"):
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue

            release_name = cells[0].get_text(strip=True)
            date_text    = cells[1].get_text(strip=True) if len(cells) > 1 else ""

            matched_key = None
            for key in TARGETS:
                if key.lower() in release_name.lower():
                    matched_key = key
                    break
            if not matched_key:
                continue

            # 날짜 파싱: "Wednesday, June 12, 2024" 또는 "06/12/2024"
            try:
                d = None
                # ISO: 2024-06-12
                m = re.search(r"(\d{4}-\d{2}-\d{2})", date_text)
                if m:
                    d = date.fromisoformat(m.group(1))
                else:
                    # "Month DD, YYYY"
                    m2 = re.search(r"([A-Za-z]+)\s+(\d+),\s*(\d{4})", date_text)
                    if m2:
                        from datetime import datetime as dt
                        d = dt.strptime(f"{m2.group(1)} {m2.group(2)} {m2.group(3)}", "%B %d %Y").date()
                    else:
                        # MM/DD/YYYY
                        m3 = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", date_text)
                        if m3:
                            d = date(int(m3.group(3)), int(m3.group(1)), int(m3.group(2)))

                if d and date_in_range(d):
                    kr_name, imp = TARGETS[matched_key]
                    results.append({
                        "id":         f"bls_{matched_key.replace(' ','_')}_{d}",
                        "type":       "economic",
                        "name":       kr_name,
                        "country":    "US",
                        "datetime":   f"{d.strftime('%Y-%m-%d')} 21:30",  # 대부분 동부 8:30 = KST 21:30
                        "date":       d.strftime("%Y-%m-%d"),
                        "importance": imp,
                        "previous":   None,
                        "forecast":   None,
                        "actual":     None,
                    })
            except Exception:
                pass

        delay()

    except Exception as e:
        print(f"[BLS] 크롤링 오류: {e}")

    print(f"[BLS] {len(results)}개 수집")
    return results


# ── 메인 ─────────────────────────────────────────────────────────────────────

def main():
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")
    print(f"\n{'='*55}")
    print(f"  xinvest 캘린더 크롤러 시작  [{now_kst}]")
    print(f"  수집 범위: {TODAY} ~ {CUTOFF}")
    print(f"{'='*55}\n")

    all_events: list = []

    # ① 기업 실적
    print("[1/4] 기업 실적 크롤링 (yfinance)...")
    all_events.extend(fetch_earnings())

    # ② 네이버 경제 지표
    print("\n[2/4] 네이버 경제 지표 크롤링...")
    all_events.extend(fetch_naver_economic())

    # ③ FOMC
    print("\n[3/4] FOMC 일정 크롤링...")
    all_events.extend(fetch_fomc())

    # ④ BLS
    print("\n[4/4] BLS(CPI/NFP) 일정 크롤링...")
    all_events.extend(fetch_bls_schedule())

    # ─ 중복 제거 (id 기준)
    seen, unique = set(), []
    for ev in all_events:
        if ev["id"] not in seen:
            seen.add(ev["id"])
            unique.append(ev)

    # ─ 날짜 정렬
    unique.sort(key=lambda x: x.get("datetime") or x.get("date", ""))

    # ─ 출력 JSON
    output = {
        "updated_at": datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "range_from": TODAY.strftime("%Y-%m-%d"),
        "range_to":   CUTOFF.strftime("%Y-%m-%d"),
        "count":      len(unique),
        "events":     unique,
    }

    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*55}")
    print(f"  ✅ 완료: {len(unique)}개 이벤트 → data/calendar.json")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
