import { ImageResponse } from "next/og";
import { getQuiz, quizzes } from "@/data/quizzes";

export const runtime = "nodejs";
export const alt = "나침반 Compass 검사 결과";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export function generateStaticParams() {
  return quizzes.flatMap((quiz) =>
    Object.keys(quiz.results).map((type) => ({ slug: quiz.slug, type }))
  );
}

/** 마루 부리 Bold (네이버 공식 CDN). 실패 시 Google Fonts 세리프 서브셋으로 폴백. */
async function loadKoreanFont(text: string): Promise<ArrayBuffer | null> {
  try {
    const res = await fetch(
      "https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.ttf"
    );
    if (res.ok) return await res.arrayBuffer();
  } catch {
    // 아래 폴백으로 진행
  }
  try {
    const cssUrl = `https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@700&text=${encodeURIComponent(text)}`;
    const css = await fetch(cssUrl).then((r) => r.text());
    const match = css.match(/src:\s*url\((.+?)\)\s*format\('(?:opentype|truetype)'\)/);
    if (!match) return null;
    return await fetch(match[1]).then((r) => r.arrayBuffer());
  } catch {
    return null;
  }
}

export default async function OgImage({
  params,
}: {
  params: { slug: string; type: string };
}) {
  const quiz = getQuiz(params.slug);
  const result = quiz?.results[params.type];

  const title = quiz?.title ?? "나침반";
  const name = result?.name ?? "자기이해 검사";
  const color = result?.color ?? "#171717";

  const textForSubset = `${title}${name}나침반 COMPASS 검사 결과나의 유형`;
  const fontData = await loadKoreanFont(textForSubset);

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          backgroundColor: "#FAFAF8",
          padding: "0 80px",
          fontFamily: "MaruBuri, serif",
        }}
      >
        {/* 결과 다이얼 링 */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: 340,
            height: 340,
            borderRadius: 999,
            border: `26px solid ${color}`,
            backgroundColor: "#FFFFFF",
            flexShrink: 0,
          }}
        >
          <div
            style={{
              display: "flex",
              fontSize: 44,
              fontWeight: 700,
              color,
              textAlign: "center",
              padding: "0 26px",
              lineHeight: 1.35,
              wordBreak: "keep-all",
            }}
          >
            {name}
          </div>
        </div>

        {/* 텍스트 영역 */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            marginLeft: 72,
          }}
        >
          <div style={{ display: "flex", fontSize: 26, color: "#6F6E69" }}>
            나침반 COMPASS
          </div>
          <div
            style={{
              display: "flex",
              fontSize: 40,
              color: "#171717",
              marginTop: 18,
            }}
          >
            {title} 결과
          </div>
          <div
            style={{
              display: "flex",
              fontSize: 76,
              fontWeight: 700,
              color: "#171717",
              marginTop: 10,
            }}
          >
            {name}
          </div>
          <div
            style={{
              display: "flex",
              width: 140,
              height: 10,
              backgroundColor: color,
              borderRadius: 5,
              marginTop: 34,
            }}
          />
        </div>
      </div>
    ),
    {
      ...size,
      fonts: fontData
        ? [
            {
              name: "MaruBuri",
              data: fontData,
              weight: 700 as const,
              style: "normal" as const,
            },
          ]
        : undefined,
    }
  );
}
