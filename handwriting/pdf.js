// A small PDF writer for locally rendered JPEG pages; no service, CDN or font upload.
const bytes = value => new TextEncoder().encode(value);
export function makePDF(images) {
  const chunks=[], offsets=[0]; let length=0;
  const add=value=>{const data=typeof value==='string'?bytes(value):value;chunks.push(data);length+=data.length;};
  const object=(id,content)=>{offsets[id]=length;add(`${id} 0 obj\n${content}\nendobj\n`);};
  add('%PDF-1.4\n');
  object(1,'<< /Type /Catalog /Pages 2 0 R >>');
  object(2,`<< /Type /Pages /Count ${images.length} /Kids [${images.map((_,i)=>`${3+i*3} 0 R`).join(' ')}] >>`);
  images.forEach((image,i)=>{
    const id=3+i*3;
    object(id,`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.276 841.89] /Resources << /XObject << /Im0 ${id+1} 0 R >> >> /Contents ${id+2} 0 R >>`);
    offsets[id+1]=length;
    add(`${id+1} 0 obj\n<< /Type /XObject /Subtype /Image /Width ${image.width} /Height ${image.height} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${image.data.length} >>\nstream\n`);
    add(image.data);add('\nendstream\nendobj\n');
    const content='q\n595.276 0 0 841.89 0 0 cm\n/Im0 Do\nQ\n';
    object(id+2,`<< /Length ${bytes(content).length} >>\nstream\n${content}endstream`);
  });
  const start=length,count=3+images.length*3;
  add(`xref\n0 ${count}\n0000000000 65535 f \n`);
  for(let i=1;i<count;i++) add(`${String(offsets[i]).padStart(10,'0')} 00000 n \n`);
  add(`trailer\n<< /Size ${count} /Root 1 0 R >>\nstartxref\n${start}\n%%EOF`);
  return new Blob(chunks,{type:'application/pdf'});
}
export async function renderJPEG(ops) {
  const scale=240/25.4,canvas=document.createElement('canvas');
  canvas.width=Math.round(210*scale);canvas.height=Math.round(297*scale);
  const ctx=canvas.getContext('2d');ctx.fillStyle='white';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.scale(scale,scale);
  for(const o of ops) {
    if(o.type==='line') {
      ctx.strokeStyle=o.color;ctx.lineWidth=o.width;ctx.setLineDash(o.dash?[.45,.6]:[]);ctx.beginPath();ctx.moveTo(o.x1,o.y1);ctx.lineTo(o.x2,o.y2);ctx.stroke();
    } else {
      ctx.fillStyle=o.color;ctx.font=`${o.size}px "${o.font}"`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(o.value,o.x,o.y,o.maxWidth||1000);
    }
  }
  const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',.96));
  if(!blob) throw Error('이미지를 만들 수 없습니다.');
  return {width:canvas.width,height:canvas.height,data:new Uint8Array(await blob.arrayBuffer())};
}
