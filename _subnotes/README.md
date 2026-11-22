# 서브노트

공개 읽기 전용 페이지: https://azza999.github.io/subnotes/

내용은 `_subnotes/notes/<고유한-영문-이름>.md`에서 관리한다. 웹 편집기나 로그인은 없다. 사용자가 대화로 수정 사항을 전달하면 에이전트가 Markdown을 수정하고 커밋·배포한다. 기존 학습 점수는 별도로 관리한다.

## 기록 추가·수정

- `template.md`를 `notes/`로 복사하고 고유한 영문 파일명을 사용한다. 기존 파일명은 공개 주소이므로 유지한다.
- 메타데이터는 `title`, `category`, `updated`(한국시간 실제 수정일), `summary`를 각각 한 줄로 작성한다. 따옴표로 감싸지 않는다.
- 본문은 `##`부터 시작한다. 표·목록·링크·이미지·코드 블록을 지원하며 목차는 자동 생성된다.
- 151기 확정 숙제는 `curriculum.json`의 번호·원래 주제·영문 경로와 각 노트의 `homework_order`로 연결된다. 빌드는 32개가 중복·누락 없이 일치하는지 확인한다. 숙제 여부와 수업의 출제·암기 강조는 구분한다.
- 셀프테스트 추가 주제는 `selftest.json`의 `extra_topics`와 각 노트의 `selftest_order`로 연결한다. `questions`에는 기본 50·심화 7·2교시형 6문항의 요약과 연결 노트를 관리한다. 범위 필터와 `/subnotes/selftest/` 연결표는 빌드가 생성한다. 확정 숙제 32개와 추가 주제의 번호·집합을 구분하고, 각 문항의 모든 세부 요구가 해당 노트에 설명되어 있는지 확인한다.
- 읽기 구조는 쉬운 설명 → 정의·회상 단서 → 도식·표 → 가리고 설명하기 → 상황 적용 → 혼동 교정 → 출처다. 실제 이해 확인 없이 학습 완료를 표시하지 않는다.
- 회상·적용 해설은 `<details class="answer" markdown="1"><summary>…</summary><div markdown="1">…</div></details>`로 접는다. 인쇄/PDF에서는 해설을 펼치고 종료 후 원래 상태로 되돌린다.
- 기존 내용·출처·정정 이력을 보존한다. 근거가 없는 학습 완료나 평가 점수를 만들지 않는다.
- 공개 페이지에 로그인 정보나 비공개 교재 원문을 올리지 않는다. 학습 내용은 본인의 요약으로 기록하고 출처 링크를 붙인다.
- 이미지 등은 `assets/subnotes/`에 저장하고 `/assets/subnotes/example.png` 같은 사이트 절대 경로로 연결한다.
- **모든 노트에 개념도는 필수다.** 현재 숙제 32개·셀프테스트 추가 27개·가이드 2개 모두 출처를 검토한 SVG를 포함한다. 카페·ITPE 지식관리의 관계도·표·설명을 확인하고, 손으로 재현할 수 있도록 핵심 구조를 직접 재구성한다. 원본 이미지를 사용한 것처럼 표기하지 않는다. 지식관리 본문·도식이 비어 있거나 다른 개념의 그림이면, 그 한계를 밝히고 공식 1차자료를 근거로 직접 구성한다.
- 개념도는 `_subnotes/draw_diagrams.py`에서 관리한다. 수정 후 `python3 _subnotes/draw_diagrams.py`로 `assets/subnotes/concepts/*.svg`와 `_subnotes/diagrams.json`을 재생성한다. 셀프테스트 추가 그림은 `extra_diagrams.json`의 출처·설명과 `draw_extra_diagrams.py`의 구조를 함께 관리한다. 생성기는 표준 라이브러리만 사용한다. 출처의 `image_number`는 해당 지식관리 페이지의 서브노트 이미지에서 1부터 센 번호이며, 설명만 참고한 경우 비워 둔다.
- 각 Markdown의 `diagram` 메타데이터·로컬 그림·대체 텍스트·읽는 법·손그림 순서·참고 링크·확인일을 함께 유지한다. `diagrams.json`의 설명과 노트 본문도 함께 수정한다. 빌드는 개념도 누락·잘못된 경로·SVG 접근성 설명 누락을 거부한다.
- 포함관계·흐름·시간축·비교행렬 등 주제에 맞는 구조를 선택한다. PDCA를 모든 개념의 실제 절차로 바꾸지 않는다. RPO는 장애 전 데이터 손실 구간의 목표, RTO는 장애 후 복구 소요시간의 목표로 구분한다. 수업상 LISS·AX 2.0은 수학 정의·보편 표준과 구분한다.
- `subnotes/`는 생성물이다. 직접 수정하지 않는다. `web/`이 UI 원본이다.
- 전용 `.github/workflows/subnotes.yml`이 Markdown 설치·빌드 및 전체 사이트의 Pages 게시를 처리한다. 학습 점수 대시보드의 데이터 재계산과 독립적으로 실행된다. 커밋 전 로컬 빌드를 실행해 `subnotes/` 생성물도 함께 커밋한다.

## 로컬 확인

```sh
python3 -m venv /tmp/subnotes-venv
/tmp/subnotes-venv/bin/pip install -r _subnotes/requirements.txt
/tmp/subnotes-venv/bin/python _subnotes/build.py
python3 -m http.server 8000
```

http://localhost:8000/subnotes/ 에서 목록·검색·도메인 선택·상세 목차·모바일·인쇄를 확인한다. JavaScript가 꺼져 있어도 목록과 본문을 읽을 수 있다. Markdown은 저장소 작성자를 신뢰하여 HTML을 허용하므로 외부 입력을 자동 수집하지 않는다.
