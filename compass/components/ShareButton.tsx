"use client";

import { Toast, useToast } from "./Toast";

export default function ShareButton({
  title,
  text,
  accent,
}: {
  title: string;
  text: string;
  accent: string;
}) {
  const { message, show } = useToast();

  async function handleShare() {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title, text, url });
      } catch {
        // 사용자가 공유 시트를 닫은 경우 — 아무것도 하지 않는다
      }
      return;
    }
    try {
      await navigator.clipboard.writeText(url);
      show("링크가 복사되었습니다");
    } catch {
      show("복사에 실패했어요. 주소창의 URL을 이용해 주세요");
    }
  }

  return (
    <>
      <button
        onClick={handleShare}
        className="w-full rounded-xl px-6 py-3.5 text-base font-semibold text-white transition-opacity hover:opacity-90 active:opacity-80"
        style={{ backgroundColor: accent }}
      >
        결과 공유하기
      </button>
      <Toast message={message} />
    </>
  );
}
