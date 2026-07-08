"use client";

import { Toast, useToast } from "./Toast";

/**
 * 실용 진단 결과 페이지 전용 프리미엄 CTA.
 * 결제 연동 전까지는 클릭 시 "준비 중" 토스트만 노출한다.
 */
export default function PremiumCta() {
  const { message, show } = useToast();

  return (
    <section className="rounded-2xl bg-ink p-6 text-white">
      <p className="text-xs font-medium tracking-wide text-white/60">
        PREMIUM REPORT
      </p>
      <h3 className="mt-2 font-serif text-xl font-bold leading-snug">
        투자 성향 상세 리포트
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-white/80">
        유형별 자산 배분 가이드, 성향에 맞는 리스크 관리 원칙, 피해야 할 투자
        패턴까지 — 12페이지 분량의 맞춤 리포트로 받아보세요.
      </p>
      <button
        onClick={() => show("결제 기능을 준비 중이에요. 조금만 기다려 주세요!")}
        className="mt-5 w-full rounded-xl border border-white/25 bg-ink px-6 py-3.5 text-base font-semibold text-white transition-colors hover:bg-black active:opacity-80"
      >
        상세 리포트 받기 · ₩4,900
      </button>
      <Toast message={message} />
    </section>
  );
}
