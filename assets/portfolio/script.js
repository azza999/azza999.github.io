const profile = window.portfolio;
const safeUrl = value => { try { const url = new URL(value); return ['https:', 'http:'].includes(url.protocol) ? url.href : null; } catch { return null; } };
function link(label, url) { const a = document.createElement('a'); a.textContent = label + ' ↗'; a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a; }
if (profile.name?.trim()) { document.title = profile.name + ' | 보안 엔지니어'; document.querySelector('#profile-name').textContent = profile.name; }
const contacts = document.querySelector('#contact-links');
if (safeUrl(profile.techBlog)) contacts.append(link('기술 블로그', safeUrl(profile.techBlog)));
if (safeUrl(profile.blog)) contacts.append(link('인문학 블로그', safeUrl(profile.blog)));
if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profile.email)) { const a = document.createElement('a'); a.textContent = profile.email; a.href = 'mailto:' + profile.email; contacts.append(a); }
const destinations = { personal: '#personal-projects', work: '#work-projects', essay: '#essay-projects' };
const labels = { problem: '문제와 배경', approach: '접근과 해결 과정', contribution: '발휘한 역량', learning: '배운 점' };
profile.projects.forEach(project => {
  const article = document.createElement('article'); article.className = 'entry project-entry' + (project.description ? ' project-entry--summary' : '');
  const heading = document.createElement('div'); heading.className = 'entry-heading';
  const title = document.createElement('h3'); title.textContent = project.title;
  const category = project.category || 'personal';
  const meta = document.createElement('span'); meta.className = 'meta'; meta.textContent = {personal:'개인 프로젝트',work:'업무 프로젝트',essay:'Troubleshooting'}[category] || '프로젝트';
  heading.append(title, meta);
  const content = document.createElement('div'); content.className = 'entry-content';
  if (project.image?.trim()) {
    try {
      const url = new URL(project.image, document.baseURI);
      if (['http:', 'https:'].includes(url.protocol)) {
        const figure = document.createElement('figure'); figure.className = 'project-figure';
        const img = document.createElement('img'); img.src = url.href; img.alt = project.imageAlt || project.title + ' 프로젝트 이미지'; img.loading = 'lazy'; img.decoding = 'async';
        img.addEventListener('error', () => figure.remove(), { once: true }); figure.append(img); content.append(figure);
      }
    } catch {}
  }
  if (project.summary?.trim()) { const p = document.createElement('p'); p.className = 'project-summary'; p.textContent = project.summary; content.append(p); }
  if (project.description?.trim()) { const p = document.createElement('p'); p.className = 'project-description'; p.textContent = project.description; content.append(p); }
  if (project.result?.trim()) { const p = document.createElement('p'); p.className = 'project-result'; p.textContent = project.result; content.append(p); }
  const copy = document.createElement('div'); copy.className = 'project-copy';
  for (const [key, label] of Object.entries(labels)) {
    const block = document.createElement('div'); const h4 = document.createElement('h4'); h4.textContent = label;
    const p = document.createElement('p'); p.textContent = project[key] || '';
    if (!p.textContent.trim()) { p.className = 'blank'; p.setAttribute('aria-label', label + ' 내용 미작성'); }
    block.append(h4, p); copy.append(block);
  }
  if (!project.description?.trim()) content.append(copy);
  if (safeUrl(project.url)) content.append(link('관련 기록', safeUrl(project.url)));
  article.append(heading, content); document.querySelector(destinations[category] || destinations.personal).append(article);
});
if (safeUrl(profile.blog)) document.querySelector('#blog-link').append(link('인문학 블로그에서 생각의 기록 읽기', safeUrl(profile.blog)));
