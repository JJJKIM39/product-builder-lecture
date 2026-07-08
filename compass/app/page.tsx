import Link from "next/link";
import AdSlot from "@/components/AdSlot";
import LastResults from "@/components/LastResults";
import { quizzes } from "@/data/quizzes";

const CATEGORY_META = {
  casual: { label: "캐주얼 검사", color: "#E8604C", note: "무료 · 가볍게" },
  formal: { label: "정식 검사", color: "#1B2A4A", note: "검증된 척도" },
  practical: { label: "실용 진단", color: "#7A9B7E", note: "상세 리포트 제공" },
} as const;

function QuizCard({
  slug,
  title,
  tagline,
  minutes,
  questionCount,
  category,
}: {
  slug: string;
  title: string;
  tagline: string;
  minutes: string;
  questionCount: number;
  category: keyof typeof CATEGORY_META;
}) {
  const meta = CATEGORY_META[category];
  return (
    <Link
      href={`/quiz/${slug}`}
      className="group block rounded-2xl border border-line bg-card p-6 transition-all duration-150 hover:-translate-y-0.5 hover:shadow-md"
    >
      <div className="flex items-center justify-between">
        <span
          className="rounded-full px-2.5 py-1 text-[11px] font-semibold text-white"
          style={{ backgroundColor: meta.color }}
        >
          {meta.label}
        </span>
        <span className="text-xs text-sub">
          {questionCount}문항 · 약 {minutes}
        </span>
      </div>
      <h3 className="mt-4 font-serif text-lg font-bold text-ink">{title}</h3>
      <p className="mt-1.5 text-sm leading-relaxed text-sub">{tagline}</p>
      <p className="mt-4 text-sm font-semibold text-indigo transition-transform duration-150 group-hover:translate-x-0.5">
        검사 시작하기 →
      </p>
    </Link>
  );
}

export default function HomePage() {
  const casual = quizzes.filter((q) => q.category === "casual");
  const practical = quizzes.filter((q) => q.category === "practical");

  return (
    <div className="mx-auto max-w-[720px] px-5 py-12">
      {/* 히어로 */}
      <section className="mb-14 text-center">
        <h1 className="font-serif text-[28px] font-bold leading-snug text-ink sm:text-3xl">
          내 방향을 아는 것이,
          <br />
          다음 선택을 쉽게 만듭니다.
        </h1>
        <p className="mx-auto mt-4 max-w-md text-[15px] leading-relaxed text-sub">
          3분이면 충분해요. 나를 아는 만큼, 선택이 쉬워집니다.
        </p>
        <Link
          href="/quiz/energy-type"
          className="mx-auto mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-xl bg-ink px-6 text-base font-semibold text-white transition-colors hover:bg-black"
        >
          3분 만에 내 유형 알아보기
        </Link>
        <p className="mt-2 text-xs text-sub">회원가입 없이 바로 시작</p>
      </section>

      <LastResults />

      {/* 캐주얼 검사 */}
      <section className="mb-10">
        <h2 className="mb-3 font-serif text-base font-bold text-ink">
          가볍게 해보는 검사
        </h2>
        <div className="flex flex-col gap-4">
          {casual.map((q) => (
            <QuizCard
              key={q.slug}
              slug={q.slug}
              title={q.title}
              tagline={q.tagline}
              minutes={q.minutes}
              questionCount={q.questions.length}
              category={q.category as "casual"}
            />
          ))}
        </div>
      </section>

      {/* 정식 검사 — 준비 중 */}
      <section className="mb-10">
        <h2 className="mb-3 font-serif text-base font-bold text-ink">
          제대로 받아보는 정식 검사
        </h2>
        <div className="rounded-2xl border border-line bg-card/60 p-6">
          <div className="flex items-center justify-between">
            <span className="rounded-full bg-ink px-2.5 py-1 text-[11px] font-semibold text-white">
              정식 검사
            </span>
            <span className="rounded-full border border-line px-2.5 py-1 text-[11px] font-medium text-sub">
              준비 중
            </span>
          </div>
          <h3 className="mt-4 font-serif text-lg font-bold text-ink/50">
            Big5 성격검사
          </h3>
          <p className="mt-1.5 text-sm leading-relaxed text-sub">
            심리학계에서 가장 널리 검증된 5요인 성격 모델 기반의 정식 검사를
            준비하고 있어요.
          </p>
        </div>
      </section>

      {/* 실용 진단 */}
      <section className="mb-14">
        <h2 className="mb-3 font-serif text-base font-bold text-ink">
          다음 결정을 돕는 실용 진단
        </h2>
        <div className="flex flex-col gap-4">
          {practical.map((q) => (
            <QuizCard
              key={q.slug}
              slug={q.slug}
              title={q.title}
              tagline={q.tagline}
              minutes={q.minutes}
              questionCount={q.questions.length}
              category={q.category as "practical"}
            />
          ))}
        </div>
      </section>

      {/* 광고 — 콘텐츠와 명확히 분리 */}
      <div className="border-t border-line pt-8">
        <AdSlot />
      </div>

      {/* SEO 소개 문단 */}
      <p className="mt-10 text-[13px] leading-relaxed text-sub">
        나침반은 성격검사, 투자성향테스트 등 자기이해를 돕는 무료 심리테스트를
        제공합니다.
      </p>
    </div>
  );
}
