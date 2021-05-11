---
layout:		post
title:		"[Python] 문자열 이어쓰기"
categories:	dev
tags:		diary
comments:	true
hard_wrap: true

---

# 파이썬에서 문자열 이어쓰기

## 말 그대로 이어서 계속 쓰기
---

구글 코랩에서 print 함수로 두 문자열을 출력하려다가 실수로 콤마(,)를 적지 않고 print를 출력하게 되었다.

> print('abc' 'def')

다른 언어에서는 syntax 에러가 나기 때문에 당연히 에러가 나오겠거니 하고 끄려 했는데, 놀랍게도 결과가 출력되었다.

> asdqwe

처음에는 구글 코랩에서 파이썬 런타임에 코드를 넘길 때 escape되지 않았나 했는데, 로컬 환경에서 실행해도 마찬가지 였다. 인터넷에 검색해도 substring, split, join같이 문자열을 다루는 함수만 나오고 코딩할 때 문자열을 이어쓰는 경우는 (물론 거의 없겠지만) 잘 안나오길래 기록해 둔다.

참고로 다음과 같은 문자열 지정 방식도 모두 가능하다)

> print('abc' 'def')			# abcdef  
> print('abc' "def")			# abcdef  
> print('abc' """def""")		# abcdef  
> print('abc' """def  
>   
> """)							# abcdef  