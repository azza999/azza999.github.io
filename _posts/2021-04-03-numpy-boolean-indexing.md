---
layout:		post
title:		"[Python] 넘파이 불리언 인덱싱"
categories:	dev
tags:		diary
comments:	true
hard_wrap: true

---

# 배열에서 요소 선택하기

## 불리언 인덱싱
---

> arr = [1, 2, 3, 4, 5]
> booleans = [True, False, True, False, False]
> print(arr[booleans])
>
> result : [1, 4]

파이썬 넘파이 배열에서는 타겟 배열에서 같은 차원의 boolean 값을 담은 배열을 인덱스로 사용할 수 있다.

> arr = np.array([
					[1,2,3,4,5],
					[11,22,33,44,55],
					[111,222,333,444,555]
				])
> booleans = np.array([
					[True,False,False,True,False],
					[True,False,False,True,True],
					[True,False,True,True,False]
				])
> print(arr[booleans])
>
> result : [1, 4, 11, 44, 55, 111, 333, 444]

2차원 이상에서도 가능하다.