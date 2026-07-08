"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getQuiz } from "@/data/quizzes";
import { RESULTS_STORAGE_KEY, type StoredResult } from "./SaveResult";

interface Entry {
  slug: string;
  quizTitle: string;
  resultName: string;
  color: string;
  href: string;
}

/** 홈 화면 — localStorage에 저장된 지난 검사 결과 바로가기. */
export default function LastResults() {
  const [entries, setEntries] = useState<Entry[]>([]);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(RESULTS_STORAGE_KEY);
      if (!raw) return;
      const data: Record<string, StoredResult> = JSON.parse(raw);
      const list: Entry[] = [];
      for (const [slug, stored] of Object.entries(data)) {
        const quiz = getQuiz(slug);
        const result = quiz?.results[stored.type];
        if (!quiz || !result) continue;
        list.push({
          slug,
          quizTitle: quiz.title,
          resultName: result.name,
          color: result.color,
          href: `/quiz/${slug}/result/${stored.type}`,
        });
      }
      setEntries(list);
    } catch {
      // 저장 데이터가 깨진 경우 무시
    }
  }, []);

  if (entries.length === 0) return null;

  return (
    <section className="mb-10">
      <h2 className="mb-3 text-sm font-semibold text-sub">지난 결과 보기</h2>
      <div className="flex flex-col gap-2">
        {entries.map((e) => (
          <Link
            key={e.slug}
            href={e.href}
            className="flex items-center gap-3 rounded-xl border border-line bg-card px-4 py-3 transition-shadow hover:shadow-md"
          >
            <span
              className="h-2.5 w-2.5 shrink-0 rounded-full"
              style={{ backgroundColor: e.color }}
            />
            <span className="text-sm text-sub">{e.quizTitle}</span>
            <span className="ml-auto text-sm font-semibold text-ink">
              {e.resultName} →
            </span>
          </Link>
        ))}
      </div>
    </section>
  );
}
