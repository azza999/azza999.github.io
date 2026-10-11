// 이 파일을 수정하면 페이지에 반영됩니다. 주소를 넣기 전에는 링크가 표시되지 않습니다.
window.portfolio = {
  name: '김도현', // 예: 김도현 (비워두면 이름을 표시하지 않습니다)
  blog: 'https://blog.naver.com/azza999/', // 네이버 블로그의 전체 https:// 주소
  github: '', // GitHub 프로필의 전체 https:// 주소
  email: '',
  techBlog: 'https://velog.io/@azzadh999/posts',
  // image: 저장소의 이미지 경로 (예: assets/portfolio/images/autobounty.webp)
  // imageAlt: 이미지가 전달하는 내용을 설명하는 문장
  projects: [
    { title: 'Autobounty', category: 'personal', kind: 'PROJECT', summary: 'LLM 기반 오픈소스 취약점 자동 분석 프레임워크', description: '오픈소스 리포지토리의 탐색부터 취약점 분석, 독립 검증, 보고서 작성까지 수행하는 자동화 프레임워크를 개발했습니다. 초기에는 단순한 취약점 발견에 집중했으나, 실제 사용 환경에서의 발현 가능성, Downstream 영향 분석, 취약점 체이닝까지 검증하도록 발전시켰습니다.', result: '22회 점검 · 외부 보고서 10건 · GHSA 공개 2건', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' },
    { title: 'CodexTF', category: 'personal', kind: 'PROJECT', summary: '가설 기반 멀티에이전트 CTF 풀이 프레임워크', description: '단일 LLM 에이전트의 추론 정체와 병렬 실행 시 중복 탐색 문제를 개선하기 위해 가설 기반 문제 분해와 역할별 에이전트 협업 구조를 설계했습니다. 개별 가설 검증과 전체 공격 체인의 재현을 구분하고, 작업 간 상태 연속성을 검증하도록 발전시켰습니다.', result: '2026 CCE Jeopardy 13문제 중 9문제 풀이', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' },
    { title: 'CCE 2026 SpeedHack Solver', category: 'personal', kind: 'PROJECT', summary: '제한 시간 CTF를 위한 실시간 문제 풀이 자동화 파이프라인', description: '약 15분 주기로 공개되는 문제의 수집, LLM 풀이, 플래그 제출 과정을 자동화했습니다. 문제 수집 지연과 불필요한 판단 단계를 줄이도록 워크플로를 최적화하며 대회 진행 중에도 지속적으로 성능을 개선했습니다.', result: '최초 정답 15회 · SpeedHack 50팀 중 3위 · 후반 11라운드 평균 풀이 시간 1분 58초', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' },
    { title: 'MCRC 성능개량사업', category: 'work', kind: 'PROJECT', summary: '', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' },
    { title: '이중화에 관한 고찰', category: 'essay', kind: 'TECHNICAL ESSAY', summary: '', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' }
  ]
};
