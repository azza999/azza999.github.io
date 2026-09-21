// Pure layout functions: the preview, printout and PDF share these drawing operations.
export const segment = text => typeof Intl.Segmenter === 'function' ? [...new Intl.Segmenter('ko', {granularity:'grapheme'}).segment(text)].map(x=>x.segment) : Array.from(text);
export function splitLines(text, columns, keepSpaces=true) {
  const lines=[];
  for (const paragraph of text.replace(/\r\n?/g,'\n').normalize('NFC').split('\n')) {
    const chars=segment(keepSpaces ? paragraph.replace(/\t/g,' ') : paragraph.replace(/[\t ]/g,''));
    if (!chars.length) lines.push([]);
    for(let i=0;i<chars.length;i+=columns) lines.push(chars.slice(i,i+columns));
  }
  return lines;
}
export function paginate(state) {
  const cell=170/state.columns, repeat=state.mode==='both'?3:2;
  const groups=Math.floor(220/(cell*repeat));
  const lines=state.mode==='empty'?[[]]:splitLines(state.content,state.columns,state.spaces);
  const pages=[];
  for(let i=0;i<lines.length;i+=groups) pages.push({lines:lines.slice(i,i+groups),cell,groups,repeat});
  return pages;
}
export function drawing(page,state,index,total,family) {
  const ops=[];
  const line=(x1,y1,x2,y2,color,width=.16,dash=false)=>ops.push({type:'line',x1,y1,x2,y2,color,width,dash});
  const text=(value,x,y,size,font,color='#30352f',maxWidth)=>ops.push({type:'text',value,x,y,size,font,color,maxWidth});
  text('한 글 한 글',105,18,2.3,'Nanum','#89917f');
  text(state.title||'나의 글씨 연습',105,30,6,'Myeongjo','#30372f',168);
  text('천천히 바라보고, 정성껏 따라 쓰기',105,39,2.4,'Nanum','#959a8e');
  const {cell,groups,repeat}=page, rows=groups*repeat, top=51;
  for(let r=0;r<rows;r++) for(let c=0;c<state.columns;c++) {
    const x=20+c*cell,y=top+r*cell, guideColor=state.color+'70';
    if(['cross','graph'].includes(state.guide)) {
      line(x+cell/2,y,x+cell/2,y+cell,guideColor,.12,true);
      line(x,y+cell/2,x+cell,y+cell/2,guideColor,.12,true);
    }
    if(state.guide==='graph') for(const f of [.25,.75]) {
      line(x+cell*f,y,x+cell*f,y+cell,guideColor,.1,true);
      line(x,y+cell*f,x+cell,y+cell*f,guideColor,.1,true);
    }
    if(state.guide==='vertical') line(x+cell/2,y,x+cell/2,y+cell,guideColor,.12,true);
    if(state.guide==='diagonal') {line(x,y+cell,x+cell/2,y,guideColor,.14);line(x+cell/2,y+cell,x+cell,y,guideColor,.14,true);}
    const group=Math.floor(r/repeat), kind=r%repeat;
    const value=page.lines[group]?.[c];
    if(value && state.mode!=='empty' && (kind===0 || kind===1 && state.mode!=='blank')) {
      const channel=Math.round(255-(255-48)*state.opacity/100).toString(16).padStart(2,'0');
      text(value,x+cell/2,y+cell*.54,cell*state.size/100,family,kind===0?'#30352f':`#${channel}${channel}${channel}`,cell*.9);
    }
  }
  for(let c=0;c<=state.columns;c++) line(20+c*cell,top,20+c*cell,top+rows*cell,state.color,.2);
  for(let r=0;r<=rows;r++) line(20,top+r*cell,190,top+r*cell,state.color,r%repeat===0?.23:.15);
  text('나만의 필사 연습장',38,283,2.1,'Nanum','#a1a697');
  text(`${index+1} / ${total}`,183,283,2.3,'Nanum','#a1a697');
  return ops;
}
export const escapeXML = value => String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
export function toSVG(ops,index) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 297" role="img" aria-label="원고지 ${index+1}페이지"><rect width="210" height="297" fill="white"/>${ops.map(o=>o.type==='line'?`<line x1="${o.x1}" y1="${o.y1}" x2="${o.x2}" y2="${o.y2}" stroke="${o.color}" stroke-width="${o.width}" ${o.dash?'stroke-dasharray=".45 .6"':''}/>`:`<text x="${o.x}" y="${o.y}" font-size="${o.size}" font-family="${escapeXML(o.font)}" fill="${o.color}" text-anchor="middle" dominant-baseline="central"${o.fitWidth?` textLength="${o.fitWidth}" lengthAdjust="spacingAndGlyphs"`:''}>${escapeXML(o.value)}</text>`).join('')}</svg>`;
}
