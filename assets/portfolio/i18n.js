// English is the default; the URL is the source of truth for shared links.
(() => {
  const language = new URLSearchParams(window.location.search).get('lang') === 'ko' ? 'ko' : 'en';
  document.documentElement.lang = language;
  const korean = {
  "copy-0": "본문으로 건너뛰기",
  "copy-1": "김도현 · RESUME",
  "copy-2": "PDF로 저장 ↗",
  "copy-3": "질문하고, 탐구하는",
  "copy-4": "보안 엔지니어 ",
  "copy-5": "김도현",
  "copy-6": "문제를 정의하고, 모르는 것을 찾고,",
  "copy-7": " 알아가는 과정을 즐깁니다.",
  "copy-8": "핵심 역량",
  "copy-9": "시스템 분석 및 보안 운영",
  "copy-10": "고가용성이 요구되는 주요 국방 기반시설을 운영하며, '가용성도 보안이다'라는 관점에서 보안대책을 시스템에 안정적으로 적용하는 방법을 고민해 왔습니다. 또한 SIEM을 비롯한 다양한 엔터프라이즈 보안 솔루션을 운용하며 보안 정책 수립·적용, 탐지 규칙 및 경보 설정 등 보안 운영 전반의 실무 경험을 쌓았습니다.",
  "copy-11": "취약점 연구",
  "copy-12": "OSCP 취득, CTF 대회 수상, 오픈소스 취약점 연구를 통해 웹 해킹, 리버싱, 디지털 포렌식 등 다양한 보안 분야의 역량을 쌓았습니다. 취약점을 발견하는 데 그치지 않고 실제 공격 가능성과 영향을 검증하며, 연구 결과를 제보하고 보안 개선에 기여하고 있습니다.",
  "copy-13": "보안 자동화 설계",
  "copy-14": "Autobounty와 CodexTF를 직접 설계·개발하며 LLM 기반 보안 자동화 워크플로를 구축했습니다. '이것도 자동화할 수 있지 않을까?'라는 질문에서 출발해 반복적인 보안 업무를 분석하고, 에이전트 간 역할 분담과 검증 절차를 설계하여 자동화의 범위를 확장하고 있습니다.",
  "copy-15": "자격증",
  "copy-16": "정보보안기사",
  "copy-17": "정보처리기사",
  "copy-18": "정보처리산업기사",
  "copy-19": "수상",
  "copy-20": "CCE 공공부문 ",
  "copy-21": "3위",
  "copy-22": "공군 사이버보안 경진대회 ",
  "copy-23": "최우수상 (1위)",
  "copy-24": "화이트햇 콘테스트 간부트랙 본선 4위",
  "copy-25": "화이트햇 콘테스트 간부트랙 본선 8위",
  "copy-26": "공군 사이버전사 경연대회 ",
  "copy-27": "공군 정보통신 경연대회 해킹방어부문 ",
  "copy-28": "CCE 공공분야 본선 8위",
  "copy-29": "학력",
  "copy-30": "아주대학교",
  "copy-31": " 정보통신대학원",
  "copy-32": "사이버보안 전공 · 석사과정 재학",
  "copy-33": "독학학위제",
  "copy-34": "컴퓨터공학 · 학사 졸업",
  "copy-35": "공군항공과학고등학교",
  "copy-36": "정보통신공학과 졸업",
  "copy-37": "해외경험",
  "copy-38": "대한민국 공군 국외 병과교육 대상자로 선발되어 미국 Keesler 공군기지에서 약 18주간 Cyber Systems Operations 과정을 수료했습니다. 미군 교육생 18명과 함께 영어 기반 기술 교육과 실습에 참여하며 Network, Windows, Linux, Active Directory, Cyber Defense 등 사이버시스템 운영 분야를 학습했습니다.",
  "copy-39": "현지 홈스테이를 통해 미국의 생활과 문화를 경험했으며, 미 공군과 대한민국 공군의 교육체계를 비교·분석하여 국내 교육과정 및 구조 개선에 관한 귀국 보고서를 작성했습니다.",
  "copy-40": "개인 프로젝트",
  "copy-41": "업무 프로젝트",
  "copy-42": "배움의 태도",
  "copy-43": "기술을 배우는 마음으로, 사람과 세상도 이해하고 싶습니다.",
  "copy-44": "저의 호기심은 코드 안에만 머무르지 않습니다. 문제가 생기면 무엇을 모르는지부터 찾고, 질문을 따라가며 이해의 범위를 넓힙니다.",
  "copy-45": "인간관계와 철학을 공부하는 일도 좋아합니다. 사람은 어떻게 생각하고, 우리는 어떻게 함께 살아가는지. 기술을 탐구할 때처럼 삶에서도 당연하게 여겼던 것에 질문을 던지고 싶습니다.",
  "copy-46": "요즘 공부하는 것",
  "copy-47": "최근 정보관리기술사를 준비하며 공부한 내용을 기록하고 있습니다.",
  "copy-48": "기술사 공부 기록",
  "copy-49": "기술을 넘어 배움의 의미와 인간에 대해 고민하며 기록한 글입니다.",
  "copy-50": "AI 시대에도 계속 공부해야 하는 이유",
  "copy-51": "오늘 하루는 몇 점이었나요",
  "copy-52": "김도현 · 계속 묻고, 배우고, 연결합니다.",
  "copy-53": "맨 위로 ↑",
  "attr-0": "김도현 — 개인 프로젝트와 보안 연구를 중심으로 기록한 보안 엔지니어의 이력서.",
  "attr-1": "프로필 링크",
  "attr-2": "김도현 프로필 사진",
  "attr-3": "go-jose CVE-2026-116586 보안 권고문",
  "attr-4": "go-jose 업스트림 보안 패치 PR",
  "attr-5": "MediaMTX GHSA 보안 권고문",
  "attr-6": "jwx GHSA 보안 권고문",
  "attr-7": "neko GHSA 보안 권고문",
  "attr-8": "dufs 보안 수정 커밋"
};
  if (language === 'ko') {
    document.title = '김도현 | 보안 엔지니어';
    document.querySelectorAll('[data-i18n]').forEach(element => {
      element.textContent = korean[element.getAttribute('data-i18n')];
    });
    ['content', 'alt', 'aria-label'].forEach(attribute => {
      document.querySelectorAll(`[data-i18n-${attribute}]`).forEach(element => {
        element.setAttribute(attribute, korean[element.getAttribute(`data-i18n-${attribute}`)]);
      });
    });
  }
  document.querySelectorAll('[data-language]').forEach(link => {
    const url = new URL(window.location.href);
    url.searchParams.set('lang', link.dataset.language);
    link.href = url.pathname + url.search + url.hash;
    if (link.dataset.language === language) link.setAttribute('aria-current', 'page');
  });
  window.portfolioLanguage = language;
})();
