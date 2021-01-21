---
layout:		post
title:		"[Python] 키보드 입력을 통한 간단한 선택 구현"
subtitle:	"언제까지 숫자 입력으로 선택할래?"
categories:	dev
tags:		diary
comments:	true
hard_wrap: true

---

# 1. 가위 / 2. 바위 / 3. 보

## 가장 간단한 입력법
---

> print('1. 가위')  
> print('2. 가위')  
> print('3. 가위')  
> userPosition = read("당신의 선택은?")  

처음 코딩을 배울 때 다들 한번쯤 써본 멘트일 것이다. 비슷한 방식의 어떤 식으로든. 지금도 친구들에게 코딩을 가르쳐 주거나 테스트 알고리즘을 만들 때 귀찮으면 이렇게 처리하곤 한다. 하지만 이 방법에는 작은 문제들이 있다.

이런 입력 폼을 보면 그냥 왠지모르게 4가 눌러보고 싶어진다. 게임을 할 때 맵 밖에 나가보고 싶거나 괜히 레이싱 게임에서 가만히 멈춰있어 보는 것처럼 말이다. 긴 설명 필요없이 뭔가 구리다. 없어보인다. 그래서 간단하지만 있어보이는 선택 폼을 만드는 법을 알아봤다.
<br>
<br>

## 키보드로 선택하기
---

![BIOS 선택창]({{ site.url }}/assets/img/2021-01-21/bios.png)
<p style="opacity: 0.5; text-align: center;">바이오스에서의 옵션 선택창</p>

요즘 자주 보던 창이라 문득 생각났다. 바이오스에서는 옵션을 주고 키보드로 선택하게 한다. 고전적이지만 마우스가 필요 없으면서도 있어보이고 찰진 방법이다. 파이썬에서 키보드 처리법을 알아보고 간단하게 구현해보자.
<br>
<br>

## 키보드 입력 감지
---

<pre>
	<code>
import keyboard
import time

while 1:
	if keyboard.is_pressed(80):
		print('아래쪽 방향키 입력')
		time.sleep(0.1)

	if keyboard.is_pressed(72):
		print('위쪽 방향키 입력')
		time.sleep(0.1)

	if keyboard.is_pressed('enter'):
		print('엔터 키 입력')
		time.sleep(0.1)

	</code>
</pre>

간단하게 구현한 모습이다. 기본적으로 keyboard 모듈이 필요하고, 입력을 한번씩 받기 위해서 선택적으로 time 모듈이 필요하다.

while문을 사용한 것은 keyboard.is_pressed 메서드는 코드가 해당 부분을 지나갈 그 '찰나'의 순간에 키보드가 눌려있는지를 감지하기 때문에 반복문을 걸어주어 입력을 계속 기다리는 것이다. 만약 입력을 받고 해당 값을 리턴해야 한다면 return이나 break등으로 값을 반환할 수 있다.

time.sleep()메서드를 사용한 이유는 while문 안에서 정지없이 계속 감지를 하다보니 정말 짧게 눌러도 while문이 적게는 2~3번, 약간만 길게 눌러도 10~20번은 감지해 버리기 때문에, 키 입력이 있으면 즉시 무한루프를 잠시 정지함으로써 입력을 한번씩 받기 위해서 이다.
<br>
<br>


## 실 사용

우리가 원하는 것은 어떤 지점에서 몇가지의 입력 중 하나를 선택해서 그 결과를 사용하는 것이다. 간단하게 세가지 경우에서 한가지를 선택하는 코드이다.

<pre>
	<code>
import time
import os
import keyboard



def selectOne(value = 1):
	os.system('cls')
	printOptions(value)
	while 1:
		if keyboard.is_pressed(72):
			value -= 1
			if value < 1:
				value = 3
			os.system('cls')
			printOptions(value)
			time.sleep(0.1)

		if keyboard.is_pressed(80):
			value += 1
			if value > 3:
				value = 1
			os.system('cls')
			printOptions(value)
			time.sleep(0.1)

		if keyboard.is_pressed('enter'):
			return value
			time.sleep(0.1)

def printOptions(selected):
	if selected == 1:
		printWithBg("1번 항목", "black", "bg_white")
	else:
		printWithBg("1번 항목", "white", "bg_black")

	if selected == 2:
		printWithBg("2번 항목", "black", "bg_white")
	else:
		printWithBg("2번 항목", "white", "bg_black")

	if selected == 3:
		printWithBg("3번 항목", "black", "bg_white")
	else:
		printWithBg("3번 항목", "white", "bg_black")

	changeColor('white')
	changeColor('bg_black') 		#커맨드 창을 다시 검은색으로 바꿈

def printWithBg(text, color, bgcolor):
	changeColor(color)
	changeColor(bgcolor)
	print(text)

def changeColor(code):
	colors = {
		'black' : 30,
		'white' : 37,
		'bg_black' : 40,
		'bg_white' :47
	}
	print('\033['+ str(colors[code]) +'m', end = '\r')

print('하나를 선택해 주세요!')
time.sleep(1)
result = selectOne()
print(str(result) + "을 선택하셨습니다!")
time.sleep(1)
	</code>
</pre>

아직 정리가 안되고 확장성도 없는 일회성 코드이지만... 조만간 작은 모듈로 만들어 봐야겠다.