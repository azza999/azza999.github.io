const profile = window.portfolio;
const safeUrl = value => { try { const url = new URL(value); return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : null; } catch { return null; } };
function icon(name) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'ui-icon'); svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('aria-hidden', 'true');
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use'); use.setAttribute('href', '#icon-' + name); svg.append(use); return svg;
}
function link(label, url) { const a = document.createElement('a'); a.append(icon(label === 'GitHub' ? 'code' : 'book'), document.createTextNode(label + ' ↗')); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a; }
if (profile.name.trim()) { document.title = profile.name + ' | 배움의 기록'; document.querySelector('.small-note').textContent = profile.name + ' · 기술과 사람 사이, 계속 배우는 중'; }
const labels = { problem: '문제와 배경', approach: '접근과 해결 과정', contribution: '발휘한 역량', learning: '배운 점' };
profile.projects.forEach((project, index) => {
  const details = document.createElement('details'); details.className = 'project';
  const summary = document.createElement('summary');
  const number = document.createElement('span'); number.className = 'project-number'; number.textContent = String(index + 1).padStart(2, '0');
  const title = document.createElement('h3'); title.textContent = project.title;
  const kind = document.createElement('span'); kind.className = 'project-kind'; kind.textContent = project.kind;
  const plus = document.createElement('span'); plus.className = 'plus'; plus.textContent = '+'; plus.setAttribute('aria-hidden', 'true');
  const thumbnail = document.createElement('span'); thumbnail.className = 'project-thumbnail';
  const placeholder = () => { thumbnail.classList.add('is-placeholder'); const label = document.createElement('span'); label.textContent = 'IMAGE / ' + String(index + 1).padStart(2, '0'); thumbnail.replaceChildren(icon('image'), label); };
  let imageUrl;
  try { if (project.image?.trim()) { const parsed = new URL(project.image, document.baseURI); if (['http:', 'https:'].includes(parsed.protocol)) imageUrl = parsed.href; } } catch {}
  if (imageUrl) {
    const img = document.createElement('img'); img.src = imageUrl; img.alt = project.imageAlt || project.title + ' 프로젝트 이미지'; img.loading = 'lazy'; img.decoding = 'async'; img.addEventListener('error', placeholder, { once: true }); thumbnail.append(img);
  } else placeholder();
  const projectInfo = document.createElement('div'); projectInfo.className = 'project-info'; projectInfo.append(title, kind);
  summary.append(number, thumbnail, projectInfo, plus); details.append(summary);
  const body = document.createElement('div'); body.className = 'project-body';
  if (project.summary.trim()) { const p = document.createElement('p'); p.textContent = project.summary; body.append(p); }
  for (const [key, label] of Object.entries(labels)) { const block = document.createElement('div'); const heading = document.createElement('h4'); heading.textContent = label; const text = document.createElement('p'); text.className = project[key].trim() ? 'project-text' : 'empty-line'; text.textContent = project[key]; if (!project[key].trim()) text.setAttribute('aria-label', label + ' 내용 미작성'); block.append(heading, text); body.append(block); }
  const url = safeUrl(project.url); if (url) body.append(link('관련 기록 읽기', url));
  details.append(body); document.querySelector('#project-list').append(details);
});
const blog = safeUrl(profile.blog); if (blog) document.querySelector('#blog-link').replaceChildren(link('네이버 블로그에서 읽기', blog));
const contacts = document.querySelector('#contact-links');
if (safeUrl(profile.github)) contacts.append(link('GitHub', safeUrl(profile.github)));
if (blog) contacts.append(link('Naver Blog', blog));
if (safeUrl(profile.techBlog)) contacts.append(link('Tech Blog', safeUrl(profile.techBlog)));
if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profile.email)) { const a = document.createElement('a'); a.textContent = '이메일 보내기 ↗'; a.href = 'mailto:' + profile.email; contacts.append(a); }
if (!contacts.children.length) { const p = document.createElement('p'); p.className = 'contact-pending'; p.textContent = '연락처와 프로필 링크를 준비하고 있습니다.'; contacts.append(p); }

// 인쇄할 때 접힌 프로젝트까지 포함하고, 인쇄가 끝나면 이전 상태로 복구합니다.
let printStates;
window.addEventListener('beforeprint', () => {
  if (printStates) return;
  printStates = [...document.querySelectorAll('details')].map(item => [item, item.open]);
  printStates.forEach(([item]) => { item.open = true; });
});
window.addEventListener('afterprint', () => {
  printStates?.forEach(([item, open]) => { item.open = open; });
  printStates = null;
});
