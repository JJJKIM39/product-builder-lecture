/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: { ignoreDuringBuilds: true },
  // GitHub Pages는 정적 파일만 서빙하므로 완전 정적 export로 빌드한다.
  output: "export",
  trailingSlash: true,
};

export default nextConfig;
