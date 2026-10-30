---
id: ci-cd
title: CI/CD (Continuous Integration / Delivery / Deployment)
category: 소프트웨어 공학
score: 60
max_score: 100
studied_at: 2026-10-19
reviews: [{"date":"2026-10-26","score":15},{"date":"2026-10-27","score":10}]
---
## 핵심 개념
- CI(Continuous Integration, 지속적 통합): 개발자가 변경한 코드를 자주 공유 저장소에 통합하고 빌드·자동화 테스트로 변경을 검증하는 개발 실천.
- Continuous Delivery(지속적 제공): 검증된 변경 사항을 언제든 운영환경에 배포 가능한 상태로 유지하는 방식. 운영 배포는 수동 승인할 수 있음.
- Continuous Deployment(지속적 배포): 검증을 통과한 변경 사항을 별도 수동 승인 없이 운영환경에 자동 배포하는 방식.

## CI/CD 파이프라인
1. 코드 변경·커밋
2. 빌드 및 단위·통합 테스트(CI)
3. 산출물 패키징 및 배포 준비(Delivery)
4. 승인 기반 수동 배포(Delivery) 또는 자동 운영 배포(Deployment)
5. 배포 후 모니터링·피드백

## 주요 비교
| 구분 | CI | Continuous Delivery | Continuous Deployment |
|---|---|---|---|
| 목적 | 코드 통합 및 품질 검증 | 배포 가능한 상태 유지 | 운영환경까지 자동 배포 |
| 자동화 범위 | 빌드·테스트 | 배포 준비까지 | 실제 운영 배포까지 |
| 운영 배포 승인 | 해당 없음 | 수동 승인 가능 | 별도 수동 승인 없음 |

## 답안 구조
1. CI/CD 개념
2. CI/CD 파이프라인
3. Delivery와 Deployment의 차이

## 학습 기록
- 2026-10-19 학습: CI/CD 개념과 파이프라인 도식 학습.
- 2026-10-20 기록 요청에 따라 자기 지정 숙련도 60/100 반영. 별도 독립 답안 채점은 수행하지 않음.
