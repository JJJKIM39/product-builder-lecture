"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Quiz, QuizQuestion } from "@/data/types";
import { computeResult } from "@/data/quizzes";

function shuffle<T>(arr: T[]): T[] {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export default function QuizRunner({ quiz }: { quiz: Quiz }) {
  const router = useRouter();
  const [picks, setPicks] = useState<string[]>([]);
  const [navigating, setNavigating] = useState(false);
  const [questions, setQuestions] = useState<QuizQuestion[]>(quiz.questions);

  // 선택지 순서 랜덤화 — SSR 마크업과의 hydration 불일치를 피하기 위해 마운트 후 셔플
  useEffect(() => {
    setQuestions(
      quiz.questions.map((q) => ({ ...q, options: shuffle(q.options) }))
    );
  }, [quiz]);

  const total = questions.length;
  const step = Math.min(picks.length, total - 1);
  const question = questions[step];
  const accent = quiz.category === "practical" ? "#7A9B7E" : "#E8604C";
  const progress = (picks.length / total) * 100;

  function select(type: string) {
    if (navigating) return;
    const next = [...picks, type];
    if (next.length === total) {
      setNavigating(true);
      const winner = computeResult(quiz, next);
      router.push(`/quiz/${quiz.slug}/result/${winner}`);
      return;
    }
    setPicks(next);
  }

  function goBack() {
    if (navigating || picks.length === 0) return;
    setPicks(picks.slice(0, -1));
  }

  return (
    <div className="mx-auto max-w-[560px] px-5 py-10">
      {/* 진행 바 */}
      <div className="mb-8">
        <div className="mb-2 flex items-center justify-between text-xs font-medium text-sub">
          <span>{quiz.title}</span>
          <span>
            Q{step + 1} <span className="text-sub/60">/ {total}</span>
          </span>
        </div>
        <div className="h-1.5 w-full overflow-hidden rounded-full bg-line/70">
          <div
            className="h-full rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progress}%`, backgroundColor: accent }}
          />
        </div>
      </div>

      {/* 질문 */}
      <div key={step} className="animate-fade-up">
        <h1 className="font-serif text-xl font-bold leading-relaxed text-ink">
          {question.q}
        </h1>

        <div className="mt-6 flex flex-col gap-3">
          {question.options.map((opt, i) => (
            <button
              key={i}
              onClick={() => select(opt.type)}
              disabled={navigating}
              className="group w-full rounded-xl border border-line bg-card px-5 py-4 text-left text-[15px] leading-relaxed text-ink transition-all duration-150 hover:-translate-y-0.5 hover:shadow-md disabled:opacity-60"
              style={{ WebkitTapHighlightColor: "transparent" }}
              onMouseEnter={(e) => (e.currentTarget.style.borderColor = accent)}
              onMouseLeave={(e) => (e.currentTarget.style.borderColor = "")}
            >
              {opt.text}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-8 flex items-center justify-between text-sm text-sub">
        {picks.length === 0 ? (
          <Link
            href={`/quiz/${quiz.slug}`}
            className="transition-colors hover:text-ink"
          >
            ← 검사 소개로
          </Link>
        ) : (
          <button
            onClick={goBack}
            disabled={navigating}
            className="transition-colors hover:text-ink"
          >
            ← 이전 질문
          </button>
        )}
        {navigating && <span>결과를 계산하는 중…</span>}
      </div>
    </div>
  );
}
