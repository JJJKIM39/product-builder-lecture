"use client";

import { useEffect } from "react";

export const RESULTS_STORAGE_KEY = "compass:results";

export interface StoredResult {
  type: string;
  at: string;
}

/** 결과 페이지 방문 시 localStorage에 최근 결과를 저장한다 (재방문 시 홈에 노출). */
export default function SaveResult({
  slug,
  type,
}: {
  slug: string;
  type: string;
}) {
  useEffect(() => {
    try {
      const raw = localStorage.getItem(RESULTS_STORAGE_KEY);
      const data: Record<string, StoredResult> = raw ? JSON.parse(raw) : {};
      data[slug] = { type, at: new Date().toISOString() };
      localStorage.setItem(RESULTS_STORAGE_KEY, JSON.stringify(data));
    } catch {
      // localStorage 접근 불가(시크릿 모드 등)는 조용히 무시
    }
  }, [slug, type]);

  return null;
}
