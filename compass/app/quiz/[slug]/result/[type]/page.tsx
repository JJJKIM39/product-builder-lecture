import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import AdSlot from "@/components/AdSlot";
import PremiumCta from "@/components/PremiumCta";
import ResultDial from "@/components/ResultDial";
import SaveResult from "@/components/SaveResult";
import ShareButton from "@/components/ShareButton";
import { getQuiz, quizzes } from "@/data/quizzes";

interface Props {
  params: { slug: string; type: string };
}

export function generateStaticParams() {
  return quizzes.flatMap((quiz) =>
    Object.keys(quiz.results).map((type) => ({ slug: quiz.slug, type }))
  );
}

export function generateMetadata({ params }: Props): Metadata {
  const quiz = getQuiz(params.slug);
  const result = quiz?.results[params.type];
  if (!quiz || !result) return {};
  const title = `${result.name} — ${quiz.title} 결과`;
  const description = result.tagline;
  return {
    title,
    description,
    openGraph: { title, description },
    twitter: { card: "summary_large_image", title, description },
  };
}

function CheckIcon({ color }: { color: string }) {
  return (
    <svg
      className="mt-0.5 h-4 w-4 shrink-0"
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden="true"
    >
      <circle cx="10" cy="10" r="9" stroke={color} strokeWidth="1.5" />
      <path
        d="M6 10.5l2.5 2.5L14 7.5"
        stroke={color}
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function CautionIcon() {
  return (
    <svg
      className="mt-0.5 h-4 w-4 shrink-0"
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M10 3L18 16.5H2L10 3z"
        stroke="#B08A3E"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      <path d="M10 8.5v3.5" stroke="#B08A3E" strokeWidth="1.8" strokeLinecap="round" />
      <circle cx="10" cy="14.2" r="0.9" fill="#B08A3E" />
    </svg>
  );
}

export default function ResultPage({ params }: Props) {
  const quiz = getQuiz(params.slug);
  const result = quiz?.results[params.type];
  if (!quiz || !result) notFound();

  const isPractical = quiz.category === "practical";
  const paragraphs = result.desc.split("\n\n");

  return (
    <div className="mx-auto max-w-[560px] px-5 py-12">
      <SaveResult slug={quiz.slug} type={params.type} />

      <p className="text-center text-sm font-medium text-sub">{quiz.title}</p>

      <div className="mt-6">
        <ResultDial
          color={result.color}
          label={result.name}
          sublabel="나의 유형"
        />
      </div>

      {/* 한 줄 요약 */}
      <p className="mt-6 text-center font-serif text-lg font-bold leading-snug text-ink">
        “{result.tagline}”
      </p>

      {/* 상세 해설 — 문단 구분 유지 */}
      <section className="mt-6 rounded-2xl border border-line bg-card p-6">
        {paragraphs.map((p, i) => (
          <p
            key={i}
            className={`text-[15px] leading-relaxed text-ink/85 ${i > 0 ? "mt-4" : ""}`}
          >
            {p}
          </p>
        ))}
      </section>

      {/* 강점 */}
      <section className="mt-4 rounded-2xl border border-line bg-card p-6">
        <h2 className="mb-3 text-sm font-bold" style={{ color: result.color }}>
          이런 점이 강해요
        </h2>
        <ul className="space-y-2.5">
          {result.strengths.map((s, i) => (
            <li key={i} className="flex gap-2.5 text-[14px] leading-relaxed text-ink/85">
              <CheckIcon color={result.color} />
              <span>{s}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* 주의할 점 */}
      <section className="mt-4 rounded-2xl border border-line bg-card p-6">
        <h2 className="mb-3 text-sm font-bold text-[#B08A3E]">
          이건 조심하세요
        </h2>
        <ul className="space-y-2.5">
          {result.cautions.map((c, i) => (
            <li key={i} className="flex gap-2.5 text-[14px] leading-relaxed text-ink/85">
              <CautionIcon />
              <span>{c}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* 어울리는 환경·스타일 */}
      <section
        className="mt-4 rounded-2xl border bg-card p-6"
        style={{ borderColor: `${result.color}44` }}
      >
        <h2 className="mb-2 text-sm font-bold text-ink">
          {isPractical ? "잘 맞는 투자 방식" : "잘 맞는 환경"}
        </h2>
        <p className="text-[15px] leading-relaxed text-ink/85">{result.fit}</p>
      </section>

      {/* 성장 포인트 — 인용구 스타일 */}
      <blockquote
        className="mt-6 rounded-r-2xl border-l-4 bg-white/60 py-4 pl-5 pr-4"
        style={{ borderLeftColor: result.color }}
      >
        <p className="font-serif text-[15px] font-semibold leading-relaxed text-ink">
          {result.growthTip}
        </p>
      </blockquote>

      {/* 공유 & 다시하기 */}
      <div className="mt-8 flex flex-col gap-3">
        <ShareButton
          title={`${quiz.title} — 나는 ${result.name}`}
          text={`나의 ${quiz.title} 결과는 "${result.name}". 당신의 유형도 확인해 보세요.`}
          accent={isPractical ? "#7A9B7E" : "#2B3CF3"}
        />
        <Link
          href={`/quiz/${quiz.slug}`}
          className="w-full rounded-xl border border-line bg-card px-6 py-3.5 text-center text-base font-semibold text-ink transition-shadow hover:shadow-md"
        >
          다시 검사하기
        </Link>
      </div>

      {/* 수익화 영역 — 캐주얼은 광고, 실용 진단은 프리미엄 CTA (광고 금지) */}
      <div className="mt-10">
        {isPractical ? (
          <PremiumCta />
        ) : (
          <div className="border-t border-line pt-8">
            <AdSlot />
          </div>
        )}
      </div>

      <p className="mt-10 text-center">
        <Link
          href="/"
          className="text-sm font-medium text-sub transition-colors hover:text-ink"
        >
          다른 검사도 해보기 →
        </Link>
      </p>

      {/* 면책 문구 */}
      {quiz.disclaimer && (
        <p className="mt-8 text-center text-xs leading-relaxed text-sub/80">
          {quiz.disclaimer}
        </p>
      )}
    </div>
  );
}
