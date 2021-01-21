---
layout:		post
title:		"i386과 x86_64"
subtitle:	"os 부트 미디어 생성시 주의점"
categories:	os
tags:		i386 x86_64 boot mbr
comments:	true
hard_wrap:	true

---

# 부트 미디어 생성시 i386과 x86_64

## 문제점
---

리눅스 (centos 6.10) 부트 미디어를 만들 일이 생겨서 별 생각 없이 CentOS-6.10-i386-bin-DVD.iso 버전을 다운받고 UltraISO를 이용해 boot media를 생성했는데, 해당 미디어로 부팅하면 바이오스에서

> booting from hard disk...  
> booting from rom...  
> boot from ipxe4 (혹은 ipxe6)  

이렇게 뜨며 부팅이 안되거나, 하위 순서이던 윈도우로 부팅이 되어버리는 현상이었다.
<br>
<br>

## 해결
---

간단하게, 32비트 cpu 기반인 i386 버전을 64비트 cpu 컴퓨터에서 돌리려니 이 사단이 난 것이었다. i386 버전이 아닌 x86_64라고 써있는 64bit cpu 버전의 iso 파일을 다시 구워서 해결했다.

![i386과 x86_64]({{ site.url }}/assets/img/2021-01-21/boot_isos.PNG)


<br>
<br>

## 배경지식
---

처음에 i386 버전을 다운받고, 64bit cpu pc의 vmware에서 돌렸을때는 아주 잘 돌아가서 이상하게 생각했다. iso파일에 이상이 있거나 boot record가 제대로 생성되지 않은것 같아서 boot media 생성 프로그램을 4\~5개를 돌려가며 써봤는데(rufus, ImgBurn, ultraISO, CDBurnerXP 등) 전부다 안되길레 구글링 후 os 부트 미디어는 cpu bit를 맞추지 않으면 안된다는 것을 깨달았다.


