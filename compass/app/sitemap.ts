import type { MetadataRoute } from "next";
import { quizzes } from "@/data/quizzes";
import { SITE_URL } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticPages: MetadataRoute.Sitemap = [
    { url: SITE_URL, changeFrequency: "weekly", priority: 1 },
    { url: `${SITE_URL}/about`, changeFrequency: "monthly", priority: 0.5 },
  ];

  const quizPages: MetadataRoute.Sitemap = quizzes.map((quiz) => ({
    url: `${SITE_URL}/quiz/${quiz.slug}`,
    changeFrequency: "monthly",
    priority: 0.9,
  }));

  const resultPages: MetadataRoute.Sitemap = quizzes.flatMap((quiz) =>
    Object.keys(quiz.results).map((type) => ({
      url: `${SITE_URL}/quiz/${quiz.slug}/result/${type}`,
      changeFrequency: "monthly" as const,
      priority: 0.6,
    }))
  );

  return [...staticPages, ...quizPages, ...resultPages];
}
