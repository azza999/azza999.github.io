"""Build the read-only notebook from Markdown. Run from any directory."""
from pathlib import Path
from datetime import date
import html
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'subnotes'
WEB = ROOT / 'web'


def esc(value):
    return html.escape(str(value), quote=True)


def read_note(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError(f'{path.name}: metadata is required')
    front, body = text[4:].split('\n---\n', 1)
    meta = {}
    for line in front.splitlines():
        if line.strip() and not line.startswith('#'):
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip()
    for key in ('title', 'category', 'updated', 'summary'):
        if not meta.get(key):
            raise ValueError(f'{path.name}: missing {key}')
    date.fromisoformat(meta['updated'])
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', path.stem):
        raise ValueError(f'{path.name}: use a stable lowercase English filename')
    if re.search(r'^# ', body, re.M):
        raise ValueError(f'{path.name}: title is provided by metadata; start sections at ##')
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'sane_lists'],
                           extension_configs={'toc': {'permalink': False}})
    meta.update(slug=path.stem, content=md.convert(body), toc=md.toc,
                search=' '.join((meta['title'], meta['category'], meta['summary'], body)).casefold())
    return meta


def shell(title, body, stylesheet):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="정보관리기술사 서브노트. 이해한 개념과 답안의 핵심을 기록합니다.">
<meta name="theme-color" content="#f6f8fb"><title>{esc(title)} · 서브노트</title>
<link rel="stylesheet" href="{stylesheet}"></head><body><a class="skip" href="#main">본문으로 건너뛰기</a>{body}</body></html>'''


def build():
    notes = sorted((read_note(p) for p in (ROOT / 'notes').glob('*.md')),
                   key=lambda n: (n['updated'], n['title']), reverse=True)
    OUT.mkdir(exist_ok=True)
    # Only generated note pages are removed; assets are managed separately.
    note_out = OUT / 'notes'
    if note_out.exists():
        shutil.rmtree(note_out)
    note_out.mkdir()
    for name in ('style.css', 'search.js'):
        shutil.copyfile(WEB / name, OUT / name)
    cards = ''.join(f'''<a class="note-card" href="notes/{n['slug']}/" data-category="{esc(n['category'])}" data-search="{esc(n['search'])}">
<div class="card-meta"><span>{esc(n['category'])}</span><time datetime="{esc(n['updated'])}">{esc(n['updated'])}</time></div>
<h3>{esc(n['title'])}</h3><p>{esc(n['summary'])}</p><span class="read-label">노트 읽기</span></a>''' for n in notes)
    categories = ''.join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in sorted({n['category'] for n in notes}))
    body = f'''<div class="page"><header class="topbar"><a class="brand" href="./">서브노트<span>ITPE 151기</span></a><a href="/study/">학습 기록</a></header>
<main id="main"><section class="intro"><p class="eyebrow">정보관리기술사 · 나의 지식 노트</p><h1>이해한 것을 기록하고,<br>답안으로 연결하기.</h1><p class="lead">정의, 개념도, 핵심 키워드.<br class="mobile-break"> 다시 펼쳤을 때 설명할 수 있도록 남깁니다.</p></section>
<section class="library" aria-labelledby="library-title"><div class="library-head"><h2 id="library-title">노트 모음 <span class="count">{len(notes)}</span></h2><span>최근 수정순</span></div>
<form class="filters" role="search" onsubmit="return false"><div class="search-field"><label for="search">노트 검색</label><input id="search" type="search" placeholder="토픽, 키워드, 본문 검색" autocomplete="off"></div><div class="category-field"><label for="category">도메인</label><select id="category"><option value="">전체 도메인</option>{categories}</select></div></form>
<p class="results" id="results" role="status" aria-live="polite">전체 {len(notes)}개의 노트</p><div class="note-grid">{cards}</div><div id="empty" class="empty" hidden><h3>일치하는 노트가 없습니다.</h3><p>검색어를 줄이거나 다른 도메인을 선택해보세요.</p><button type="button" id="reset">전체 노트 보기</button></div></section>
<aside class="routine"><h2>매주, 조금씩 다듬기</h2><div><p><strong>토요일</strong>수업의 핵심과 질문 표시</p><p><strong>일–월요일</strong>숙제 정리와 이해 보완</p><p><strong>수–금요일</strong>셀프테스트와 오답 반영</p></div></aside></main><footer>배운 내용을 내 언어로 쌓아갑니다.<span>내용 수정은 대화로 요청해주세요.</span></footer></div><script src="search.js" defer></script>'''
    (OUT / 'index.html').write_text(shell('노트 모음', body, 'style.css'), encoding='utf-8')
    for n in notes:
        dest = note_out / n['slug']
        dest.mkdir()
        body = f'''<div class="page reading-page"><header class="topbar"><a class="brand" href="../../">서브노트<span>ITPE 151기</span></a><nav aria-label="상단 탐색"><a href="../../">노트 목록</a><button type="button" onclick="window.print()">인쇄 / PDF</button></nav></header>
<main id="main"><header class="note-header"><p class="eyebrow">{esc(n['category'])}</p><h1>{esc(n['title'])}</h1><p class="lead">{esc(n['summary'])}</p><p class="updated">수정 <time datetime="{esc(n['updated'])}">{esc(n['updated'])}</time></p></header>
<div class="reading-layout"><aside class="contents"><details open><summary>이 노트의 목차</summary><nav aria-label="본문 목차">{n['toc']}</nav></details></aside><article class="prose">{n['content']}</article></div></main>
<footer><a href="../../">전체 노트 보기</a><span>배운 내용을 내 언어로 쌓아갑니다.</span></footer></div>'''
        (dest / 'index.html').write_text(shell(n['title'], body, '../../style.css'), encoding='utf-8')
    print(f'Built {len(notes)} notes in {OUT}')


if __name__ == '__main__':
    build()
