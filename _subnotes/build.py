"""Build the read-only notebook from Markdown. Run from any directory."""
from pathlib import Path
from datetime import date
import html
import re
import shutil
import json
import markdown
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'subnotes'
WEB = ROOT / 'web'
DIAGRAMS = json.loads((ROOT / 'diagrams.json').read_text(encoding='utf-8'))
SELFTEST = json.loads((ROOT / 'selftest.json').read_text(encoding='utf-8'))


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
    diagram = DIAGRAMS.get(meta.get('diagram'))
    if not diagram:
        raise ValueError(f'{path.name}: a source-reviewed concept diagram is required')
    asset = diagram['asset']
    if not asset.startswith('/assets/subnotes/concepts/') or '..' in asset:
        raise ValueError(f'{path.name}: invalid diagram asset path')
    image = ROOT.parent / asset.lstrip('/')
    if not image.is_file() or asset not in body:
        raise ValueError(f'{path.name}: embed the required diagram in the Markdown body')
    svg = ET.parse(image).getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    if not svg.findtext('svg:title', namespaces=ns) or not svg.findtext('svg:desc', namespaces=ns):
        raise ValueError(f'{path.name}: SVG title and description are required')
    if not all(diagram.get(k) for k in ('alt', 'draw', 'read', 'sources', 'checked_at')):
        raise ValueError(f'{path.name}: diagram provenance and drawing guidance are required')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', path.stem):
        raise ValueError(f'{path.name}: use a stable lowercase English filename')
    if re.search(r'^# ', body, re.M):
        raise ValueError(f'{path.name}: title is provided by metadata; start sections at ##')
    order = meta.get('homework_order')
    if order:
        if not order.isdigit() or not 1 <= int(order) <= 32:
            raise ValueError(f'{path.name}: invalid homework_order')
        meta['homework_order'] = int(order)
    extra_order = meta.get('selftest_order')
    if extra_order:
        if order or not extra_order.isdigit() or int(extra_order) < 1:
            raise ValueError(f'{path.name}: invalid selftest_order or overlapping scope')
        meta['selftest_order'] = int(extra_order)
    meta['scope'] = 'homework' if order else 'selftest' if extra_order else 'guide'
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'sane_lists', 'md_in_html'],
                           extension_configs={'toc': {'permalink': False}})
    meta.update(slug=path.stem, content=md.convert(body), toc=md.toc,
                search=re.sub(r'\s+', ' ', ' '.join((meta['title'], meta['category'], meta['summary'], body))).strip().casefold())
    return meta


def scope_label(note):
    if note['scope'] == 'homework':
        return f'숙제 {note["homework_order"]:02d}'
    if note['scope'] == 'selftest':
        return f'셀테 추가 {note["selftest_order"]:02d}'
    return '학습 가이드'


def shell(title, body, stylesheet):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="정보관리기술사 서브노트. 이해한 개념과 답안의 핵심을 기록합니다.">
<meta name="theme-color" content="#f6f8fb"><title>{esc(title)} · 서브노트</title>
<link rel="stylesheet" href="{stylesheet}"></head><body><a class="skip" href="#main">본문으로 건너뛰기</a>{body}</body></html>'''


def build():
    notes = sorted((read_note(p) for p in (ROOT / 'notes').glob('*.md')),
                   key=lambda n: ({'homework': 0, 'selftest': 1, 'guide': 2}[n['scope']],
                                  n.get('homework_order', n.get('selftest_order', 99)), n['title']))
    curriculum = json.loads((ROOT / 'curriculum.json').read_text(encoding='utf-8'))
    homework = [n for n in notes if 'homework_order' in n]
    expected = {(t['number'], t['slug']) for t in curriculum['topics']}
    actual = {(n['homework_order'], n['slug']) for n in homework}
    if len(homework) != curriculum['count'] or len(actual) != len(homework) or expected != actual:
        raise ValueError('The confirmed 32-topic curriculum and note files must match exactly')
    extra_notes = [n for n in notes if n['scope'] == 'selftest']
    expected_extras = {(t['number'], t['slug']) for t in SELFTEST['extra_topics']}
    actual_extras = {(n['selftest_order'], n['slug']) for n in extra_notes}
    if len(extra_notes) != len(expected_extras) or actual_extras != expected_extras:
        raise ValueError('Self-test extra topics and note files must match exactly')
    by_slug = {n['slug']: n for n in notes}
    question_ids = set()
    for question in SELFTEST['questions']:
        if question['id'] in question_ids or not question['notes']:
            raise ValueError('Self-test question IDs must be unique and have linked notes')
        question_ids.add(question['id'])
        for slug in question['notes']:
            if slug not in by_slug:
                raise ValueError(f'{question["id"]}: missing linked note {slug}')
    for group in SELFTEST['groups']:
        if sum(q['group'] == group['id'] for q in SELFTEST['questions']) != group['count']:
            raise ValueError(f'{group["id"]}: self-test question count mismatch')
    OUT.mkdir(exist_ok=True)
    # Only generated note pages are removed; assets are managed separately.
    note_out = OUT / 'notes'
    if note_out.exists():
        shutil.rmtree(note_out)
    note_out.mkdir()
    for name in ('style.css', 'search.js', 'reading.js'):
        shutil.copyfile(WEB / name, OUT / name)
    cards = ''.join(f'''<a class="note-card" href="notes/{n['slug']}/" data-scope="{n['scope']}" data-category="{esc(n['category'])}" data-search="{esc(n['search'])}">
<div class="card-meta"><span>{scope_label(n)} · {esc(n['category'])}</span><time datetime="{esc(n['updated'])}">{esc(n['updated'])}</time></div>
<h3>{esc(n['title'])}</h3><p>{esc(n['summary'])}</p><span class="read-label">노트 읽기</span></a>''' for n in notes)
    categories = ''.join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in sorted({n['category'] for n in notes}))
    body = f'''<div class="page"><header class="topbar"><a class="brand" href="./">서브노트<span>ITPE 151기</span></a><a href="/study/">학습 기록</a></header>
<main id="main"><section class="intro"><p class="eyebrow">정보관리기술사 · 나의 지식 노트</p><h1>이해한 것을 기록하고,<br>답안으로 연결하기.</h1><p class="lead">정의, 개념도, 핵심 키워드.<br class="mobile-break"> 다시 펼쳤을 때 설명할 수 있도록 남깁니다.</p></section>
<aside class="start-here"><div><p class="eyebrow">151기 · 확정 숙제 32개 · 셀프테스트 추가 {len(extra_notes)}개</p><h2>읽고, 가리고, 설명해보세요.</h2><p>정답을 펼치기 전에 먼저 답해보세요. 다음 날 다시 설명할 수 있는지 확인합니다.</p></div><a href="notes/mastery-method/">학습 순서와 복습법</a></aside>
<section class="library" aria-labelledby="library-title"><div class="library-head"><h2 id="library-title">노트 모음 <span class="count">{len(notes)}</span></h2><a class="coverage-link" href="selftest/">셀프테스트 {len(SELFTEST['questions'])}문항 연결표</a></div>
<form class="filters" role="search" onsubmit="return false"><div class="search-field"><label for="search">노트 검색</label><input id="search" type="search" placeholder="토픽, 키워드, 본문 검색" autocomplete="off"></div><div class="scope-field"><label for="scope">학습 범위</label><select id="scope"><option value="">전체 범위</option><option value="homework">확정 숙제 32개</option><option value="selftest">셀프테스트 추가 {len(extra_notes)}개</option><option value="guide">학습 가이드</option></select></div><div class="category-field"><label for="category">도메인</label><select id="category"><option value="">전체 도메인</option>{categories}</select></div></form>
<p class="results" id="results" role="status" aria-live="polite">전체 {len(notes)}개의 노트</p><div class="note-grid">{cards}</div><div id="empty" class="empty" hidden><h3>일치하는 노트가 없습니다.</h3><p>검색어를 줄이거나 다른 도메인을 선택해보세요.</p><button type="button" id="reset">전체 노트 보기</button></div></section>
<aside class="routine"><h2>매주, 조금씩 다듬기</h2><div><p><strong>토요일</strong>수업의 핵심과 질문 표시</p><p><strong>일–월요일</strong>숙제 정리와 이해 보완</p><p><strong>수–금요일</strong>셀프테스트와 오답 반영</p></div></aside></main><footer>배운 내용을 내 언어로 쌓아갑니다.<span>내용 수정은 대화로 요청해주세요.</span></footer></div><script src="search.js" defer></script>'''
    (OUT / 'index.html').write_text(shell('노트 모음', body, 'style.css'), encoding='utf-8')
    for n in notes:
        dest = note_out / n['slug']
        dest.mkdir()
        navigation = ''
        if 'homework_order' in n:
            position = homework.index(n)
            neighbors = []
            if position:
                previous = homework[position-1]
                neighbors.append(f'<a href="../{previous["slug"]}/"><small>이전 숙제</small>{esc(previous["title"])}</a>')
            if position+1 < len(homework):
                following = homework[position+1]
                neighbors.append(f'<a href="../{following["slug"]}/"><small>다음 숙제</small>{esc(following["title"])}</a>')
            navigation = '<nav class="note-neighbors" aria-label="숙제 순서">'+''.join(neighbors)+'</nav>'
        badge = scope_label(n) + ('/32' if n['scope'] == 'homework' else '') + ' · '
        references = [q for q in SELFTEST['questions'] if n['slug'] in q['notes']]
        question_links = ' · '.join(f'<a href="../../selftest/#{q["id"]}">{esc(q["label"])}</a>' for q in references)
        question_links = f'<p class="selftest-links"><strong>셀프테스트 연결</strong> {question_links}</p>' if references else ''
        body = f'''<div class="page reading-page"><header class="topbar"><a class="brand" href="../../">서브노트<span>ITPE 151기</span></a><nav aria-label="상단 탐색"><a href="../../">노트 목록</a><button type="button" onclick="window.print()">인쇄 / PDF</button></nav></header>
<main id="main"><header class="note-header"><p class="eyebrow">{badge}{esc(n['category'])}</p><h1>{esc(n['title'])}</h1><p class="lead">{esc(n['summary'])}</p>{question_links}<p class="updated">수정 <time datetime="{esc(n['updated'])}">{esc(n['updated'])}</time></p></header>
<div class="reading-layout"><aside class="contents"><details open><summary>이 노트의 목차</summary><nav aria-label="본문 목차">{n['toc']}</nav><a class="method-link" href="../mastery-method/">학습 순서와 복습법</a></details></aside><article class="prose">{n['content']}{navigation}</article></div></main>
<footer><a href="../../">전체 노트 보기</a><span>배운 내용을 내 언어로 쌓아갑니다.</span></footer></div><script src="../../reading.js" defer></script>'''
        (dest / 'index.html').write_text(shell(n['title'], body, '../../style.css'), encoding='utf-8')
    build_selftest_page(by_slug)
    print(f'Built {len(notes)} notes in {OUT}')


def build_selftest_page(notes):
    sections = []
    for group in SELFTEST['groups']:
        rows = []
        for q in (q for q in SELFTEST['questions'] if q['group'] == group['id']):
            links = ' · '.join(f'<a href="../notes/{slug}/">{esc(notes[slug]["title"].split(" · ")[0])}</a>'
                               + (' <span class="extra-tag">추가</span>' if notes[slug]['scope'] == 'selftest' else '')
                               for slug in q['notes'])
            rows.append(f'<tr id="{q["id"]}"><th scope="row">{esc(q["label"])}</th><td>{esc(q["title"])}</td><td>{links}</td></tr>')
        sections.append(f'<section><h2 id="{group["id"]}">{esc(group["label"])} · {group["count"]}문항</h2><div class="coverage-table"><table><thead><tr><th>문항</th><th>확인할 내용</th><th>연결 노트</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>')
    body = f'''<div class="page"><header class="topbar"><a class="brand" href="../">서브노트<span>ITPE 151기</span></a><a href="../">노트 목록</a></header><main id="main"><header class="note-header"><p class="eyebrow">확정 숙제 32개 + 셀프테스트 추가 {len(SELFTEST['extra_topics'])}개</p><h1>문제에서 노트로 연결하기.</h1><p class="lead">기본 50 · 심화 7 · 2교시형 6문항을 대조했습니다.<br>‘추가’는 숙제 32개 밖에서 새로 정리한 노트입니다.</p></header><article class="coverage-page"><p>{esc(SELFTEST['scope_note'])}</p><p>문항 제목은 학습을 위한 요약입니다. 세부 조건과 원문은 <a href="{esc(SELFTEST['source_url'])}">카페 셀프테스트 공지와 첨부 문제지</a>에서 확인하세요. 확인일: {esc(SELFTEST['checked_at'])}.</p><nav class="coverage-nav" aria-label="문제 유형"><a href="#basic">기본 50</a><a href="#advanced">심화 7</a><a href="#essay">2교시형 6</a></nav>{''.join(sections)}</article></main><footer><a href="../">전체 노트 보기</a><span>노트 연결은 학습 완료나 점수를 뜻하지 않습니다.</span></footer></div>'''
    target = OUT / 'selftest'
    target.mkdir(exist_ok=True)
    (target / 'index.html').write_text(shell('셀프테스트 문항 연결표', body, '../style.css'), encoding='utf-8')


if __name__ == '__main__':
    build()
