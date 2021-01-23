---
layout:		post
title:		"[LINUX/UNIX] 에러 메세지 리다이렉트 문제"
subtitle:	"에러 스킵이 이상한데?"
categories:	os
tags:		redirect find permission
comments:	true
hard_wrap: true

---

# 에러 메시지는 볼 필요가 없어요!

## find 명령어가 남발하는 에러 메시지
---

환경 : centos 6.10

![Find 에러 메시지]({{ site.url }}/assets/img/2021-01-23/find_error_msg.png)
<p style="opacity: 0.5; text-align: center;">파일을 찾는건지, 에러 메시지를 찾는건지...</p>

 일반 사용자 계정에서 find 명령어를 이용해서 파일을 찾을 때 매일 마주하는 에러 메시지이다. find 명령어가 모든 디렉터리를 스캔할 때, root 사용자 또는 다른 사용자의 디렉터리를 접근하지 못해서 발생하는 에러인데, 파일을 찾을 때 당연하게도 별로 영양가가 없는 에러 메시지 표기이다.
 <br>
 <br>

## grep을 이용한 에러 메시지 생략...?

<pre><code>find / -name hosts \| grep -v Permission</code></pre>

 처음에는 grep -v 옵션을 이용해 에러 메시지를 생략해 보려 했지만, 에러 메시지는 grep -v 옵션으로 걸러지지 않았다. 표준 출력(STDOUT)이 아닌 에러 메시지 출력(STDERR)이기 때문이다. | (파이프)를 통해서 출력값을 넘길 수 있지만, 표준 출력이 아닌 에러는 파이프를 통해서 건너가지 않는 모양이다.

 하는 수 없이 에러를 표준 출력에 포함시켜 준 뒤(2>&1), 이 결과를 파이프로 넘겨서 Permission을 포함하는 텍스트를 제외했다.

<pre><code>find / -name hosts 2>&1 \| grep -v Permission</code></pre>
<br>
<br>

## STDERR 리다이렉트를 통한 에러 메시지 무시

사실 출력 스트림을 다룰 줄 안다면, 위와 같은 복잡한 방법 말고 그냥 에러 메시지 자체를 무시해 버리는 방법도 있다. 리눅스/유닉스의 입/출력 스트림은 3가지 이다. 0번 표준 입력, 1번 표준 출력, 2번 표준 에러 스트림이다. 이를 통해 그냥 '>'만 사용하는 출력 리다이렉션이 아닌, 스트림 자체를 다른곳으로 넘겨버리는 "2> /dev/null"의 에러 메시지 리다이렉션이 있다.

<pre><code>find / -name hosts 2> /dev/null</code></pre>

![Find 에러 메시지]({{ site.url }}/assets/img/2021-01-23/clean_find.png)
<p style="opacity: 0.5; text-align: center;">깔끔하게 원하는 것만 나왔다.</p>

따라서 보통의 경우라면 위와 같은 방법으로 에러 메시지를 무시하고 표준 출력 스트림만을 볼 수 있다. 하지만 조그마한 문제가 발생했다.

![Find 에러 메시지]({{ site.url }}/assets/img/2021-01-23/csh_err_redirection.png)
<p style="opacity: 0.5; text-align: center;">2와 > 사이에 띄어쓰기가 들어갔다!</p>

현재 업무에서 사용하는 환경은 centos 6.10에 csh을 사용했는데, csh에서는 stderr의 리다이렉션이 불가능 한 듯 하다.

<a href="https://unix.stackexchange.com/questions/35715/stderr-redirection-not-working-in-csh">stderr redirection not working in csh</a>