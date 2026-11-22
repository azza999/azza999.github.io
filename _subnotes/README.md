# 서브노트

공개 읽기 전용 페이지: https://azza999.github.io/subnotes/

내용은 `_subnotes/notes/<고유한-영문-이름>.md`에서 관리한다. 웹 편집기나 로그인은 없다. 사용자가 대화로 수정 사항을 전달하면 에이전트가 Markdown을 수정하고 커밋·배포한다. 기존 학습 점수는 별도로 관리한다.

## 기록 추가·수정

- `template.md`를 `notes/`로 복사하고 고유한 영문 파일명을 사용한다. 기존 파일명은 공개 주소이므로 유지한다.
- 메타데이터는 `title`, `category`, `updated`(한국시간 실제 수정일), `summary`를 각각 한 줄로 작성한다. 따옴표로 감싸지 않는다.
- 본문은 `##`부터 시작한다. 표·목록·링크·이미지·코드 블록을 지원하며 목차는 자동 생성된다.
- 기존 내용·출처·정정 이력을 보존한다. 근거가 없는 학습 완료나 평가 점수를 만들지 않는다.
- 공개 페이지에 로그인 정보나 비공개 교재 원문을 올리지 않는다. 학습 내용은 본인의 요약으로 기록하고 출처 링크를 붙인다.
- 이미지 등은 `assets/subnotes/`에 저장하고 `/assets/subnotes/example.png` 같은 사이트 절대 경로로 연결한다.
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
