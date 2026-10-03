import json, subprocess, shutil, re, html
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parents[1]
REPO = Path(subprocess.check_output(['git','-C',str(ROOT),'rev-parse','--show-toplevel']).decode().strip())
PREFIX = ROOT.relative_to(REPO).as_posix()
TOPICS = (PREFIX + '/topics') if PREFIX != '.' else 'topics'
def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args]).decode('utf-8')
def parse(text, path):
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError(f'{path}: front matter가 필요합니다')
    front, body = text[4:].split('\n---\n',1)
    meta = {}
    for line in front.splitlines():
        if not line.strip() or line.startswith('#'): continue
        key, value = line.split(':',1)
        meta[key.strip()] = value.strip().strip('"\'')
    score = int(meta.get('score',0))
    max_score = int(meta.get('max_score',100))
    if not 1 <= max_score <= 100 or not 0 <= score <= max_score:
        raise ValueError(f'{path}: max_score는 1~100, score는 0~max_score 범위의 정수여야 합니다')
    if not meta.get('id') or not meta.get('title'): raise ValueError(f'{path}: id와 title이 필요합니다')
    return dict(id=meta['id'],title=meta['title'],category=meta.get('category','기타'),score=score,max_score=max_score,body=body,path=path)
def snapshot(rev=None):
    paths = git('ls-tree','--full-tree','-r','--name-only',rev,'--',TOPICS).splitlines() if rev else [str(p.relative_to(ROOT)) for p in sorted((ROOT/'topics').rglob('*.md'))]
    topics=[]
    for path in paths:
        if not path.endswith('.md'): continue
        text = git('show',f'{rev}:{path}') if rev else (ROOT/path).read_text()
        topics.append(parse(text,path))
    ids=[t['id'] for t in topics]
    if len(ids)!=len(set(ids)): raise ValueError('topic id 중복')
    return topics
def render_md(body):
    # Raw HTML is always escaped. Standard library only: headings, paragraphs,
    # lists, fenced code, bold, inline code and simple tables.
    lines=body.splitlines(); out=[]; fence=False; listing=False; table=False
    def inline(s):
        s=html.escape(s)
        s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
        return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    for line in lines:
        if line.startswith('```'):
            if listing: out.append('</ul>'); listing=False
            if table: out.append('</tbody></table></div>'); table=False
            out.append('</code></pre>' if fence else '<pre><code>'); fence=not fence; continue
        if fence: out.append(html.escape(line)+'\n'); continue
        if line.startswith('|') and line.endswith('|'):
            if re.fullmatch(r'[\s|:\-]+',line): continue
            if not table: out.append('<div class="table-scroll"><table><tbody>'); table=True
            out.append('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in line.strip('|').split('|'))+'</tr>'); continue
        if table: out.append('</tbody></table></div>'); table=False
        if line.startswith(('- ','* ')):
            if not listing: out.append('<ul>'); listing=True
            out.append('<li>'+inline(line[2:])+'</li>'); continue
        if listing: out.append('</ul>'); listing=False
        m=re.match(r'^(#{1,6}) (.*)',line)
        if m: n=len(m[1]); out.append(f'<h{n}>{inline(m[2])}</h{n}>')
        elif line.strip(): out.append('<p>'+inline(line)+'</p>')
    if listing: out.append('</ul>')
    if table: out.append('</tbody></table></div>')
    if fence: out.append('</code></pre>')
    return ''.join(out)
def build():
    current=snapshot(); daily={}; events=[]; previous={}
    try: commits=git('log','--first-parent','--reverse','--format=%H %cI','HEAD','--',TOPICS).splitlines()
    except subprocess.CalledProcessError: commits=[]
    for row in commits:
        rev,stamp=row.split(' ',1); day=datetime.fromisoformat(stamp).astimezone(ZoneInfo('Asia/Seoul')).date().isoformat()
        topics=snapshot(rev); scores={t['id']:t['score'] for t in topics}; lookup={t['id']:t for t in topics}
        for key in sorted(set(previous)|set(scores)):
            before=previous.get(key,0); after=scores.get(key,0)
            if before!=after:
                events.append(dict(date=day,title=lookup.get(key,{}).get('title',key),before=before,after=after,delta=after-before,commit=rev[:7]))
        daily[day]=sum(scores.values()); previous=scores
    for t in current: t['html']=render_md(t.pop('body'))
    out=REPO/'study'; out.mkdir(exist_ok=True)
    for p in (ROOT/'web').iterdir(): shutil.copy2(p,out/p.name)
    (out/'data.json').write_text(json.dumps(dict(topics=current,history=[dict(date=k,total=v) for k,v in sorted(daily.items())],events=events),ensure_ascii=False))
    (out/'.nojekyll').touch()
    print(f'Built {len(current)} topics, {len(events)} score changes -> {out}')
if __name__=='__main__': build()
