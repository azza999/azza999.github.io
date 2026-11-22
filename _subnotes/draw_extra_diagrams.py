"""Draw the self-test additions with the notebook's existing SVG primitives."""
import json
from pathlib import Path


def add_extra_diagrams(Drawing, flow, cycle, save):
    specs = json.loads((Path(__file__).parent / 'extra_diagrams.json').read_text(encoding='utf-8'))
    for slug, spec in specs.items():
        labels = [s.replace('\\n', '\n') for s in spec.get('labels', [])]
        title, alt = spec['title'], spec['alt']
        footer = spec.get('footer', '')
        if slug == 'fintech':
            d = Drawing(title, alt, 390)
            d.box(30,40,220,95,'고객 접점\n모바일·웹')
            d.box(350,40,220,95,'금융 기능\nAPI·거래 처리')
            d.arrow([(250,87),(350,87)],both=True)
            d.box(30,230,540,80,'공통 기반 · 인증·암호화·이상 탐지',size=24)
            d.arrow([(140,230),(140,135)]);d.arrow([(460,230),(460,135)])
            d.text(300,365,'보호·신뢰는 금융 서비스 전 구간에 적용',22,color='#17654a')
        elif slug == 'svs-svc':
            d=Drawing(title,alt,590)
            d.rect(20,20,560,550,fill='#f8faff')
            d.text(300,55,'SVS · 서비스 가치 시스템',26,weight=650)
            d.text(300,93,'지도 원칙 · 거버넌스',23)
            d.rect(35,120,530,365,fill='white')
            d.text(300,151,'SVC · 서비스 가치사슬',23,color='#17654a')
            nodes=[(50,175,'계획'),(325,175,'개선'),(50,280,'관여'),(325,280,'설계·전환'),(50,385,'획득·구축'),(325,385,'제공·지원')]
            for x,y,label in nodes:d.box(x,y,225,70,label,size=24)
            d.line(300,210,300,420)
            for x,y,_ in nodes:d.line(275 if x<300 else 325,y+35,300,y+35)
            d.text(300,523,'프랙티스 · 지속적 개선',23)
            d.text(300,558,'기회·수요 → 활동 조합 → 가치',22,color='#17654a')
        elif slug == 'itil-v4':
            d=Drawing(title,alt,465)
            coords=[(25,30,'조직·사람'),(335,30,'정보·기술'),(25,300,'파트너·공급자'),(335,300,'가치흐름·프로세스')]
            for x,y,label in coords:d.box(x,y,240,90,label,size=23)
            d.box(195,180,210,90,'서비스 가치',fill='#e8f4ee',size=25)
            for x,y,_ in coords:
                d.line(x+120,y+90 if y<150 else y,x+120,225)
                d.line(x+120,225,195 if x<300 else 405,225)
            d.text(300,440,'SVS · 34 관리 프랙티스로 연결',23,color='#17654a')
        elif slug == 'bcp':
            d=Drawing(title,alt,490)
            d.box(145,20,310,65,'BIA · 우선순위·복구 목표',size=23)
            d.arrow([(300,85),(300,130)])
            d.rect(30,130,540,325,fill='#eef3fc')
            d.text(300,173,'BCP · 업무연속성 계획',26,weight=650)
            d.text(300,223,'사람 · 장소 · 협력사 · 연락 · 업무',23)
            d.box(75,275,450,80,'DRP · IT 시스템·데이터 복구 계획',size=23)
            d.text(300,416,'DRS · 복구 자원과 기술 체계',23,color='#17654a')
        elif slug == 'sow-sla-slm':
            d=Drawing(title,alt,350)
            for x,label in [(20,'SoW\n범위·책임'),(210,'SLA\n수준·측정 합의'),(400,'SLM\n지속 수준관리')]:d.box(x,50,164,96,label,size=23)
            d.arrow([(184,98),(210,98)]);d.arrow([(374,98),(400,98)])
            d.arrow([(482,146),(482,205),(102,205),(102,146)],dashed=True)
            d.text(300,255,'운영 결과를 범위·약속에 환류',23,color='#17654a')
            d.text(300,315,'SLM은 요구 파악·협상부터 관여',21)
        elif slug == 'okr':
            d=Drawing(title,alt,420)
            d.box(145,25,310,80,'Objective · 목표',size=25)
            for x,label in [(30,'KR 1 · 핵심결과'),(330,'KR 2 · 핵심결과')]:
                d.box(x,185,240,80,label,size=24)
                d.line(300,105,300,145);d.line(300,145,x+120,145);d.line(x+120,145,x+120,185)
            d.box(145,335,310,65,'실행과제 · 결과를 위한 수단',size=22)
            d.arrow([(235,335),(150,265)]);d.arrow([(365,335),(450,265)])
        elif slug == 'ahp':
            d=Drawing(title,alt,440)
            d.box(170,20,260,65,'의사결정 목표')
            for x,label in [(25,'기준 A'),(215,'기준 B'),(405,'기준 C')]:
                d.arrow([(300,85),(300,115),(x+85,115),(x+85,150)])
                d.box(x,150,170,65,label,size=24)
                d.arrow([(x+85,215),(x+85,245)])
            d.box(30,245,540,65,'쌍대비교 · 가중치 · 일관성 점검',size=23)
            for x,label in [(75,'대안 1'),(345,'대안 2')]:
                d.box(x,360,180,65,label,size=24)
                d.arrow([(300,310),(300,335),(x+90,335),(x+90,360)])
        elif slug == 'government-ea':
            d=Drawing(title,alt,400)
            d.box(160,20,280,70,'범정부 EA')
            for x,label,question in [(20,'메타모델','무엇을 기록?\n산출물·속성·관계'),(215,'참조모형','어떤 공통 기준?\n분류·재사용'),(410,'성숙도 모델','어느 수준?\n평가·개선')]:
                d.arrow([(300,90),(300,125),(x+85,125),(x+85,165)])
                d.box(x,165,170,70,label,size=23);d.text(x+85,290,question,21)
            d.text(300,375,'모델별 목적·내용·활용을 구분',23,color='#17654a')
        elif slug == 'strategy-environment':
            d=Drawing(title,alt,400)
            d.box(30,35,240,110,'외부환경\n기회·위협');d.box(330,35,240,110,'내부환경\n강점·약점')
            d.arrow([(150,145),(150,205),(300,205),(300,250)])
            d.arrow([(450,145),(450,205),(300,205)])
            d.box(100,250,400,100,'SWOT · 대안 비교\n전략 과제·실행 우선순위',size=24)
            d.text(300,390,'같은 기준일·목표·사업 범위에서 분석',22,color='#17654a')
        elif slug == 'idc-location':
            d=Drawing(title,alt,440)
            for x,y,label in [(25,30,'재난·지정학\n동시 피해 위험'),(335,30,'전력·통신·시설\n경로 독립성'),(25,300,'거리·지연\n복제·RPO'),(335,300,'운영·인력·비용\n접근·지원')]:
                d.box(x,y,240,95,label,size=23)
                d.arrow([(x+120,y+95 if y<150 else y),(x+120,235),(195 if x<300 else 405,235)])
            d.box(195,185,210,95,'입지·복구 전략\nRTO·RPO 검증',fill='#e8f4ee',size=23)
        elif slug == 'open-banking':
            d=Drawing(title,alt,425)
            positions=[(30,40,'이용자\n동의·인증'),(330,40,'이용기관\n앱·서비스'),(330,245,'공동 플랫폼\n표준 API·중계'),(30,245,'참가기관\n계좌·금융 기능')]
            for x,y,label in positions:d.box(x,y,240,100,label,size=24)
            d.arrow([(270,90),(330,90)],both=True);d.arrow([(450,140),(450,245)],both=True);d.arrow([(330,295),(270,295)],both=True)
            d.text(260,200,'동의한 기능·범위 안에서 연결',22,color='#17654a')
            d.text(300,400,'요청과 결과 · 인증·권한·거래 보호',22,color='#17654a')
        elif len(labels)>6:
            rows=(len(labels)+2)//3;d=Drawing(title,alt,rows*150+100)
            coords=[]
            for i,label in enumerate(labels):
                row=i//3;col=i%3 if row%2==0 else 2-i%3;x=20+col*190;y=30+row*150
                d.box(x,y,160,90,label,size=22);coords.append((x,y))
            for (x,y),(nx,ny) in zip(coords,coords[1:]):
                if y==ny:d.arrow([(x+160 if nx>x else x,y+45),(nx if nx>x else nx+160,ny+45)])
                else:d.arrow([(x+80,y+90),(nx+80,ny)])
            d.text(300,d.height-30,footer,21,color='#17654a')
        elif spec.get('kind')=='cycle' and len(labels)==4:
            d=cycle(title,alt,labels,spec.get('center','검토 · 개선'))
        else:
            d=flow(title,alt,labels,footer,feedback=(slug=='sow-sla-slm'))
        save(slug,d,spec['draw'],spec['read'],spec['sources'],spec['adaptation'])
