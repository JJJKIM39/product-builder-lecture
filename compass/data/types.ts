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
