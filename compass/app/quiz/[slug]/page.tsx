import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getQuiz, quizzes } from "@/data/quizzes";

interface Props {
  params: { slug: string };
}

export function generateStaticParams() {
  return quizzes.map((q) => ({ slug: q.slug }));
}

export function generateMetadata({ params }: Props): Metadata {
  const quiz = getQuiz(params.slug);
  if (!quiz) return {};
  return {
    title: quiz.title,
    description: `${quiz.tagline} — ${quiz.questions.length}문항, 약 ${quiz.minutes}. 무료 ${
      quiz.category === "practical" ? "투자성향테스트" : "성격검사"
    }를 지금 바로 시작해 보세요.`,
  };
}

function CheckIcon() {
  return (
    <svg
      className="mt-0.5 h-4 w-4 shrink-0"
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden="true"
    >
      <circle cx="10" cy="10" r="9" stroke="#E8604C" strokeWidth="1.5" />
      <path
        d="M6 10.5l2.5 2.5L14 7.5"
        stroke="#E8604C"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function QuizIntroPage({ params }: Props) {
  const quiz = getQuiz(params.slug);
  if (!quiz) notFound();

  return (
    <div className="mx-auto flex min-h-[calc(100vh-3.5rem)] max-w-[560px] flex-col px-5 py-8">
      {/* 제목 + 태그라인 */}
      <h1 className="font-serif text-2xl font-bold leading-snug text-ink">
        {quiz.title}
      </h1>
      <p className="mt-2 text-[15px] leading-relaxed text-ink/75">
        {quiz.tagline}
      </p>

      {/* 메타 정보 */}
      <p className="mt-3 text-sm font-medium text-sub">
        {quiz.questions.length}문항 · 약 {quiz.minutes}
      </p>

      {/* 이 검사로 알 수 있는 것 */}
      <section className="mt-6 rounded-2xl border border-line bg-card p-5">
        <h2 className="mb-3 text-sm font-bold text-ink">
          이 검사로 알 수 있는 것
        </h2>
        <ul className="space-y-2.5">
          {quiz.introHighlights.map((h, i) => (
            <li
              key={i}
              className="flex gap-2.5 text-[14px] leading-relaxed text-ink/85"
            >
              <CheckIcon />
              <span>{h}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* 검사 방법론 — 접이식 */}
      <details className="group mt-3 rounded-xl border border-line bg-white/60 px-5 py-3.5">
        <summary className="cursor-pointer list-none text-sm font-medium text-ink/70 transition-colors hover:text-ink [&::-webkit-details-marker]:hidden">
          이 검사는 어떻게 만들어졌나요?
          <span className="float-right text-sub transition-transform group-open:rotate-180">
            ⌄
          </span>
        </summary>
        <p className="mt-3 text-[13px] leading-relaxed text-sub">
          {quiz.methodology}
        </p>
      </details>

      {/* 안내 문구 + CTA — 모바일에서 첫 화면에 보이도록 하단 고정 배치 */}
      <div className="mt-auto pt-8">
        <p className="mb-4 text-center text-[13px] leading-relaxed text-sub">
          정답은 없습니다. 너무 오래 고민하지 말고,
          <br />
          처음 떠오르는 대로 답해주세요.
        </p>
        <Link
          href={`/quiz/${quiz.slug}/start`}
          className="block w-full rounded-xl bg-coral px-6 py-4 text-center text-base font-semibold text-white transition-opacity hover:opacity-90 active:opacity-80"
        >
          검사 시작하기
        </Link>
      </div>
    </div>
  );
}
