/**
 * 나침반의 시그니처 비주얼 — 결과 컬러로 채워지는 원형 게이지.
 * 서버 컴포넌트. 애니메이션은 globals.css의 dial-fill 키프레임 사용.
 */
export default function ResultDial({
  color,
  label,
  sublabel,
}: {
  color: string;
  label: string;
  sublabel?: string;
}) {
  const size = 240;
  const stroke = 16;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;

  return (
    <div className="relative mx-auto" style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        role="img"
        aria-label={`${label} 결과 다이얼`}
      >
        {/* 트랙 */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="#EFEAE0"
          strokeWidth={stroke}
        />
        {/* 채움 아크 */}
        <circle
          className="dial-arc"
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          style={
            {
              "--dial-circumference": `${c}px`,
              "--dial-offset": "0px",
            } as React.CSSProperties
          }
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
        {sublabel && (
          <span className="mb-1 text-xs font-medium text-sub">{sublabel}</span>
        )}
        <span
          className="font-serif text-2xl font-bold leading-snug"
          style={{ color }}
        >
          {label}
        </span>
      </div>
    </div>
  );
}
