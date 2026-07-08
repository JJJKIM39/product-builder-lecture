import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "소개",
  description:
    "나침반 Compass는 성격검사·투자성향테스트 등 자기이해를 돕는 검사를 제공하는 서비스입니다.",
};

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-[720px] px-5 py-14">
      <h1 className="font-serif text-2xl font-bold leading-snug text-ink">
        방향을 아는 사람은
        <br />
        헤매는 시간이 짧습니다.
      </h1>
      <div className="mt-8 space-y-6 text-[15px] leading-relaxed text-ink/80">
        <p>
          나침반은 자기이해를 돕는 검사 플랫폼입니다. 재미로 해보는 가벼운
          심리테스트부터, 투자·커리어 같은 실제 결정에 쓰이는 실용 진단까지 —
          모든 검사는 &ldquo;나를 조금 더 정확히 아는 것&rdquo;이라는 하나의
          목적을 향합니다.
        </p>
        <p>
          결과는 사람을 상자에 가두는 낙인이 아니라, 다음 선택의 출발점이라고
          믿습니다. 그래서 나침반의 결과 페이지는 &ldquo;당신은 이런
          사람입니다&rdquo;에서 멈추지 않고, &ldquo;그렇다면 이렇게 해보면
          어떨까요&rdquo;까지 이야기합니다.
        </p>
        <div className="rounded-2xl border border-line bg-card p-6">
          <h2 className="font-serif text-base font-bold text-ink">
            나침반의 원칙
          </h2>
          <ul className="mt-3 space-y-2 text-sm text-ink/80">
            <li>
              <strong className="text-ink">광고와 콘텐츠의 분리.</strong> 가벼운
              검사에는 광고가 붙지만, 실제 결정을 다루는 실용 진단 결과에는
              광고를 싣지 않습니다.
            </li>
            <li>
              <strong className="text-ink">과장하지 않기.</strong> 검사 결과는
              참고 자료이며, 전문 상담을 대신하지 않는다는 것을 분명히 합니다.
            </li>
            <li>
              <strong className="text-ink">가입 없이 바로.</strong> 검사에
              로그인은 필요하지 않습니다.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
