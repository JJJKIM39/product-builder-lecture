import type { Metadata } from "next";
import { Instrument_Serif } from "next/font/google";
import Link from "next/link";
import { SITE_NAME, SITE_URL } from "@/lib/site";
import "./globals.css";

// 영문 로고타입·진행 표시 숫자용
const instrument = Instrument_Serif({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-instrument",
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${SITE_NAME} — 무료 성격검사·투자성향테스트`,
    template: `%s | ${SITE_NAME}`,
  },
  description:
    "나침반은 성격검사, 투자성향테스트 등 자기이해를 돕는 무료 심리테스트를 제공합니다. 내 방향을 아는 것이 다음 선택을 쉽게 만듭니다.",
  keywords: [
    "성격검사",
    "무료 심리테스트",
    "투자성향테스트",
    "자기이해",
    "성향 진단",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko" className={instrument.variable}>
      <body className="font-sans">
        <header className="sticky top-0 z-10 border-b border-line bg-ivory/80 backdrop-blur">
          <div className="mx-auto flex h-[60px] max-w-[720px] items-center justify-between px-5">
            <Link href="/" className="flex items-center gap-2">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/icon.svg" alt="" width={22} height={22} />
              <span className="flex items-baseline gap-1.5">
                <span className="font-serif text-lg font-bold text-ink">
                  나침반
                </span>
                <span className="font-instrument text-sm tracking-wide text-sub">
                  COMPASS
                </span>
              </span>
            </Link>
            <nav className="flex items-center gap-6 text-sm text-sub">
              <Link
                href="/"
                className="transition-colors duration-200 hover:text-ink"
              >
                검사
              </Link>
              <Link
                href="/about"
                className="transition-colors duration-200 hover:text-ink"
              >
                소개
              </Link>
            </nav>
          </div>
        </header>
        <main className="min-h-[calc(100vh-60px)]">{children}</main>
        <footer className="border-t border-line py-8">
          <div className="mx-auto max-w-[720px] px-5 text-xs leading-relaxed text-sub">
            <p className="font-serif font-semibold text-ink/60">
              나침반 Compass
            </p>
            <p className="mt-1">
              모든 검사 결과는 자기이해를 돕기 위한 참고 자료이며, 전문적인
              심리·투자 상담을 대신하지 않습니다.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
