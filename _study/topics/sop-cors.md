---
id: sop-cors
title: SOP(Same-Origin Policy)와 CORS
category: 디지털 시큐리티
score: 50
max_score: 60
---
## 핵심 개념
- SOP(Same-Origin Policy)는 브라우저가 서로 다른 Origin 간의 스크립트 기반 데이터 접근을 제한하는 보안 정책이다.
- Origin은 Scheme, Host, Port의 조합으로 판단하며 세 요소가 모두 동일해야 Same-Origin으로 본다.
- SOP는 Cross-Origin 요청 자체를 전면 차단하는 정책이 아니다. 일부 요청은 전송될 수 있지만, JavaScript가 다른 Origin의 응답을 읽거나 DOM에 접근하는 행위를 제한하는 것이 핵심이다.
- CORS(Cross-Origin Resource Sharing)는 서버가 HTTP 응답 헤더를 통해 특정 Origin의 Cross-Origin 응답 접근을 허용하도록 브라우저에 알리는 메커니즘이다.

## SOP 적용 이유
- 공격자 Origin의 JavaScript가 사용자의 인증 상태를 이용해 다른 Origin에 요청을 보낼 수 있더라도, SOP는 그 응답 내용을 공격자 스크립트가 읽는 것을 제한한다.
- 이를 통해 다른 Origin의 민감 데이터가 임의의 스크립트에 노출되는 것을 방지한다.

## CORS 주요 동작
- 서버는 대표적으로 `Access-Control-Allow-Origin` 응답 헤더를 통해 허용 Origin을 명시한다.
- 서버가 요청을 정상 처리해 `200 OK`와 응답 본문을 반환하더라도 CORS 허용 헤더가 없으면, 브라우저는 JavaScript에 해당 응답을 노출하지 않는다.
- 따라서 네트워크 요청 성공 여부와 JavaScript가 응답을 읽을 수 있는지는 구분해야 한다.

## SOP와 CORS의 관계
| 구분 | SOP | CORS |
|---|---|---|
| 목적 | Cross-Origin 데이터 접근 제한 | 제한된 Cross-Origin 접근의 선택적 허용 |
| 적용 주체 | 브라우저 | 서버 정책 + 브라우저 집행 |
| 핵심 기준 | Origin 일치 여부 | 서버가 허용한 Origin 여부 |
| 대표 요소 | Scheme + Host + Port | Access-Control-Allow-Origin 등 |

## 답안 구조
1. SOP 정의와 Origin 구성요소
2. SOP 적용 목적과 동작 원리
3. CORS 정의와 주요 헤더
4. SOP와 CORS의 관계
5. 요청 전송과 응답 읽기 제한의 차이

## 평가 기록
- 2026-10-05: 50/60점
- 최초 독립 답변에서 SOP가 브라우저에서 동작하며 Fetch/XMLHttpRequest 결과의 Cross-Origin 읽기를 제한한다는 핵심을 정확히 설명함.
- Origin을 Scheme, Host(서브도메인 포함), Port로 구분한 점도 정확했음.
- SOP를 '데이터 전송/읽기 제한'으로 다소 넓게 표현하여 Cross-Origin 요청 자체가 전면 차단되는 것처럼 오해될 여지가 있어 감점.
- CORS를 SOP 제한을 선택적으로 허용하는 정책으로 설명한 관계성은 정확했으나, 서버가 HTTP 응답 헤더로 허용 정책을 명시한다는 기술적 설명이 최초 답변에서 부족했음.
- 후속 질문에서는 `Access-Control-Allow-Origin`이 없을 때 서버가 응답을 반환하더라도 브라우저가 JavaScript의 응답 접근을 차단한다는 점을 정확히 답변함.
- 다만 이 후속 답변은 평가 해설에서 핵심 구분을 이미 제시한 뒤의 확인 답변이므로 최초 독립 답변의 잠정 점수 50점을 유지함.
- 본 평가는 채팅 기반 내용 숙련도 평가이며 제한시간 내 수기 답안 작성 능력까지 검증한 것은 아님.

## 출처
- MDN Web Docs, Same-origin policy
- MDN Web Docs, Cross-Origin Resource Sharing (CORS)
