import {segment,paginate,drawing,toSVG} from './layout.js';
import {makePDF,renderJPEG} from './pdf.js';
const $=id=>document.getElementById(id),KEY='hangeul-practice-v1';
const presets=[
{id:'daily',title:'마음을 고르는 시간',content:'서두르지 않아도 괜찮다.\n오늘의 나는 어제보다 조금 더 나아지고 있다.\n작은 걸음이 모여 나만의 길이 된다.\n잠시 멈추어 숨을 고르고, 다시 한 걸음을 내딛는다.\n내 마음에 다정한 문장 하나를 건네는 시간.'},
{id:'season',title:'계절을 걷는 문장',content:'창문 너머로 가을빛이 내려앉는다.\n바람은 나뭇잎 사이를 지나고, 햇살은 책장 위에 머문다.\n따뜻한 차 한 잔을 곁에 두고 오늘의 마음을 천천히 적는다.'},
{id:'basics',title:'한글 기초 연습',content:'가나다라마바사아자차카타파하\n고노도로모보소오조초코토포호\n구누두루무부수우주추쿠투푸후\n기니디리미비시이지치키티피히\n아름다운 우리말을 바르게 씁니다.'}
];
const builtinFonts=[{id:'pen',name:'나눔손글씨 펜',family:'Pen'},{id:'myeongjo',name:'나눔명조',family:'Myeongjo'},{id:'gothic',name:'나눔고딕',family:'Nanum'}];
const defaults={title:presets[0].title,content:presets[0].content,preset:'daily',font:'pen',size:70,opacity:20,columns:12,guide:'cross',color:'#b77770',mode:'trace',spaces:true};
let state={...defaults},texts=[],fonts=[],readyFonts=new Map(),pages=[],ops=[],renderVersion=0,timer,noticeTimer;
function notify(message,persistent=false){clearTimeout(noticeTimer);$('status').textContent=message;if(!persistent)noticeTimer=setTimeout(()=>$('status').textContent='',4800);}
function save(){try{localStorage.setItem(KEY,JSON.stringify({version:1,state,texts,fonts}));return true;}catch{notify('브라우저 저장 공간이 부족하거나 저장이 차단됐습니다. 현재 내용은 PDF로 내려받을 수 있어요.',true);return false;}}
function restore(){try{const data=JSON.parse(localStorage.getItem(KEY)||'null');if(!data)return;if(data.version!==1)throw Error();const s=data.state||{};for(const key of ['title','content']) if(typeof s[key]==='string')state[key]=s[key].slice(0,key==='title'?50:12000);for(const key of ['preset','font'])if(typeof s[key]==='string' && /^[\w-]{1,80}$/.test(s[key]))state[key]=s[key];for(const [key,values] of Object.entries({size:[45,50,55,60,65,70,75,80,85],opacity:[10,15,20,25,30,35,40,45,50],columns:[10,12,14,16,20],guide:['plain','cross','diagonal','vertical','graph'],color:['#b77770','#7a8a7c','#8a8a8a'],mode:['trace','trace-only','blank','both','empty']}))if(values.includes(s[key]))state[key]=s[key];if(typeof s.spaces==='boolean')state.spaces=s.spaces;texts=Array.isArray(data.texts)?data.texts.filter(x=>typeof x.id==='string'&&typeof x.title==='string'&&typeof x.content==='string'&&x.content.length<=12000):[];fonts=Array.isArray(data.fonts)?data.fonts.filter(x=>/^font-[\w-]+$/.test(x.id)&&typeof x.name==='string'&&typeof x.data==='string'&&/^data:[^,]*;base64,[A-Za-z0-9+/=]+$/.test(x.data)&&x.data.length<2900000):[];}catch{notify('저장된 내용을 읽을 수 없어 기본 양식을 열었습니다.',true);}}
function fontList(){return [...builtinFonts,...fonts.map(f=>({...f,family:f.id}))];}
function refreshOptions(){
  $('preset').replaceChildren(new Option('직접 입력 중', 'draft'));for(const [label,items] of [['기본 글',presets],['내 글',texts]]){if(!items.length)continue;const group=document.createElement('optgroup');group.label=label;for(const t of items)group.append(new Option(t.title||'제목 없는 글',t.id));$('preset').append(group);}
  $('preset').value=[...presets,...texts].some(t=>t.id===state.preset)?state.preset:'draft';
  $('font').replaceChildren(...fontList().map(f=>new Option(f.name,f.id)));$('font').value=state.font;
  $('delete-text').disabled=!texts.some(t=>t.id===state.preset);$('delete-font').disabled=!fonts.some(f=>f.id===state.font);
}
function syncControls(){for(const key of ['title','content','font','size','opacity','columns','guide','color','mode'])$(key).value=state[key];$('spaces').checked=state.spaces;refreshOptions();}
async function ensureFont(){const font=fontList().find(f=>f.id===state.font)||builtinFonts[0];if(font.data&&!readyFonts.has(font.id)){const face=new FontFace(font.family,`url("${font.data}")`);await face.load();document.fonts.add(face);readyFonts.set(font.id,face);}await Promise.all([document.fonts.load(`20px "${font.family}"`),document.fonts.load('20px "Myeongjo"'),document.fonts.load('20px "Nanum"')]);return font.family;}
const measure=document.createElement('canvas').getContext('2d');
async function render(){
  const version=++renderVersion;$('mode-hint').textContent=state.mode==='trace-only'?'옅은 글씨 위에 바로 따라 써 보세요.':'보고 쓰고, 옅은 글씨 위에 한 번 더.';$('size-value').textContent=`칸의 ${state.size}%`;$('opacity-value').textContent=`${state.opacity}%`;$('char-count').textContent=`${segment(state.content).length.toLocaleString()}자`;
  let family;try{family=await ensureFont();}catch{if(version!==renderVersion)return;state.font='pen';$('font').value='pen';family='Pen';notify('글꼴을 읽을 수 없어 기본 글꼴로 변경했습니다.');}
  if(version!==renderVersion)return;
  $('font-sample').style.fontFamily=`"${family}"`;
  pages=paginate(state);ops=pages.map((p,i)=>drawing(p,state,i,pages.length,family));
  for(const page of ops)for(const op of page)if(op.type==='text'&&op.maxWidth){measure.font=`${op.size}px "${op.font}"`;if(measure.measureText(op.value).width>op.maxWidth)op.fitWidth=op.maxWidth;}
  $('pages').innerHTML=ops.map((o,i)=>`<div class="sheet">${toSVG(o,i)}</div>`).join('');$('page-count').textContent=`총 ${pages.length}페이지`;
}
function changed(){clearTimeout(timer);timer=setTimeout(()=>{save();render();},180);}
for(const key of ['title','content','size','opacity','columns','guide','color','mode','spaces'])$(key).addEventListener('input',()=>{state[key]=$(key).type==='checkbox'?$(key).checked:['size','opacity','columns'].includes(key)?Number($(key).value):$(key).value;if(['title','content'].includes(key)){state.preset='draft';refreshOptions();}changed();});
$('preset').addEventListener('change',()=>{const p=[...presets,...texts].find(t=>t.id===$('preset').value);if(!p)return;Object.assign(state,{title:p.title,content:p.content,preset:p.id});syncControls();save();render();});
$('font').addEventListener('change',()=>{state.font=$('font').value;refreshOptions();save();render();});
$('save-text').addEventListener('click',()=>{if(!state.content.trim())return notify('저장할 글을 먼저 입력해 주세요.');const prev=[...texts],prevPreset=state.preset;const item={id:`text-${crypto.randomUUID()}`,title:state.title.trim()||'제목 없는 글',content:state.content};texts=[...texts,item];state.preset=item.id;if(!save()){texts=prev;state.preset=prevPreset;return;}refreshOptions();notify('내 글 보관함에 저장했습니다.');});
$('delete-text').addEventListener('click',()=>{const index=texts.findIndex(t=>t.id===state.preset);if(index<0)return;const old=texts;texts=texts.filter((_,i)=>i!==index);if(!save()){texts=old;return;}refreshOptions();notify('보관함에서 삭제했습니다. 편집 중인 내용은 그대로 남아 있어요.');});
$('text-file').addEventListener('change',async e=>{const file=e.target.files[0];try{if(!file)return;if(!/\.txt$/i.test(file.name))throw Error('TXT 파일을 선택해 주세요.');if(file.size>100000)throw Error('100KB 이하의 텍스트 파일을 선택해 주세요.');const content=new TextDecoder('utf-8',{fatal:true}).decode(await file.arrayBuffer()).replace(/^\uFEFF/,'');if(content.length>12000)throw Error('글은 12,000자까지 불러올 수 있습니다.');state.preset='draft';state.content=content;state.title=file.name.replace(/\.txt$/i,'').slice(0,50);syncControls();save();await render();notify('글을 불러왔습니다. 내 글 저장을 누르면 보관함에도 추가돼요.');}catch(err){notify(err instanceof TypeError?'UTF-8로 저장된 텍스트 파일을 선택해 주세요.':err.message);}finally{e.target.value='';}});
$('font-file').addEventListener('change',async e=>{const file=e.target.files[0];let face;try{if(!file)return;if(!/\.(ttf|otf|woff2?)$/i.test(file.name))throw Error('TTF, OTF, WOFF, WOFF2 파일을 선택해 주세요.');if(file.size>2*1024*1024)throw Error('글꼴은 2MB 이하의 파일을 선택해 주세요.');const data=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsDataURL(file);});const id=`font-${crypto.randomUUID()}`;face=new FontFace(id,`url("${data}")`);await face.load();const item={id,name:file.name.replace(/\.[^.]+$/,''),data};const previous=state.font;fonts.push(item);state.font=id;if(!save()){fonts.pop();state.font=previous;return;}document.fonts.add(face);readyFonts.set(id,face);refreshOptions();await render();notify('글꼴을 이 브라우저에 저장했습니다.');}catch{notify('글꼴을 추가할 수 없습니다. 파일 형식과 크기(최대 2MB)를 확인해 주세요.');}finally{e.target.value='';}});
$('delete-font').addEventListener('click',()=>{const id=state.font;if(!fonts.some(f=>f.id===id))return;const old=fonts;fonts=fonts.filter(f=>f.id!==id);state.font='pen';if(!save()){fonts=old;state.font=id;return;}if(readyFonts.has(id)){document.fonts.delete(readyFonts.get(id));readyFonts.delete(id);}refreshOptions();render();notify('업로드한 글꼴을 삭제했습니다.');});
$('print').addEventListener('click',async()=>{clearTimeout(timer);save();await render();await document.fonts.ready;window.print();});
$('download').addEventListener('click',async()=>{
  const button=$('download');button.disabled=true;
  try{clearTimeout(timer);save();await render();await document.fonts.ready;const snapshot=ops.map(page=>page.map(op=>({...op}))),filename=state.title||'한글한글';const images=[];
    for(let i=0;i<snapshot.length;i++){button.textContent=`PDF 만드는 중 ${i+1}/${snapshot.length}`;images.push(await renderJPEG(snapshot[i]));}
    const url=URL.createObjectURL(makePDF(images)),a=document.createElement('a');a.href=url;a.download=`${filename.replace(/[<>:"/\\|?*\x00-\x1F]/g,'_')}.pdf`;a.click();setTimeout(()=>URL.revokeObjectURL(url),60000);notify('PDF를 다운로드했습니다. A4 크기로 인쇄해 주세요.');
  }catch(err){console.error(err);notify('PDF를 만들지 못했습니다. 인쇄 버튼에서 PDF로 저장을 이용해 주세요.');}finally{button.disabled=false;button.textContent='↓ PDF 다운로드';}
});
window.addEventListener('pagehide',()=>{if(timer){clearTimeout(timer);save();}});
restore();if(!fontList().some(f=>f.id===state.font))state.font='pen';syncControls();render();
