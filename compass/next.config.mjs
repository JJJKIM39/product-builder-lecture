/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: { ignoreDuringBuilds: true },
  // 정적 호스팅(Cloudflare Workers assets)용 완전 정적 export.
  output: "export",
  trailingSlash: true,
  // dev 서버가 떠 있는 상태에서 build가 .next를 덮어써 깨뜨리지 않도록
  // 필요 시 NEXT_DIST_DIR로 빌드 산출물 경로를 분리할 수 있다.
  distDir: process.env.NEXT_DIST_DIR || ".next",
};

export default nextConfig;
