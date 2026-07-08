import type { Metadata } from "next";
import { notFound } from "next/navigation";
import QuizRunner from "@/components/QuizRunner";
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
    title: `${quiz.title} — 검사 진행`,
    // 인트로(/quiz/[slug])가 대표 페이지 — 진행 화면은 색인 제외
    robots: { index: false },
  };
}

export default function QuizStartPage({ params }: Props) {
  const quiz = getQuiz(params.slug);
  if (!quiz) notFound();

  return <QuizRunner quiz={quiz} />;
}
