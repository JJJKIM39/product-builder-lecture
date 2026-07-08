"use client";

import type { ReportSection } from "@/data/types";
import { Toast, useToast } from "./Toast";

function LockIcon({ className = "" }: { className?: string }) {
  return (
    <svg
      className={`h-3.5 w-3.5 shrink-0 ${className}`}
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden="true"
    >
      <rect x="4" y="9" width="12" height="8" rx="1.5" stroke="currentColor" strokeWidth="1.4" />
      <path
        d="M6.5 9V6.5a3.5 3.5 0 017 0V9"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinecap="round"
      />
    </svg>
  );
}

/** partial 섹션 본문을 앞 2문장(선명)과 나머지(페이드+블러)로 나눈다. */
function splitPreview(body: string): { head: string; tail: string } {
  const sentences = body.split(/(?<=[.!?])\s+/);
  return {
    head: sentences.slice(0, 2).join(" "),
    tail: sentences.slice(2).join(" "),
  };
}

/**
 * 실용 진단(투자) 결과 페이지 전용 유료 리포트 미리보기.
 * 결제 연동 전까지 잠금 해제 버튼은 "준비 중" 토스트만 노출한다.
 */
export default function ReportPreview({
  sections,
}: {
  sections: ReportSection[];
}) {
  const { message, show } = useToast();

  const visible = sections.filter((s) => s.visibility !== "locked");
  const locked = sections.filter((s) => s.visibility === "locked");

  return (
    <section className="overflow-hidden rounded-2xl border border-line bg-card">
      {/* 헤더 */}
      <div className="border-b border-line p-6">
        <div className="flex items-center gap-2">
          <span className="text-xl" aria-hidden="true">
            📄
          </span>
          <h3 className="font-serif text-lg font-bold text-ink">
            투자 성향 상세 리포트
          </h3>
        </div>
        <p className="mt-1 text-sm text-sub">
          12페이지 · 진단부터 실전 처방까지
        </p>

        {/* 목차 */}
        <ol className="mt-5 overflow-hidden rounded-xl border border-line">
          {sections.map((s, i) => {
            const isLocked = s.visibility === "locked";
            return (
              <li
                key={i}
                className={`flex items-center gap-2.5 px-4 py-2.5 text-sm ${
                  i > 0 ? "border-t border-line" : ""
                }`}
              >
                <span className="w-4 text-center text-xs font-semibold tabular-nums text-sub">
                  {i + 1}
                </span>
                <span
                  className={isLocked ? "text-sub" : "font-medium text-ink"}
                >
                  {s.title}
                </span>
                {isLocked ? (
                  <LockIcon className="ml-auto text-sub" />
                ) : (
                  <span className="ml-auto text-[11px] font-medium text-indigo">
                    미리보기
                  </span>
                )}
              </li>
            );
          })}
        </ol>
      </div>

      {/* 미리보기 본문 */}
      <div className="space-y-4 p-6">
        {visible.map((s, i) => {
          if (s.visibility === "free") {
            return (
              <article
                key={i}
                className="rounded-xl border border-line bg-ivory/60 p-4"
              >
                <h4 className="text-sm font-bold text-ink">{s.title}</h4>
                <p className="mt-2 text-[13px] leading-relaxed text-ink/80">
                  {s.body}
                </p>
              </article>
            );
          }
          // partial: 앞부분 선명, 나머지 페이드+블러
          const { head, tail } = splitPreview(s.body);
          return (
            <article
              key={i}
              className="rounded-xl border border-line bg-ivory/60 p-4"
            >
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-bold text-ink">{s.title}</h4>
                <span className="text-[11px] font-medium text-indigo">
                  미리보기
                </span>
              </div>
              <p className="mt-2 text-[13px] leading-relaxed text-ink/80">
                {head}
              </p>
              {tail && (
                <p
                  aria-hidden="true"
                  className="mt-1.5 select-none text-[13px] leading-relaxed text-ink/80 blur-[2px]"
                  style={{
                    maskImage:
                      "linear-gradient(to bottom, black 0%, transparent 90%)",
                    WebkitMaskImage:
                      "linear-gradient(to bottom, black 0%, transparent 90%)",
                  }}
                >
                  {tail}
                </p>
              )}
            </article>
          );
        })}

        {/* 잠금 존 — 블러 처리된 더미 본문 + 오버레이 CTA */}
        <div className="relative max-h-[440px] overflow-hidden rounded-xl border border-line bg-ivory/60">
          <div className="space-y-5 p-4">
            {locked.map((s, i) => (
              <div key={i}>
                <div className="flex items-center gap-1.5">
                  <LockIcon className="text-sub" />
                  <h4 className="text-sm font-bold text-ink">{s.title}</h4>
                </div>
                <div
                  aria-hidden="true"
                  className="mt-2 select-none blur-[4px]"
                >
                  <p className="text-[13px] leading-relaxed text-ink/40">
                    {s.body}
                  </p>
                  <div className="mt-2 h-2.5 w-full rounded bg-line/70" />
                  <div className="mt-1.5 h-2.5 w-11/12 rounded bg-line/70" />
                  <div className="mt-1.5 h-2.5 w-3/4 rounded bg-line/70" />
                </div>
              </div>
            ))}
          </div>

          {/* 오버레이 CTA */}
          <div className="absolute inset-0 flex items-end bg-gradient-to-b from-transparent via-ivory/50 to-ivory">
            <div className="w-full p-4">
              <div className="rounded-2xl border border-line bg-card p-5 text-center shadow-lg">
                <p className="text-sm font-semibold leading-relaxed text-ink">
                  나머지 {locked.length}개 섹션과 실전 가이드를 확인하세요
                </p>
                <button
                  onClick={() =>
                    show("결제 기능을 준비 중입니다. 조금만 기다려 주세요!")
                  }
                  className="mt-3 w-full rounded-xl bg-ink px-6 py-3.5 text-sm font-bold text-white transition-colors hover:bg-black active:opacity-80"
                >
                  전체 리포트 잠금 해제 · ₩4,900
                </button>
                <p className="mt-2 text-[11px] text-sub">
                  1회 결제 · 평생 열람
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Toast message={message} />
    </section>
  );
}
