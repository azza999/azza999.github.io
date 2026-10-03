const $=id=>document.getElementById(id);
const labels=['아직 공부 안 함','개념 이해 완료','간단한 설명 가능','1교시형 답안 설명 가능','2교시+형 답안 빈칸 완성','스스로 답안 구조·내용 완성'];
const bands=['0점','1–19점','20–39점','40–59점','60–79점','80–99점','100점'];
const bandIndex=s=>s===0?0:s===100?6:Math.floor(s/20)+1;
const stage=t=>t.score===t.max_score?'목표 범위 완성':t.score>0&&t.score<20?'학습 시작':labels[Math.floor(t.score/20)];
const dateOf=d=>new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(d);
const number=n=>n.toLocaleString('ko-KR');const delta=n=>(n>0?'+':'')+number(n);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function chart(history){
 if(!history.length){$('chart').innerHTML='<p class="empty">첫 주제를 커밋하면 성장 기록이 시작됩니다.</p>';return;}
 const now=dateOf(new Date()),last=history.at(-1);if(now>last.date)history=[...history,{date:now,total:last.total}];
 const W=1000,H=280,L=64,R=30,T=20,B=48,max=Math.max(100,...history.map(p=>p.total)),start=Date.parse(history[0].date),end=Date.parse(history.at(-1).date);
 const x=p=>L+(Date.parse(p.date)-start)/Math.max(86400000,end-start)*(W-L-R),y=p=>H-B-p.total/max*(H-T-B);
 let line=`M ${x(history[0])} ${y(history[0])}`;for(let i=1;i<history.length;i++)line+=` H ${x(history[i])} V ${y(history[i])}`;
 let grid='';for(let i=0;i<=4;i++){const yy=H-B-i/4*(H-T-B);grid+=`<line x1="${L}" x2="${W-R}" y1="${yy}" y2="${yy}" stroke="#303d53"/><text x="${L-10}" y="${yy+5}" text-anchor="end">${Math.round(max*i/4)}</text>`;}
 $('chart').innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="날짜별 누적 점수. 현재 ${last.total}점"><title>날짜별 누적 점수</title>${grid}<path d="${line}" fill="none" stroke="#56e3b5" stroke-width="3"/>${history.map(p=>`<circle cx="${x(p)}" cy="${y(p)}" r="4" fill="#56e3b5"><title>${p.date}: ${p.total}점</title></circle>`).join('')}<text x="${L}" y="${H-10}">${history[0].date}</text><text x="${W-R}" y="${H-10}" text-anchor="end">${history.at(-1).date}</text></svg><details><summary>날짜별 수치 보기</summary><table>${history.map(p=>`<tr><td>${p.date}</td><td>${number(p.total)}점</td></tr>`).join('')}</table></details>`;
}
async function init(){
 try{const response=await fetch('data.json');if(!response.ok)throw Error('data');const d=await response.json();const today=dateOf(new Date());const monday=new Date(today+'T00:00:00Z');monday.setUTCDate(monday.getUTCDate()-((monday.getUTCDay()+6)%7));const week=monday.toISOString().slice(0,10);
 $('total').textContent=number(d.topics.reduce((s,t)=>s+t.score,0));$('today').textContent=delta(d.events.filter(e=>e.date===today).reduce((s,e)=>s+e.delta,0));$('week').textContent=delta(d.events.filter(e=>e.date>=week&&e.date<=today).reduce((s,e)=>s+e.delta,0));$('count').textContent=d.topics.filter(t=>t.score>0).length+'개';chart(d.history);
 $('levels').innerHTML=bands.map((label,i)=>{const n=d.topics.filter(t=>bandIndex(t.score)===i).length;return `<div class="level"><b>${label}</b><div><div class="track"><div class="fill" style="width:${n/Math.max(1,d.topics.length)*100}%"></div></div></div><span>${n}개</span></div>`;}).join('');
 $('events').innerHTML=d.events.length?[...d.events].reverse().slice(0,8).map(e=>`<div class="event"><div>${esc(e.title)}<small>${e.date} · ${e.before} → ${e.after}점</small></div><b class="delta ${e.delta<0?'negative':''}">${delta(e.delta)}</b></div>`).join(''):'<p class="empty">점수를 변경하고 커밋하면 이곳에 기록됩니다.</p>';
 $('topic-count').textContent=d.topics.length+'개 등록';$('topics').innerHTML=d.topics.length?d.topics.map((t,i)=>`<div class="topic"><button data-index="${i}">${esc(t.title)}<small>${esc(t.category)} · ${stage(t)}</small></button><b>${t.score} / ${t.max_score}점</b></div>`).join(''):'<p class="empty">topic-template.md를 복사해 _study/topics 폴더에 첫 주제를 추가하세요.</p>';
 $('topics').addEventListener('click',e=>{const b=e.target.closest('[data-index]');if(!b)return;const t=d.topics[Number(b.dataset.index)];$('detail-title').textContent=t.title;$('detail-meta').textContent=t.category+' · '+t.score+' / '+t.max_score+'점 · '+stage(t);$('detail-body').innerHTML=t.html;$('detail').showModal();});
 }catch(e){$('error').textContent='기록을 불러오지 못했습니다. 배포가 완료됐는지 확인하고 새로고침해 주세요.';}
}
$('close').onclick=()=>$('detail').close();init();
