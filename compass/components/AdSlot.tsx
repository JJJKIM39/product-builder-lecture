/**
 * 광고 슬롯 플레이스홀더.
 * AdSense 승인 후 아래 주석 위치에 광고 코드를 삽입하면 된다.
 * 신뢰 원칙: 실용 진단(practical) 결과 페이지에는 이 컴포넌트를 배치하지 않는다.
 */
export default function AdSlot({ className = "" }: { className?: string }) {
  return (
    <aside className={`w-full ${className}`} aria-label="광고 영역">
      <p className="mb-1.5 text-[11px] font-medium tracking-widest text-sub">
        AD · 광고
      </p>
      <div className="flex h-28 w-full items-center justify-center rounded-xl border border-dashed border-line bg-white/50">
        {/* <ins className="adsbygoogle" ... /> 를 여기에 삽입 */}
        <span className="text-sm text-sub">광고 영역</span>
      </div>
    </aside>
  );
}
