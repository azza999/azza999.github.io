---
layout:		post
title:		"[LINUX/UNIX] 리눅스 입출력 파일로 장난치기"
subtitle:	"hellooow?"
categories:	os
tags:		tty pts 입/출력 리눅스 유닉스
comments:	true
hard_wrap: true

---

# 다른 터미널로 러브레터 보내기


## 서론 / 사전지식

### unix/linux의 입출력
---

linux를 배우다보면, "linux는 입출력을 파일로 한다." 라는 말을 한번쯤 들어보았을 것이다. 하지만 난 정말 무슨 말인지 이해하지 못했다. 난 분명 키보드로 입력하고 모니터 화면과 스피커로 출력을 받고 있는데, 도대체 내가 언제 파일을 생성하고 파일을 받고있다는 것일까?
<br>
<br>

### /dev의 정체
---

처음 dev 디렉터리를 만났을 때는, 안드로이드의 개발자 도구나 각종 에디터들의 개발자의 편의를 위해 뭔가 도구를 넣어놨나 하는 생각을 했었다. 하지만 dev의 뜻은 'developer'가 아닌 'device'이다. 뭐 그렇다 치고, 이 안에는 어떤 파일들이 있을까?

![block 단위]({{ site.url }}/assets/img/2021-01-25/disk.png)
<p style="opacity: 0.5; text-align: center;">블록 단위 입출력</p>

![character 단위]({{ site.url }}/assets/img/2021-01-25/tty.png)
<p style="opacity: 0.5; text-align: center;">캐릭터 단위 입출력</p>

ls -l로 디렉터리를 조사하면 디렉터리, 파일을 표시하는 맨 앞자리에 b, c와 같이 처음보는 친구들이 있다. 여기서 b와 c는 block과 character이다. 각각 블록 단위 입출력, 캐릭터(한글자) 단위 입출력을 뜻한다. 주로 저장장치(sba, sbc 등등)같은 할당 단위 크기가 있는 친구들이 블록 단위 입출력이고, tty, pts 등과 같은 주로 터미널 터미널 등 한글자씩 입/출력되는 친구들이 캐릭터 단위 입출력이다.
<br>
<br>

### tty, pts
---

간략하게 tty, pts에 대해 알아보자. tty, pts 모두 터미널이고, 해당 파일로 입출력을 하는 것은 동일하므로 이해하기 쉽고 간단하게 요약해서 설명하겠다.

tty는 물리적인(본체에 직접 연결된) 터미널을 뜻한다. 터미널에서 ctrl + alt + [f1 \~ f6]을 통해서 각각의 tty를 넘나들 수 있다.

![pts]({{ site.url }}/assets/img/2021-01-25/pts.png)
<p style="opacity: 0.5; text-align: center;">pts 가상 터미널</p>

pts는 가상 터미널을 뜻한다. xwindow 터미널을 생성하거나 ssh같은 원격 접속 터미널을 생성할 때마다 하나씩 pts/n의 입출력 파일이 늘어나는 것을 볼 수 있다.

<br>
<br>

## pts로 출력 리다이렉트...?
---

linux 쉘 스크립트를 공부하다 보니 보기 싫은 에러 메시지를 null 쉘로 돌리거나 특정 출력을 파일로 리다이렉트하여 저장할 일이 많아졌다. 그러다 문득 출력을 파일이나 쉘이 아니라 우리가 쓰는 pts, tty 쉘로 한다면 어떨까 생각이 들었다... 호기심에 내가 현재 쓰고있는 쉘을 확인한 뒤, 현재 쉘로 출력 리다이렉트를 해 보았다.

![hello]({{ site.url }}/assets/img/2021-01-25/hello.png)
<p style="opacity: 0.5; text-align: center;">hello!</p>

예상대로 출력되었다. ls나 shutdown같은 명령어도 리다이렉트 해보았지만 다행히 해당 터미널에서 명령이 실행되지는 않는 것 같다. 그렇다면, 다른 유저의 쉘은 어떨까?

![denined]({{ site.url }}/assets/img/2021-01-25/denined.png)
<p style="opacity: 0.5; text-align: center;">Permission denined!</p>

아쉽게도(다행히도) 권한이 없는 계정에는 출력 리다이렉트를 할 수 없었다. 그래도 같은 계정을 사용하는 다른 사람에게는 조용히, 흔적도 남지 않는 터미널로의 출력 리다이렉트로 오늘 점심을 뭐 먹을지 상의해 볼 수 있을 것 같다.

![chicken]({{ site.url }}/assets/img/2021-01-25/chicken.png)
<p style="opacity: 0.5; text-align: center;">오늘 점심은 치킨이닭!</p>