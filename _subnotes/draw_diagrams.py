"""Render hand-drawable, source-reviewed concept diagrams (standard library only)."""
from pathlib import Path
import html
import json
import math

ROOT = Path(__file__).resolve().parent
DEST = ROOT.parent / 'assets/subnotes/concepts'
MANIFEST = {}
INK, BLUE, SOFT, GREEN = '#17263c', '#2858b6', '#eef3fc', '#17654a'

def e(s): return html.escape(str(s), quote=True)

class Drawing:
    def __init__(self, title, description, height=440):
        self.title, self.description, self.height = title, description, height
        self.parts = []
    def text(self, x, y, lines, size=24, color=INK, weight=500, anchor='middle'):
        if isinstance(lines, str): lines = lines.split('\n')
        for i, line in enumerate(lines):
            self.parts.append(f'<text x="{x}" y="{y+i*(size+9)}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{e(line)}</text>')
    def rect(self, x, y, w, h, fill='white', stroke=BLUE, dashed=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="2.5"'+(' stroke-dasharray="8 6"' if dashed else '')+'/>')
    def box(self, x, y, w, h, lines, fill=SOFT, size=24):
        self.rect(x,y,w,h,fill)
        if isinstance(lines,str): lines=lines.split('\n')
        self.text(x+w/2,y+h/2-(len(lines)-1)*(size+9)/2+size*.35,lines,size,weight=600)
    def line(self, x1,y1,x2,y2,color=BLUE,dash=False):
        self.parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2.5" fill="none"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
    def arrow(self, points, color=BLUE, dashed=False, both=False):
        d='M'+' L'.join(f'{x} {y}' for x,y in points)
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round"'+(' stroke-dasharray="7 5"' if dashed else '')+'/>')
        # Explicit arrowheads also survive image export engines without SVG marker support.
        ends = [(points[-2], points[-1])]
        if both: ends.append((points[1], points[0]))
        for previous, tip in ends:
            angle = math.atan2(tip[1]-previous[1], tip[0]-previous[0])
            bx, by = tip[0]-10*math.cos(angle), tip[1]-10*math.sin(angle)
            ax, ay = bx+5*math.sin(angle), by-5*math.cos(angle)
            cx, cy = bx-5*math.sin(angle), by+5*math.cos(angle)
            self.parts.append(f'<path d="M{ax:.2f} {ay:.2f} L{tip[0]} {tip[1]} L{cx:.2f} {cy:.2f}" fill="none" stroke="{color}" stroke-width="2.5"/>')
    def circle(self,x,y,r,fill=SOFT):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{BLUE}" stroke-width="2.5"/>')
    def svg(self):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{self.height}" viewBox="0 0 600 {self.height}" role="img" aria-labelledby="title desc">
<title id="title">{e(self.title)}</title><desc id="desc">{e(self.description)}</desc>
<rect width="600" height="{self.height}" fill="white"/>
<g font-family="-apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif">{''.join(self.parts)}</g></svg>\n'''

SOURCE_TITLES = {
    3:'ISP·ISMP', 6:'IT 경제성 분석', 7:'IT-ROI', 8:'BSC·IT-BSC',
    12:'데이터 마이닝', 18:'신경망 분석', 23:'SWOT', 24:'3C·4C',
    25:'MECE·LISS', 49:'공급망 관리', 53:'MES', 68:'SLA', 75:'ITSM',
    78:'BCP·BCM', 79:'ISO 22301', 80:'DRP', 81:'DR·BIA·DRaaS',
    82:'RTO·RPO', 83:'IT 거버넌스', 86:'ESG', 87:'IT 컴플라이언스',
    100:'앰비언트 컴퓨팅·커머스', 111:'공유경제', 118:'구독경제',
    121:'디지털 카르텔', 122:'다크패턴', 130:'지식재산권',
    131:'기술 가치 평가', 1251:'DRS', 1316:'BIA', 1782:'AX 2.0',
    3162:'SLO·에러버짓',
}

def source(topic, image=None, section='서브노트'):
    return {'label':'ITPE 지식관리 · '+SOURCE_TITLES[topic], 'url':f'https://itpe.co.kr/main/portal/selectPortalContent.do?topicId={topic}', 'section':section, 'image_number':image}

def cafe(article, label):
    return {'label':'ITPE 카페 · '+label,'url':f'https://cafe.naver.com/81th/{article}'}

def save(slug,d,recipe,read,sources,review='핵심 관계만 남긴 학습용 재구성. 원본 이미지를 전재하지 않음.'):
    DEST.mkdir(parents=True,exist_ok=True)
    (DEST/f'{slug}.svg').write_text(d.svg(),encoding='utf-8')
    MANIFEST[slug]={'title':d.title,'alt':d.description,'width':600,'height':d.height,'asset':f'/assets/subnotes/concepts/{slug}.svg','draw':recipe,'read':read,'sources':sources,'checked_at':'2026-11-22','adaptation':review}

def flow(title,desc,labels,footer='',feedback=False):
    # Up to six nodes: left-to-right on each row; the second row continues below.
    d=Drawing(title,desc,460 if len(labels)>3 else 290)
    n=len(labels); cols=3 if n in (3,5,6) else 2
    w=164 if cols==3 else 240;gap=26 if cols==3 else 64;x0=(600-cols*w-(cols-1)*gap)/2
    coords=[]
    for i,label in enumerate(labels):
        row=i//cols;col=i%cols
        if row%2:col=cols-1-col
        x=x0+col*(w+gap);y=50+row*172;coords.append((x,y));d.box(x,y,w,96,label,size=23)
    for i,((x,y),(nx,ny)) in enumerate(zip(coords,coords[1:])):
        if y==ny:
            d.arrow([(x+w if nx>x else x,y+48),(nx if nx>x else nx+w,ny+48)])
        else:d.arrow([(x+w/2,y+96),(nx+w/2,ny)])
    if feedback:
        x,y=coords[-1];fx,fy=coords[0]
        d.arrow([(x,y+48),(12,y+48),(12,22),(fx+w/2,22),(fx+w/2,fy)],dashed=True)
    if footer:d.text(300,d.height-40,footer,22,color=GREEN)
    return d

def cycle(title,desc,labels,center):
    d=Drawing(title,desc,440)
    coords=[(30,45),(340,45),(340,265),(30,265)]
    for (x,y),label in zip(coords,labels): d.box(x,y,230,100,label,size=23)
    d.arrow([(260,95),(340,95)]);d.arrow([(455,145),(455,265)])
    d.arrow([(340,315),(260,315)]);d.arrow([(145,265),(145,145)])
    d.text(300,209,center,23,color=GREEN,weight=650)
    return d

def hub(title,desc,labels,center,footer=''):
    d=Drawing(title,desc,440)
    coords=[(25,30),(335,30),(25,290),(335,290)]
    for (x,y),label in zip(coords,labels):d.box(x,y,240,94,label,size=23)
    d.box(195,175,210,90,center,fill='#e8f4ee',size=25)
    for x,y in coords[:len(labels)]:
        sx=x+120;sy=y+94 if y<175 else y
        d.arrow([(sx,sy),(sx,220),(195 if sx<300 else 405,220)])
    if footer:d.text(300,420,footer,21,color=GREEN)
    return d


def build():
    MANIFEST.clear()
    d=Drawing('BCM의 관리 범위와 계획의 포함관계','BCM의 지속적 관리 안에 BIA와 BCP가 있고, BCP 중 IT 복구 계획이 DRP다. DRP는 DRS와 인력·절차로 실행한다.',450)
    d.rect(25,25,550,390,SOFT);d.text(300,65,'BCM · 지속적인 연속성 관리',25,weight=700)
    d.box(55,95,490,65,'BIA · 핵심 업무와 복구 목표',fill='white');d.arrow([(300,160),(300,193)])
    d.rect(55,195,490,190,'white');d.text(300,232,'BCP · 사람·장소·업무의 지속 계획',24,weight=600)
    d.box(95,259,410,66,'DRP · IT 재해복구 계획');d.text(300,361,'실행 수단: DRS + 인력·절차',23,color=GREEN)
    save('bcm',d,'큰 관리 상자 → BIA → BCP 상자 → 안에 DRP → 아래 실행 수단.','상자는 관리 범위와 계획의 포함관계다. BCM은 관리 활동이고 BCMS는 이를 운영하는 경영시스템이다.',[source(78,1),cafe(242153,'BCMS·BCP·DRP 관계도')])

    d=flow('DRP의 발동·복구·검증 흐름','재해 발동과 연락 후 복구환경으로 전환하고 복구·업무 검증을 수행한다. 이후 안정화·원복·개선으로 이어진다.',['발동 판단\n비상 연락','DR 전환\n시스템 복구','업무 검증\n서비스 재개','안정화\n원복·개선'],footer='각 단계에 책임자·조건·점검 항목을 지정')
    save('drp',d,'네 상자를 지그재그로 잇고, 각 상자 아래 책임자·조건을 떠올린다.','서비스 재개 전 업무 검증이 필요하다. 원복은 주센터 안전성과 복귀 조건 확인 후 수행한다.',[source(80,4),cafe(242153,'BCP·DRP 답안')])

    d=Drawing('DRaaS의 복제와 재해 시 서비스 전환','고객 운영환경을 공급자의 클라우드 복구환경으로 복제한다. 재해 시 이용자를 복구환경으로 전환하고 검증하며, 안정화 후 원복한다.',430)
    d.box(25,60,220,120,'고객 운영환경\n응용·데이터');d.box(355,60,220,120,'공급자 클라우드\n복구 자원·사본')
    d.arrow([(245,120),(355,120)]);d.text(300,96,'복제',23)
    d.box(185,290,230,90,'서비스 이용자')
    d.arrow([(235,290),(135,245),(135,180)],dashed=True);d.text(100,270,'평상시',22)
    d.arrow([(365,290),(465,245),(465,180)]);d.text(487,270,'재해 시',22)
    d.text(300,415,'전환·검증·원복 시험과 책임 분담',23,color=GREEN)
    save('draas',d,'좌우에 고객·공급자, 아래 이용자 → 복제 화살표 → 재해 시 접속 경로.','복제 사본뿐 아니라 실제 서비스를 실행할 복구 자원과 전환 절차를 제공한다.',[source(81,2),source(1251,5)],'DRaaS 설명·운영형태 표를 바탕으로 서비스 관계도를 직접 설계함. 점선은 평상시 접속 경로.')

    d=cycle('IT 컴플라이언스의 요구·통제·증거 연결','외부 법규와 내부 정책을 식별하고 통제를 설계·운영한다. 증거로 준수 여부를 평가한 뒤 미비점을 시정한다.',['요구 식별\n법규·내부 정책','통제 설계·운영\n접근·보관·보호','증거 수집·평가\n로그·감사 기록','미비점 시정\n정책·통제 보완'],'준수 여부를 증명')
    save('it-compliance',d,'요구 → 통제 → 증거 → 시정, 네 상자를 순환으로 잇는다.','법규 이름을 나열하는 데서 끝내지 않고, 운영 통제와 준수 증거를 연결한다.',[source(87,2),source(87,4)])

    d=Drawing('기술 가치 평가의 세 접근법','평가대상과 목적을 정하고 수익·시장·비용 접근법으로 가치를 추정한다. 기술성·권리성·시장성·사업성과 가정을 함께 검토한다.',420)
    d.box(120,25,360,70,'평가 대상·목적·기준일')
    for x,label in [(25,'수익 접근\n미래 현금흐름'),(215,'시장 접근\n유사 거래 비교'),(405,'비용 접근\n재생산·대체 비용')]:
        d.box(x,165,170,105,label,size=22);d.arrow([(300,95),(300,130),(x+85,130),(x+85,165)])
        d.arrow([(x+85,270),(x+85,310),(300,310),(300,340)])
    d.box(145,340,310,60,'가치 추정 + 가정·한계',fill='#e8f4ee',size=23)
    save('technology-valuation',d,'위에 평가 대상, 가운데 세 방법, 아래 가치 추정 → 가지를 합친다.','세 접근법은 자료와 목적에 맞게 선택·교차 검토한다. 세 결과를 무조건 단순 평균하지 않는다.',[source(131,2),source(131,4)])

    d=Drawing('BSC와 IT-BSC의 전략 가설','학습과 성장·내부 프로세스·고객·재무의 인과 가설에 IT-BSC의 미래 지향·운영 탁월성·고객 지향·회사 기여를 대응시킨다.',460)
    d.text(170,35,'BSC',25,weight=700);d.text(440,35,'IT-BSC',25,weight=700)
    for y,left,right in [(65,'재무','회사 기여'),(165,'고객','고객 지향'),(265,'내부 프로세스','운영 탁월성'),(365,'학습과 성장','미래 지향')]:
        d.box(35,y,245,65,left,size=24);d.box(325,y,245,65,right,size=24)
        d.line(280,y+32,325,y+32,dash=True)
        if y>65:d.arrow([(157,y),(157,y-35)]);d.arrow([(447,y),(447,y-35)])
    save('bsc-it-bsc',d,'좌우 네 칸을 쌓고 아래에서 위로 화살표 → 같은 높이끼리 점선 대응.','아래 역량이 위 성과에 기여한다는 전략 가설이다. 실제 인과관계와 KPI는 검증해야 한다.',[source(8,3)],'BSC 구성도에 기존 노트의 IT-BSC 관점을 대응시켜 재구성. 점선은 기능적 대응이며 동일 개념이라는 뜻은 아님.')

    d=Drawing('SWOT의 내부·외부 교차행렬','열은 내부 강점 S와 약점 W, 행은 외부 기회 O와 위협 T다. 교차점에서 SO·WO·ST·WT 전략을 도출한다.',420)
    d.text(310,35,'내부 요인',24,color=GREEN);d.text(238,89,'S · 강점',25,weight=700);d.text(455,89,'W · 약점',25,weight=700)
    d.text(68,190,'O\n기회',23);d.text(68,320,'T\n위협',23)
    for x,y,lines in [(130,120,'SO\n강점으로 기회 활용'),(350,120,'WO\n약점 보완·기회 활용'),(130,255,'ST\n강점으로 위협 대응'),(350,255,'WT\n약점·위협 최소화')]:d.box(x,y,215,125,lines,size=22)
    save('swot',d,'가로 S·W, 세로 O·T → 네 교차칸에 전략을 한 줄씩 쓴다.','내부 상태 S·W와 외부 환경 O·T를 구분하고, 목록을 조합해 전략으로 연결한다.',[source(23,1)])

    d=Drawing('공유경제의 삼자 거래 구조','제공자의 유휴자원을 플랫폼이 이용자 수요와 연결한다. 대가와 신뢰·평판이 거래를 뒷받침한다.',390)
    d.box(20,120,170,100,'제공자\n유휴자원');d.box(215,120,170,100,'플랫폼\n매칭·신뢰');d.box(410,120,170,100,'이용자\n이용 수요')
    d.arrow([(190,170),(215,170)],both=True);d.arrow([(385,170),(410,170)],both=True)
    d.text(300,63,'소유권보다 자원의 이용을 연결',25,weight=650)
    d.arrow([(105,220),(105,290),(495,290),(495,220)],both=True,dashed=True)
    d.text(300,329,'이용 대가 · 후기·평판',24,color=GREEN)
    save('sharing-economy',d,'제공자·플랫폼·이용자 세 칸 → 매칭 연결 → 아래 대가·후기 경로.','플랫폼이 반드시 자산을 소유하는 것은 아니다. 이용 조건·책임·신뢰 장치가 중요하다.',[source(111,4)])

    d=cycle('구독경제의 반복 가치 교환','고객이 정기 대가를 지급하면 플랫폼이 이용권·배송·렌털 등 서비스를 제공한다. 이용·해지 데이터를 분석하고 가치를 개선해 재구독으로 연결한다.',['고객·정기 대가\n가입·갱신','플랫폼·서비스\n이용권·배송·렌털','이용·해지 데이터\n유지율·이탈률','가치 개선\n개인화·품질'],'반복되는 가치 교환')
    save('subscription-economy',d,'고객 → 서비스 → 데이터 → 개선을 순환으로 그린다.','정기 결제만으로 성공하지 않는다. 이용 가치가 유지돼야 갱신과 반복매출로 이어진다.',[source(118,4)])

    d=flow('앰비언트 컴퓨팅과 커머스의 연결','센싱·연결로 맥락 데이터를 모으고 분석·판단을 통해 자연스러운 서비스를 제공한다. 상거래에 적용하면 주문·결제 등 앰비언트 커머스가 된다.',['센싱·연결\n상황 데이터','분석·판단\n맥락 인식','서비스 제공\n상거래 응용'],footer='컴퓨팅 = 기반 · 커머스 = 상거래 응용')
    save('ambient-commerce-computing',d,'센싱 → 맥락 판단 → 서비스 세 칸, 마지막에 상거래 응용을 표시한다.','앰비언트 컴퓨팅 전체를 무인결제로 한정하지 않는다. 개인정보·동의·오류 대응도 필요하다.',[source(100,1),source(100,3)])

    d=cycle('ITSM에서 SLO와 에러버짓을 쓰는 위치','고객 요구에 따라 서비스를 운영하고 SLI를 측정한다. SLO와 비교하고 에러버짓 잔여량을 바탕으로 변경과 신뢰성 개선을 조정한다.',['고객 요구\n서비스 설계','서비스 운영\n사고·문제·변경','SLI 측정\nSLO 대비 점검','변경·개선 판단\n에러버짓 확인'],'고객 가치 · 신뢰성')
    save('itsm-slo-error-budget',d,'서비스 운영 순환 네 칸 → 점검에 SLI·SLO, 판단에 에러버짓을 적는다.','에러버짓은 SLO가 허용하는 불완전성의 범위다. SLO 99.9%이면 허용 실패 비율은 0.1%다.',[source(75,4),source(3162,3)])

    d=Drawing('SLA의 약속·측정·미달 조치','고객과 제공자가 서비스 범위·목표·측정 기준·책임·미달 조치를 합의한다. 실제 측정 결과를 보고하고 합의 기준에 따라 개선한다.',410)
    d.box(25,25,210,70,'고객');d.box(365,25,210,70,'서비스 제공자');d.arrow([(235,60),(365,60)],both=True);d.text(300,111,'합의',23)
    d.box(60,150,480,100,'SLA\n범위·목표·측정·책임·미달 조치')
    d.arrow([(300,250),(300,290)]);d.box(60,290,480,90,'측정·보고 → 기준 대비 판단 → 조치',size=23)
    save('sla',d,'고객·제공자 → 가운데 SLA → 아래 측정·판단·조치.','SLO는 목표치, SLA는 목표뿐 아니라 측정 방법과 책임·미달 조치를 포함한 합의다.',[source(68,2),source(68,3)])

    d=cycle('ISO 22301의 BCMS 운영 순환','ISO 22301의 조직 상황·리더십·기획·지원은 Plan, 운영은 Do, 성과평가는 Check, 개선은 Act로 연결된다.',['P · 계획\n상황·리더십·기획·지원','D · 운영\nBIA·전략·계획·훈련','C · 성과평가\n측정·내부감사·검토','A · 개선\n시정조치·지속 개선'],'BCMS · 업무연속성')
    save('iso-22301',d,'네 칸을 원형으로 잇고 P·D·C·A와 실제 활동을 함께 쓴다.','인증 취득으로 끝나는 구조가 아니다. 운영·평가·개선을 반복하는 경영시스템이다.',[source(79,2),source(79,4)])

    d=Drawing('DRS의 주센터·복구센터 이중 구조','주센터의 응용·데이터·네트워크를 복구센터에 준비하고 복제한다. 재해 시 이용 경로를 전환한다. 유형별 자원 준비 수준은 서로 다르다.',410)
    d.box(30,50,220,190,'주센터\n응용·데이터\n네트워크·스토리지');d.box(350,50,220,190,'복구센터\n응용·데이터\n네트워크·스토리지')
    d.arrow([(250,145),(350,145)]);d.text(300,120,'복제',23)
    d.box(185,310,230,65,'이용 경로 전환');d.arrow([(140,240),(140,342),(185,342)],dashed=True);d.arrow([(415,342),(460,342),(460,240)])
    d.text(300,400,'준비 수준에 따라 Mirror · Hot · Warm · Cold',21,color=GREEN)
    save('drs',d,'좌우 센터 상자 → 복제 화살표 → 아래 서비스 전환 경로.','복구센터가 존재하는 것과 실제 복구 가능한 것은 다르다. 복제·의존성·전환 시험을 확인한다.',[source(1251,4),cafe(239556,'DRS 구성도')],'카페 센터 구성도와 지식관리 DRS 유형을 대조해 단순화. DWDM은 특정 구현 예이므로 필수 구성처럼 표시하지 않음.')

    for slug,focus in [('rto','RTO'),('rpo','RPO')]:
        desc='장애 전 복구 가능한 데이터 시점부터 장애까지는 데이터 손실 구간, 장애부터 서비스 복구까지는 복구 소요시간이다. RPO와 RTO는 각각 이 구간에 대한 목표다.'
        d=Drawing(f'{focus}를 구분하는 공통 시간축',desc,380)
        d.text(300,35,'장애 전 데이터 · 장애 후 복구',25,weight=700)
        d.arrow([(40,175),(565,175)])
        for x,label in [(95,'복구 가능한\n데이터 시점'),(300,'장애 발생'),(510,'서비스 복구')]:
            d.line(x,145,x,195);d.text(x,88,label,22)
        d.arrow([(95,235),(294,235)],both=True);d.arrow([(306,235),(510,235)],both=True)
        d.text(197,275,'데이터 손실 구간',22,color=BLUE,weight=650 if focus=='RPO' else 500)
        d.text(405,275,'복구 소요시간',22,color=BLUE,weight=650 if focus=='RTO' else 500)
        d.box(45 if focus=='RPO' else 315,305,240,55,focus+' · 허용 목표',fill='#e8f4ee',size=24)
        save(slug,d,'시간축 → 데이터 시점·장애·복구 세 점 → 장애 좌우에 두 구간.','그림의 구간은 실제 결과를 뜻하며 RPO·RTO는 허용 목표다. 실제 손실·복구시간이 목표 이내인지 비교한다.',[source(82,5),source(82,14)],'원본의 시간축을 대조해 RPO는 장애 전 데이터 손실, RTO는 장애 후 복구 소요시간의 목표로 구분함.')

    d=flow('BIA가 복구 우선순위와 목표로 이어지는 흐름','업무와 의존 자원을 식별하고 중단 기간별 영향을 분석한다. 이를 바탕으로 핵심 업무·복구 우선순위·복구 목표를 정해 전략과 계획에 반영한다.',['업무·의존성\n식별','중단 영향\n시간별 분석','핵심 업무\n우선순위','복구 목표\nRTO·RPO'],footer='중단 영향이 큰 업무부터 합의한 수준으로')
    save('bia',d,'업무 → 중단 영향 → 우선순위 → 목표 네 칸으로 연결한다.','단순한 장비 중요도 평가가 아니다. 업무 중단이 고객·재무·법규 등에 미치는 영향을 본다.',[source(1316,3),source(1251,3)])

    d=flow('ISP의 5단계와 통합 이행계획','환경분석·현황분석·정보화 비전 및 전략 수립·목표모델 설계·통합 이행계획 순으로 전사 정보화 방향과 실행을 연결한다.',['환경분석','현황분석\nAS-IS','비전·전략\n수립','목표모델\nTO-BE','통합 이행계획\n과제·예산'],footer='전사 정보화 방향과 과제의 연결')
    save('isp',d,'세 칸 뒤 아래로 내려가 두 칸 → 환·현·비·목·통을 적는다.','지식관리 구축절차의 핵심 단계를 유지했다. 실제 산출물과 검토 항목은 가이드·사업 조건에 맞춘다.',[source(3,3)])

    d=flow('ISMP의 요건 상세화와 발주 준비','프로젝트 착수·정보시스템 방향성 수립·업무와 정보기술 요건 분석·구조 및 요건 정의·구축사업 이행방안 수립으로 발주 가능한 요구사항을 도출한다.',['착수·참여자\n결정','정보시스템\n방향성 수립','업무·IT\n요건 분석','구조·요건\n정의','구축 이행방안\n예산·RFP'],footer='특정 정보시스템 구축을 위한 요건 상세화')
    save('ismp',d,'세 칸에서 두 칸으로 이어지는 흐름 → 마지막에 예산·RFP를 표시한다.','ISP의 전사 방향과 연결하되, 특정 사업의 기능·비기능·기술 요건과 발주 준비에 초점을 둔다.',[source(3,20),source(3,22)])

    d=Drawing('ESG의 세 관점과 IT의 기여','환경 E·사회 S·지배구조 G는 지속가능 경영의 세 관점이다. IT는 각각 에너지·탄소 관리, 접근성·개인정보 보호, 통제·책임·공시를 지원한다.',410)
    for x,label,detail in [(20,'E · 환경','에너지·탄소\n자원 효율'),(215,'S · 사회','접근성·안전\n개인정보 보호'),(410,'G · 지배구조','책임·윤리\n통제·공시')]:
        d.box(x,35,170,70,label,size=25);d.box(x,165,170,100,detail,size=22);d.arrow([(x+85,105),(x+85,165)])
        d.arrow([(x+85,265),(x+85,305),(300,305),(300,340)])
    d.box(100,340,400,55,'지속가능 경영 · 지표와 증거',fill='#e8f4ee',size=23)
    save('esg',d,'E·S·G 세 기둥 → 각 IT 사례 → 아래 지속가능 경영으로 합친다.','환경 활동만으로 ESG 전체를 설명하지 않는다. 사회·지배구조의 목표와 측정 근거도 함께 본다.',[source(86,2),source(86,3),source(86,4)])

    d=Drawing('IT 거버넌스의 방향·책임과 실행의 연결','경영 목표와 이해관계자 요구를 바탕으로 거버넌스가 평가·지시·모니터링한다. 관리는 계획·구축·운영을 실행하고 성과와 위험을 보고한다.',430)
    d.box(75,20,450,65,'경영 목표 · 이해관계자 요구');d.arrow([(300,85),(300,130)])
    d.box(75,130,450,95,'IT 거버넌스\n평가 · 지시 · 모니터링')
    d.box(75,300,450,95,'IT 관리\n계획 · 구축 · 운영')
    d.arrow([(195,225),(195,300)]);d.text(118,270,'방향·책임',21)
    d.arrow([(405,300),(405,225)]);d.text(481,270,'성과·위험',21)
    save('it-governance',d,'위 경영 목표 → 거버넌스 → 관리, 가운데 왕복 화살표에 방향·성과.','거버넌스가 방향·책임·감독을 정하고, 관리가 실행과 운영을 수행한다.',[source(83,3),source(83,4)])

    d=Drawing('IT 투자의 사전·중간·사후 평가','투자 전 경제성을 평가하고 집행 중 비용·위험·진행을 점검하며 운영 후 실제 성과와 편익을 평가한다. 결과를 차기 투자에 반영한다.',390)
    for x,label,detail in [(20,'사전 평가','NPV·IRR\nPP·BCR'),(215,'중간 평가','진행·비용\n위험 점검'),(410,'사후 평가','실제 편익\nROI·성과 지표')]:
        d.box(x,60,170,85,label,size=24);d.text(x+85,208,detail,22)
    d.arrow([(190,102),(215,102)]);d.arrow([(385,102),(410,102)])
    d.arrow([(495,260),(495,310),(105,310),(105,260)],dashed=True);d.text(300,353,'평가 결과를 차기 투자에 환류',23,color=GREEN)
    save('it-investment',d,'사전·중간·사후 세 칸 → 아래에 지표 → 사후에서 사전으로 환류.','평가 시점과 지표의 용도를 구분한다. 경제성 수치만으로 전략 적합성·위험 평가를 대신하지 않는다.',[source(6,1),source(6,2),source(7,3)])

    d=hub('3C에 환경을 더한 수업의 4C','고객·경쟁사·자사의 세 관점이 3C이며 수업의 4C는 환경을 추가한다. 분석 결과를 가치 제안과 차별화에 연결한다.',['고객\nCustomer','경쟁사\nCompetitor','자사\nCompany','환경 · 추가 C\nCircumstance'],'가치·차별화',footer='3C = 고객·경쟁사·자사 · 4C = 환경 추가')
    save('three-four-c',d,'가운데 가치·차별화 → 주변에 고객·경쟁사·자사 → 마지막 환경을 더한다.','이번 수업에서 사용하는 4C다. 다른 맥락의 4C 모델과 용어를 섞지 않는다.',[source(24,1),source(24,2)])

    d=Drawing('MECE의 전체 분류와 수업상 LISS의 선택','같은 전체 범위를 A·B·C·D로 겹침과 누락 없이 나누면 MECE다. 수업상 LISS는 중요한 영역을 골라 집중하는 설명이며 수학적 정의와 구분한다.',370)
    d.text(300,35,'같은 전체 범위: A + B + C + D',24,weight=650)
    d.text(84,127,'MECE',24,weight=700);d.text(84,258,'수업상\nLISS',23,weight=700)
    for i,label in enumerate('ABCD'):
        d.box(180+i*95,80,95,85,label,fill=SOFT,size=28)
        d.box(180+i*95,220,95,85,label,fill='#e8f4ee' if i in (0,2) else 'white',size=28)
    d.text(365,196,'중복 없이 · 빠짐없이',22,color=GREEN)
    d.text(365,344,'선택 근거와 제외 영역을 명시',22,color=GREEN)
    save('mece-liss',d,'같은 네 칸을 두 줄로 그린다 → 위 전체, 아래 선택한 칸만 강조한다.','아래는 수업의 전략적 선택 설명이다. 수학의 독립 생성집합을 불완전한 범위라는 뜻으로 사용하지 않는다.',[source(25,1),source(25,2)])

    d=Drawing('SCM의 제품·정보 흐름과 계획·실행·통합','공급자·제조·유통·고객으로 제품이 이동하고 수요·재고 정보는 반대 방향으로 공유된다. SCP·SCE·SCI가 전체 공급망을 계획·실행·통합한다.',370)
    labels=['공급자','제조','유통','고객']
    for i,label in enumerate(labels):d.box(20+i*145,80,125,80,label,size=25)
    for i in range(3):d.arrow([(145+i*145,110),(165+i*145,110)])
    d.text(300,43,'제품·물류 흐름',24,color=GREEN)
    d.arrow([(517,185),(517,220),(82,220),(82,185)]);d.text(300,258,'수요·재고·주문 정보 공유',23)
    d.box(20,295,560,55,'SCP 계획 · SCE 실행 · SCI 통합',size=24)
    save('scm',d,'공급자 → 제조 → 유통 → 고객, 아래 반대 방향 정보 화살표와 세 기능.','제품과 정보의 방향을 구분한다. 수요 정보를 함께 보지 못하면 상류로 주문 변동이 증폭될 수 있다.',[source(49,3),source(49,4)])

    d=Drawing('MES가 계획과 현장 실행을 연결하는 위치','상위 생산계획을 MES가 작업지시와 실행 관리로 구체화하고, 설비·현장의 생산실적과 품질 데이터를 모아 상위 계획에 보고한다.',440)
    d.box(155,25,290,70,'상위 생산계획');d.box(75,175,450,95,'MES\n작업지시·실적·품질·추적');d.box(155,350,290,65,'설비·생산 현장')
    d.arrow([(215,95),(215,175)]);d.text(117,140,'계획',23)
    d.arrow([(385,175),(385,95)]);d.text(486,140,'실적 보고',23)
    d.arrow([(215,270),(215,350)]);d.text(117,318,'작업지시',23)
    d.arrow([(385,350),(385,270)]);d.text(486,318,'현장 데이터',23)
    save('mes',d,'계획·MES·현장 세 층 → 왼쪽은 아래 지시, 오른쪽은 위 실적.','MES는 현장 실행을 관리한다. 장기 계획이나 설비 제어 각각과 범위를 구분한다.',[source(53,2)])

    d=Drawing('데이터 마이닝의 발견과 예측','데이터에서 패턴을 추출하는 데이터 마이닝은 예측과 기술·발견으로 나눠 볼 수 있다. 예측에는 분류·회귀, 발견에는 군집·연관규칙이 있다.',390)
    d.box(160,20,280,70,'데이터 마이닝')
    d.box(25,170,245,80,'예측',fill=SOFT);d.box(330,170,245,80,'기술·발견',fill='#e8f4ee')
    d.arrow([(300,90),(300,125),(147,125),(147,170)]);d.arrow([(300,125),(452,125),(452,170)])
    d.text(147,305,'분류 · 회귀\n미래 값·범주 예측',22);d.text(452,305,'군집 · 연관규칙\n숨은 구조·관계 발견',22)
    save('data-mining',d,'위 데이터 마이닝 → 예측·발견 두 가지 → 각 대표 기법 두 개.','군집은 비슷한 데이터를 묶고 분류는 정해진 범주를 예측한다. 마이닝 결과를 인과관계로 단정하지 않는다.',[source(12,6),source(12,8)],'원본 6번의 예측·기술 분류 사용. 5번의 K-means 예측 모델 배치는 채택하지 않고 군집으로 정리함.')

    d=Drawing('신경망의 순전파와 학습','입력층에서 은닉층을 거쳐 출력층으로 계산한다. 지도학습에서는 출력과 정답의 오차를 계산하고 역전파와 최적화로 가중치를 갱신한다.',410)
    for x,label in [(90,'입력층'),(300,'은닉층'),(510,'출력층')]:d.text(x,40,label,24,weight=650)
    for a in [105,185,265]:
        for b in [105,185,265]:d.line(110,a,280,b)
    for a in [105,185,265]:
        for b in [145,225]:d.line(320,a,490,b)
    for x,ys in [(90,[105,185,265]),(300,[105,185,265]),(510,[145,225])]:
        for y in ys:d.circle(x,y,20,fill='#e8f4ee' if x==510 else SOFT)
    d.arrow([(120,305),(490,305)]);d.text(300,342,'순전파 · 출력 계산',23)
    d.arrow([(490,374),(120,374)],dashed=True);d.text(300,405,'지도학습: 오차 역전파 · 가중치 갱신',21,color=GREEN)
    save('neural-network',d,'세 층에 동그라미 → 층 사이 연결 → 아래 순전파·학습 방향.','연결선은 가중치를 가진다. 모든 신경망 학습이 정답을 쓰는 것은 아니므로 역전파 설명은 지도학습 예다.',[source(18,3),source(18,4)])

    d=flow('다크패턴이 선택을 왜곡하는 경로','소비자의 선택 화면에 정보 은폐·오도·압박·방해를 넣으면 이해와 선택이 왜곡돼 원치 않는 결제나 해지 실패로 이어질 수 있다.',['소비자\n선택 화면','숨김·오도\n압박·방해','선택 왜곡\n원치 않는 결과'],footer='명확한 정보 · 대칭적인 선택 · 쉬운 취소')
    save('dark-patterns',d,'화면 → 조작 요소 → 왜곡된 결과, 아래 대응 원칙 세 개.','모든 설득 디자인이 다크패턴은 아니다. 충분한 정보와 자유로운 선택을 방해하는지 확인한다.',[source(122,2),source(122,3)])

    d=Drawing('디지털 카르텔의 가격 상호작용','여러 기업의 가격결정 알고리즘이 가격 정보를 관찰하고 반응한다. 공통 알고리즘·신호·학습 방식 등이 경쟁 제한 위험을 만들 수 있으나 같은 가격만으로 담합을 단정하지 않는다.',390)
    d.box(30,65,220,110,'기업 A\n가격 알고리즘');d.box(350,65,220,110,'기업 B\n가격 알고리즘')
    d.arrow([(250,120),(350,120)],both=True);d.text(300,43,'가격 정보 관찰·반응',23,weight=600)
    d.arrow([(140,175),(140,250),(300,250),(300,285)]);d.arrow([(460,175),(460,250),(300,250)])
    d.box(85,285,430,75,'가격 조정 · 경쟁 제한 위험',fill='#e8f4ee',size=24)
    save('digital-cartel',d,'기업별 알고리즘 두 칸 → 관찰·반응 → 아래 경쟁 제한 위험.','그림은 위험의 개념 구조다. 가격 일치만으로 합의·위법성을 확정하지 않으며 유형별 증거를 확인한다.',[source(121,2),source(121,3)])

    d=Drawing('지식재산권을 보호 대상별로 나눈 구조','지식재산권은 산업재산권·저작권·신지식재산의 영역으로 나누어 학습한다. 기술·표장·표현·영업비밀 등 보호 대상이 다르고 일부 영역은 중첩될 수 있다.',410)
    d.box(165,20,270,70,'지식재산권')
    for x,label,detail in [(20,'산업재산권','특허·실용신안\n상표·디자인'),(215,'저작권','창작적 표현\n문학·예술·SW'),(410,'신지식재산','영업비밀·DB 등\n여러 제도와 연결')]:
        d.box(x,165,170,75,label,size=23);d.text(x+85,295,detail,21)
        d.arrow([(300,90),(300,125),(x+85,125),(x+85,165)])
    d.text(300,383,'보호 대상 · 요건 · 권리 범위를 구분',23,color=GREEN)
    save('intellectual-property',d,'큰 권리 상자 → 세 가지 → 각 보호 대상 예시 두 개.','학습용 분류이며 모든 법적 권리가 서로 배타적인 것은 아니다. 아이디어와 구체적 표현의 보호도 구분한다.',[source(130,1),source(130,2)])

    d=Drawing('AX와 수업상 AX 2.0의 전환 구조','AX는 AI를 중심으로 업무와 의사결정을 재설계하는 조직 전환이다. 수업의 AX 2.0은 생성 보조를 넘어 계획·실행·협업하는 AI를 강조하며 사람의 감독과 평가를 함께 둔다.',430)
    d.box(35,30,530,65,'AX · 업무·조직·의사결정 재설계')
    d.box(35,150,235,115,'AI 생성·분석 보조\n사람이 실행');d.box(330,150,235,115,'계획·도구 실행\n협업·현장 연결')
    d.arrow([(270,207),(330,207)]);d.text(300,128,'수업상 확장',22)
    d.text(447,304,'AX 2.0의 강조점',22,color=GREEN,weight=650)
    d.box(35,350,530,60,'공통 기반: 데이터·평가·권한·사람의 감독',size=23)
    save('ax-transformation',d,'전체 AX 상자 → 보조에서 실행·협업으로 → 아래 공통 감독 기반.','AX 2.0은 이 수업과 지식관리의 설명 틀이다. 보편적으로 확정된 표준 단계·버전으로 쓰지 않는다.',[source(1782,2),source(1782,None,'키워드(암기법)')])

    d=cycle('서브노트를 만드는 학습 순환','자료에서 정의·관계·키워드를 확인하고 내 언어와 그림으로 정리한다. 자료를 가리고 설명·손그림을 재현한 뒤 틀린 부분을 보완한다.',['자료 확인\n교재·카페·지식관리','내 언어로 정리\n정의·개념도·키워드','가리고 재현\n설명·손그림·답안','오답 보완\n누락·관계 수정'],'작게 정리 · 반복 확인')
    save('writing-guide',d,'자료 → 정리 → 재현 → 보완의 네 칸을 반복으로 연결한다.','카페 작성 원칙을 이 노트의 운영 방식으로 재구성한 그림이며 카페 원본 도식은 아니다.',[cafe(78220,'서브노트 작성방법론'),cafe(106133,'서브노트 작성 기본 사항')])

    d=cycle('읽기에서 다른 날 재현까지','읽고 구조를 이해한 후 가리고 설명·손그림을 재현한다. 정답과 비교해 교정하고 다른 날 다시 회상·적용한다.',['읽고 이해\n핵심 관계 확인','가리고 꺼내기\n설명·손그림','비교·교정\n빠진 관계 보완','다른 날 재현\n비교·새 상황 적용'],'막힌 지점만 다시 보완')
    save('mastery-method',d,'이해 → 회상 → 교정 → 다른 날 재현을 네 칸으로 잇는다.','기존 복습 가이드와 카페의 개념도 연습 원칙을 시각화했다. 정해진 간격만으로 완벽한 기억을 보장하지 않는다.',[cafe(106133,'개념도 손그림 연습'),{'label':'기존 복습 가이드의 근거 · 인출 연습 연구','url':'https://doi.org/10.1111/j.1467-9280.2006.01693.x'}])

    (ROOT/'diagrams.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Rendered {len(MANIFEST)} concept diagrams in {DEST}')

if __name__=='__main__':build()
