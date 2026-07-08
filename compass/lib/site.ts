/** 배포 후 Vercel 환경변수 NEXT_PUBLIC_SITE_URL로 교체 */
export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

export const SITE_NAME = "나침반 Compass";
