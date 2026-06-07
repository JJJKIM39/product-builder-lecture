#!/usr/bin/env python3
"""
xinvest.site — 글로벌 지수 데이터 수집
평일 장 마감 후 GitHub Actions에서 실행
"""
import os, json
import yfinance as yf
from datetime import datetime

OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'indices.json')

INDICES = [
    ("^KS11",  "KOSPI",  "코스피"),
    ("^KQ11",  "KOSDAQ", "코스닥"),
    ("^GSPC",  "SP500",  "S&P500"),
    ("^IXIC",  "NASDAQ", "나스닥"),
    ("^DJI",   "DOW",    "다우존스"),
]

def main():
    results = []
    for ticker, id_, name in INDICES:
        try:
            df = yf.Ticker(ticker).history(period="2d")
            if len(df) < 2:
                results.append({"id": id_, "name": name, "price": "—", "changePct": 0})
                continue
            prev  = df['Close'].iloc[-2]
            close = df['Close'].iloc[-1]
            pct   = (close - prev) / prev * 100
            # 가격 포맷
            if id_ in ("KOSPI", "KOSDAQ"):
                price_str = f"{close:,.2f}"
            else:
                price_str = f"{close:,.2f}"
            results.append({"id": id_, "name": name, "price": price_str, "changePct": round(pct, 2)})
            print(f"  {name}: {price_str} ({pct:+.2f}%)")
        except Exception as e:
            print(f"  {name} 실패: {e}")
            results.append({"id": id_, "name": name, "price": "—", "changePct": 0})

    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = {"date": today, "indices": results}
    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n완료: data/indices.json 저장")

if __name__ == "__main__":
    main()
