---
id: mcp-security
title: MCP 보안 취약점과 대응 방안
category: 정보보안
score: 60
max_score: 100
---

## 핵심 개념
- MCP(Model Context Protocol): AI 애플리케이션이 외부 도구와 데이터에 표준 방식으로 연결하는 개방형 프로토콜.
- 구조: MCP Host(내부 MCP Client) ↔ MCP Server ↔ 외부 API·DB·파일 등. Client와 Server는 JSON-RPC 2.0 메시지로 통신.
- MCP는 기본적으로 에이전트 간 통신 프로토콜(A2A)이 아닌 AI와 Tool/Data 연결 프로토콜.
- Server가 Tool 정의 및 목록을 제공하고(tools/list), Host/LLM이 사용을 조정하며 Client가 tools/call 요청을 송신.

## 보안 취약점 및 대응 방안
| 위협 | 공격 내용 | 대응 방안 | 기술 요소 |
|---|---|---|---|
| 프롬프트 인젝션 | 비신뢰 입력·Tool 출력으로 LLM의 행동 유도 | 신뢰 경계 분리, 고위험 작업 승인, 출력 검증 | Guardrail, Human-in-the-Loop |
| 인증·인가 미흡 | 사용자·서비스 신원 확인/권한 통제 부실 | 강한 사용자 인증, 토큰 범위 제한, 접근 통제 | OAuth, MFA, RBAC |
| Tool Poisoning | Tool 설명·메타데이터 내 악성 명령 삽입 | 설명 검토, 변경 감시, 배포물 무결성 검증 | 전자서명, 해시, 정적 분석 |
| 과도한 권한 | Tool이 과도한 파일·명령 실행 권한 사용 | 실행 격리, 최소 권한, 권한 분리 | Sandbox, Least Privilege |
| 정보 유출 | Tool 호출을 통한 개인정보·기밀 데이터 반출 | 데이터 최소화·필터링·출력/전송 통제 | DLP, 데이터 마스킹 |
| 악성 MCP Server | 위장 또는 비신뢰 서버 연결과 공급망 악용 | 신뢰 서버 목록, 신원 확인, 공급망 검토 | TLS 인증서 검증, Allowlist, SBOM |

## 주의할 개념
- OAuth는 인가 프레임워크이고 MFA·Passkey는 사용자 인증 강화 수단.
- 단순 해시값만으로 악의적으로 작성된 Tool 설명을 탐지할 수 없음. 서명·메타데이터 검토 필요.
- SBOM(Software Bill of Materials)은 구성요소·의존성 명세로 공급망 취약점 분석을 돕지만 서버 신원 검증 수단은 아님.
- SCA는 SBOM 등 구성요소 정보를 토대로 알려진 취약점·라이선스 위험을 분석.

## 2교시형 답안 구조
1. MCP 개요 및 아키텍처, 신뢰 경계/공격 표면
2. Host/LLM, Client/통신, Server/Tool, Backend 및 공급망별 취약점
3. 취약점별 대응 방안 및 기술 요소(위 표)
4. Zero Trust 기반 보안 강화: 서버·도구 검증 → 권한 통제 → 실행 격리 → 로깅·감시

## 학습 기록
- 2026-10-21: MCP Host/Client/Server 구조, Tool Discovery·Calling, 프롬프트 인젝션·Tool Poisoning·인증·인가·권한·정보 유출·공급망 대응 및 SBOM 학습.
- 사용자가 직접 작성한 6개 위협·대응 표를 검토·보완함. 단독 2교시형 전체 답안 작성과 시간제한 평가는 수행하지 않음.
- 사용자 지정 60/100점 반영(독립 평가점수로 간주하지 않음).
