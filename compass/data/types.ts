export type QuizCategory = "casual" | "formal" | "practical";

export interface QuizOption {
  text: string;
  /** 이 선택지가 매핑되는 결과 타입 키 (Quiz.results의 키) */
  type: string;
}

export interface QuizQuestion {
  q: string;
  options: QuizOption[];
}

/** 유료 리포트 섹션의 노출 수준 */
export type ReportVisibility = "free" | "partial" | "locked";

export interface ReportSection {
  /** 섹션 제목 */
  title: string;
  /** 목차·미리보기에 쓰이는 한 줄 설명 */
  summary: string;
  /** 본문 (현재는 placeholder — 다음 작업에서 유형별 실제 내용으로 교체) */
  body: string;
  /** free=전체 공개, partial=앞부분만, locked=잠금(더미) */
  visibility: ReportVisibility;
}

export interface QuizResult {
  /** 유형명 */
  name: string;
  /** 한 줄 요약 */
  tagline: string;
  /** 상세 해설 (문단은 \n\n으로 구분) */
  desc: string;
  /** 결과 다이얼·OG 이미지에 쓰이는 대표 컬러 (hex) */
  color: string;
  /** 강점 */
  strengths: string[];
  /** 주의할 점 / 전형적 함정 */
  cautions: string[];
  /** 어울리는 환경·스타일 */
  fit: string;
  /** 성장 포인트 한 줄 */
  growthTip: string;
  /** 유료 리포트 미리보기 (실용 진단 전용) */
  reportPreview?: ReportSection[];
}

export interface Quiz {
  slug: string;
  title: string;
  tagline: string;
  category: QuizCategory;
  /** 예상 소요 시간 표기 (예: "3분") */
  minutes: string;
  /** 인트로 — "이 검사로 알 수 있는 것" 체크 리스트 (3개) */
  introHighlights: string[];
  /** 인트로 — "이 검사는 어떻게 만들어졌나요?" 설명 */
  methodology: string;
  /** 결과 페이지 최하단에 노출되는 면책 문구 */
  disclaimer?: string;
  questions: QuizQuestion[];
  results: Record<string, QuizResult>;
}
