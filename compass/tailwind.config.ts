import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./data/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ivory: "#FAFAF8",
        card: "#FFFFFF",
        line: "#E8E6E1",
        ink: "#171717",
        cobalt: { DEFAULT: "#2B3CF3", dark: "#1F2CC7" },
        sage: "#7A9B7E",
        sub: "#6F6E69",
      },
      fontFamily: {
        serif: ["MaruBuri", "serif"],
        sans: [
          "Pretendard Variable",
          "Pretendard",
          "-apple-system",
          "BlinkMacSystemFont",
          "system-ui",
          "Apple SD Gothic Neo",
          "sans-serif",
        ],
        instrument: ["var(--font-instrument)", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};

export default config;
