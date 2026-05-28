-- ============================================================
-- xinvest 경제/실적 캘린더 DB 스키마
-- SQLite / PostgreSQL 호환
-- (현재는 calendar.json으로 운영, 백엔드 확장 시 이 스키마 사용)
-- ============================================================

-- 기업 실적 발표 테이블
CREATE TABLE IF NOT EXISTS earnings_calendar (
    id            TEXT        PRIMARY KEY,
    ticker        TEXT        NOT NULL,
    name          TEXT        NOT NULL,
    country       CHAR(2)     NOT NULL CHECK (country IN ('US', 'KR', 'JP', 'EU')),
    date          DATE        NOT NULL,
    timing        TEXT        DEFAULT 'TBD'
                              CHECK (timing IN ('BMO', 'AMC', 'TBD')),
                              -- BMO: Before Market Open (장 시작 전)
                              -- AMC: After Market Close (장 마감 후)
    eps_estimate  REAL,       -- 예상 EPS
    eps_actual    REAL,       -- 실제 EPS (발표 후 채워짐)
    revenue_est   REAL,       -- 예상 매출 (억 USD)
    revenue_act   REAL,       -- 실제 매출
    created_at    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_earnings_date    ON earnings_calendar(date);
CREATE INDEX IF NOT EXISTS idx_earnings_country ON earnings_calendar(country);
CREATE INDEX IF NOT EXISTS idx_earnings_ticker  ON earnings_calendar(ticker);


-- 경제 지표 발표 테이블
CREATE TABLE IF NOT EXISTS economic_calendar (
    id            TEXT        PRIMARY KEY,
    name          TEXT        NOT NULL,           -- 지표명 (CPI, FOMC 등)
    country       CHAR(2)     NOT NULL,           -- US, KR, JP, EU, CN
    event_datetime DATETIME   NOT NULL,           -- 발표 일시 (KST)
    date          DATE        NOT NULL,           -- 날짜만 (캘린더 쿼리용)
    importance    INTEGER     NOT NULL DEFAULT 1
                              CHECK (importance BETWEEN 1 AND 3),
                              -- 1: 낮음(회색), 2: 중간(노랑), 3: 높음(빨강)
    previous      REAL,                           -- 이전치
    forecast      REAL,                           -- 예상치
    actual        REAL,                           -- 실제치 (발표 후)
    unit          TEXT,                           -- 단위 (%, 만명 등)
    created_at    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_eco_date       ON economic_calendar(date);
CREATE INDEX IF NOT EXISTS idx_eco_country    ON economic_calendar(country);
CREATE INDEX IF NOT EXISTS idx_eco_importance ON economic_calendar(importance);


-- 날짜별 전체 이벤트 조회 뷰 (프론트엔드 쿼리용)
CREATE VIEW IF NOT EXISTS calendar_by_date AS
SELECT
    id,
    'earnings'  AS type,
    date,
    NULL        AS event_datetime,
    ticker,
    name,
    country,
    timing,
    NULL        AS importance,
    eps_estimate AS estimate_val,
    eps_actual   AS actual_val
FROM earnings_calendar
UNION ALL
SELECT
    id,
    'economic'  AS type,
    date,
    event_datetime,
    NULL        AS ticker,
    name,
    country,
    NULL        AS timing,
    importance,
    forecast    AS estimate_val,
    actual      AS actual_val
FROM economic_calendar
ORDER BY date, event_datetime;
