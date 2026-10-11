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
    { title: 'MCRC 성능개량사업', category: 'work', kind: 'PROJECT', summary: '고가용성 C2 체계 운용시험평가 및 초기 정보보호체계 구축', description: '약 1,800억 원 규모의 성능개량사업에서 2025년 1~5월 운용시험평가관 및 보안 실무자로 참여했습니다. 소프트웨어·기반통신의 요구사항 충족 여부와 성능·안정성·운용 적합성을 검증하고, 수백 개 보안대책의 적용 범위와 시스템 영향을 정리해 단계별 점검 및 조치계획을 조율했습니다. 방위사업청·체계 개발업체·유관 부대와 협업하며 실시간 감시 주기 등 운용 요구사항을 기술적 근거에 따라 구체화했습니다.', result: '2025.01–05 · 운용시험평가 · 보안측정 대응 및 초기 보안체계 구축 · 감시 주기 1분 요구사항 조율', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' },
    { title: '497.1일 이후 발생한 HP-UX 장애', category: 'essay', kind: 'TROUBLESHOOTING', summary: '장기 가동 서버의 MPT/SCSI 드라이버 타이머 문제 추적', description: 'HP-UX 서버에서 장기간 무재부팅 상태 이후 MPT/SCSI 오류와 시스템 로그 급증 현상을 분석했습니다. 동일한 서버 3대의 재부팅 이력과 로그를 비교해 최근 재부팅한 서버만 정상이라는 차이를 확인했고, 약 497.1일 경과 시 발생하는 32비트 타이머 오버플로 문제와 증상이 부합함을 관련 드라이버 문서로 검토했습니다.', result: 'HP-UX · MPT/SCSI · syslog 분석 · 재부팅 이력 비교 · 497.1일 타이머 오버플로 추적', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' },
    { title: '이중화에 관한 고찰', category: 'essay', kind: 'TROUBLESHOOTING', summary: 'HSRP와 vSphere 복구 정책이 맞물린 이중화 장애 분석', description: '백본 스위치 한 대를 중단했을 때는 정상적으로 절체됐지만, 원래 백본을 복구한 직후 체계 전체에 통신 장애가 발생했습니다. HSRP Preempt와 vSphere Failback이 동시에 작용하는 상황에서 MAC 갱신·RARP·STP 등 네트워크 수렴 과정의 영향을 원인 가설로 분석했습니다. vSphere의 자동 Failback을 비활성화한 이후 같은 장애가 재발하지 않았으며, 이중화 설계에서는 장애 시 절체뿐 아니라 복구 시 동작도 검증해야 한다는 점을 확인했습니다.', result: 'HSRP · vSphere · Failover/Failback · 복구 구간 장애 분석 · 설정 변경 후 재발 미관찰', problem: '', approach: '', contribution: '', learning: '', url: '', image: '', imageAlt: '' }
  ]
};
