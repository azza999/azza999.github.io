---
layout: post
title: '[모던자바스크립트] 31. 문자열'
subtitle: 'modern javascript, 문자열'
categories: devlog
tags: javascript
comments: true
---

> 이 글은 번역 및 정리 글입니다.
> 출처: javascript.info

# 문자열

자바스크립트에서 텍스트 데이터는 문자열로 저장된다. 단일 문자에 대한 별도의 타입이 존재하지는 않는다.

문자열의 내부 형식은 `UTF-16`이며 페이지 인코딩과는 관련이 없다.

## 따옴표

따옴표는 작은 따옴표, 큰 따옴표, 역 따옴표가 있ㅆ다.

```js
let single = 'single-quoted';
let double = 'double-quoted';

let backticks = `backticks`;
```

작은 따옴표와 큰 따옴표는 기본적으로 동일하다. 그러나 백틱을 사용하면 표현식을 다음과 같이 묶어 문자열에 포함시킬 수 있다.

```js
function sum(a, b) {
  return a + b;
}

alert(`1 + 2 = ${sum(1, 2)}.`); // 1 + 2 = 3.
```

백틱을 사용하는 또 다른 장점은 문자열이 여러 줄로 확장 될 수 있다는 것이다.

```js
let guestList = `Guests:
 * John
 * Pete
 * Mary
`;

alert(guestList);
```

백틱은 추가로 `태그 템플릿`이 더 있지만 자주 사용되지는 않는다.

## 특수 문자

줄 바꿈을 나타내는 `줄 바꿈 문자`를 사용하여 작은 따옴표와 큰 따옴표로 여러 줄 문자열을 만들 수 있다.

```js
let guestList = 'Guests:\n * John\n * Pete\n * Mary';

alert(guestList);
```

아래 두 줄은 동일하지만 다르게 작성되었다.

```js
let str1 = 'Hello\nWorld'; // 개행문자로 두줄

// 백틱으로 구현한 두 줄
let str2 = `Hello
World`;

alert(str1 == str2); // true
```

이 외에도 여러가지 특수 문자가 있다.

| 문자                   | 기술                                                                                                                                                            |
| ---------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `\n`                   | 줄바꿈                                                                                                                                                          |
| `\r`                   | 캐리지 리턴: 단독으로 사용되지 않고, 윈도우즈 텍스트파일은 `\r\n`으로 줄 바꿈을 나타낸다.                                                                       |
| `\'`,`\"`              | 인용 부호                                                                                                                                                       |
| `\\`                   | 백 슬래시                                                                                                                                                       |
| `\t`                   | 탭                                                                                                                                                              |
| `\b`,`\f`,`\v`         | 백 스페이스, 폼 피드(프린트 출력시 페이지 마침), 세로 탭 - 호환성을 위해 유지되며 현재는 사용되지 않는다.                                                       |
| `\xXX`                 | 주어진 16 진수 유니 코드를 가진 유니코드 문자 `XX`. e.g. `\x7A` 는 `z`와 같다.                                                                                  |
| `\uXXXX`               | 예를 들어 UTF-16 인코딩의 16진 코드 `u00A9` - 은 저작권 기호 `©`. 4자리 16진수 여야 한다.                                                                       |
| `u{X...XXXXXX}`(1-6자) | 주어진 UTF-32 인코딩을 가진 유니 코드 심볼. 일부 희귀 문자는 2 바이트의 유니 코드 기호로 인코딩되어 4 바이트를 사용한다. 이런 식으로 긴 코드를 삽입 할 수 있다. |

유니코드를 사용한 예:

```js
alert('\u00A9'); // ©
alert('\u{20331}'); // 佫
alert('\u{1F60D}'); // 😍
```

모든 특수 문자는 백 슬래시 문자로 시작한다. 이스케이프 문자라고도 한다.

문자열에 따옴표를 삽입하려는 경우에도 사용할 수 있다.

예를 들어

```js
alert("I'm the Walrus!"); // I'm the Walrus!
```

같은 크기의 따옴표 안에서 따옴표를 사용하려면 백 슬래시를 붙여야한다.

## 문자열 길이

이 `length`속성의 문자열 길이는 다음과 같다.

```js
alert(`My\n`.length); // 3
```

## 캐릭터 접근

위치에 문자를 가져 오려면 `[pos]`처럼 대괄호를 사용하거나 `str.charAt(pos)`메소드를 호출한다. 첫 번째 문자는 0 위치에서 시작한다.

```js
let str = `Hello`;

// 첫번째 글자
alert(str[0]); // H
alert(str.charAt(0)); // H

// 마지막 글자
alert(str[str.length - 1]); // o
```

대괄호는 문자를 얻는 현대적은 방법이지만 `charAt`이 역사적 이유로 존재한다.

그들 사이의 유일한 차이점은 그 어떤 문자가 발견되지 않으면 `[]`는 `undefined`를 반환하고 `chatAt`은 빈 문자열을 반환한다.

```js
let str = `Hello`;

alert(str[1000]); // undefined
alert(str.charAt(1000)); // '' (an empty string)
```

다음처럼 문자를 반복할 수도 있다.

```js
for (let char of 'Hello') {
  alert(char); // H,e,l,l,o
}
```

## 문자열은 불변이다.

자바스크립트에서는 문자열을 변경할 수 없다. 캐릭터를 바꾸는 것은 불가능하다.

```js
let str = 'Hi';

str[0] = 'h'; // error
alert(str[0]); // 작동하지 않는다.
```

## 케이스 변경

`toLowerCase` 및 `toUpperCase()` 메소드가 대소문자를 변경한다.

```js
alert('Interface'.toUpperCase()); // INTERFACE
alert('Interface'.toLowerCase()); // interface
```

또는 단일 문자를 소문자로 사용하려는 경우:

```js
alert('Interface'[0].toLowerCase()); // 'i'
```

## 부분 문자열 검색

문자열 내에서 하위 문자열을 찾는 여러가지 방법이 있다.

### str.indexOf

첫 번째 방법은 `str.indexOf(substr, pos)` 이다.

주어진 위치에서 시작하여 `substr`을 찾고 일치하는 위치를 찾거나 찾을 수 없으면 `-1`을 반환한다.

```js
let str = 'Widget with id';

alert(str.indexOf('Widget')); // 0
alert(str.indexOf('widget')); // -1

alert(str.indexOf('id')); // 1, W'id'get
```

선택적 두 번째 매개 변수를 사용하면 주어진 위치에서 시작하여 검색 할 수 있다.

예를 들어 첫 번째 항목은 `id`가 `1`의 위치에 있다. 다음 항목을 찾으려면 `2` 위치인자를 넣어 검색한다.

```js
let str = 'Widget with id';

alert(str.indexOf('id', 2)); // 12
```

모든 경우에 관심이 있다면 `indexOf`를 루프에서 실행할 수 있다. 모든 콜은 이전 위치에서부터로 이루어진다.

```js
let str = 'As sly as a fox, as strong as an ox';

let target = 'as'; // 이걸 찾아보자

let pos = 0;
while (true) {
  let foundPos = str.indexOf(target, pos);
  if (foundPos == -1) break;

  alert(`Found at ${foundPos}`);
  pos = foundPos + 1; // 다음 위치를 찾아보자
}
```

같은 알고리즘을 더 짧게 배치 할 수 있다.

```js
let str = 'As sly as a fox, as strong as an ox';
let target = 'as';

let pos = -1;
while ((pos = str.indexOf(target, pos + 1)) != -1) {
  alert(pos);
}
```

`indexOf`를 사용할 때 주의해야 할 점이 있는데, 살펴보자.

```js
let str = 'Widget with id';

if (str.indexOf('Widget')) {
  alert('We found it'); // 작동하지 않는다. 0은 falsy값이기 때문에
}
```

제대로 동작하게 하려면 아래와 같이 해야한다.

```js
let str = 'Widget with id';

if (str.indexOf('Widget') != -1) {
  alert('We found it'); // 이제 작동!
}
```

#### 비트 NOT 트릭

`indexOf`를 동작시키는데 사용하는 간단한 트릭 중에 하나는 `비트 NOT` 연산자이다.

숫자를 32비트 정수로 변환하고 (소수부분이 존재한다면 제거) 이진 표현의 모든 비트를 반전시킨다.

컴퓨터공학적인 설명은 이렇고, 결과적으로는 `~n = -(n+1)`을 의미한다.

```js
alert(~2); // -3, -(2+1)
alert(~1); // -2, -(1+1)
alert(~0); // -1, -(0+1)
alert(~-1); // 0, -(-1+1)
```

이를 이용하면 이렇게 사용할 수 있다.

```js
let str = 'Widget';

if (~str.indexOf('Widget')) {
  alert('Found it!'); // 잘 동작한다.
}
```

요즘 자바스크립트에는 `.includes`가 존재하기 때문에 예전 코드에서나 볼 수 있는 트릭이긴 하다.

## includes, startsWith, endsWith

`str.includes(substr, pos)`는 포함여부에 따라 반환된다. 두번째 인자는 검색을 시작할 위치를 이야기한다.

```js
alert('Widget'.includes('id')); // true
alert('Widget'.includes('id', 3)); // false,
```

`str.startsWith` 및 `str.endsWith`는 다음과 같다.

```js
alert('Widget'.startsWith('Wid')); // true, "Widget" 은 "Wid"로 시작한다.
alert('Widget'.endsWith('get')); // true, "Widget" 은 "get"으로 끝난다.
```

## 부분 문자열 얻기

자바스크립트는 부분 문자열을 얻는 3가지 방법을 제공한다.

### str.slice(start[, end])

start부터 end까지의 문자를 반환한다.

```js
let str = 'stringify';
alert(str.slice(0, 5)); // 'strin'
alert(str.slice(0, 1)); // 's'
```

두번째 인수가 없으면 문자열 끝가지 반환한다.

```js
let str = 'stringify';
alert(str.slice(2)); // 'ringify'
```

음수값도 가능하다. 음수값은 끝에서 부터 시작한다.

```js
let str = 'stringify';

alert(str.slice(-4, -1)); // 'gif'
```

### str.substring(start [, end])

start와 end사이의 문자열을 반환한다. `slice`와 거의 동일하지만 end보다 start가 클 수 있다는 점이 다르다.

```js
let str = 'stringify';

alert(str.substring(2, 6)); // "ring"
alert(str.substring(6, 2)); // "ring"

// slice는
alert(str.slice(2, 6)); // "ring"
alert(str.slice(6, 2)); // ""
```

슬라이스와는 달리 음수는 작동하지 않는다.

### str.substr(start, [, length])

length만큼 start부터 반환한다.

```js
let str = 'stringify';
alert(str.substr(2, 4)); // 'ring'
```

첫번째 인수는 음수 일 수 있다.

```js
let str = 'stringify';
alert(str.substr(-4, 2)); // 'gi'
```

만약 셋 중에 하나만을 알아야겠다면 `slice`를 추천한다. 더 유연하고, 음수를 허용하며, 짧다.

## 문자열 비교

이전에도 이야기 했다시피 문자열은 알파벳 순서대로 비교된다.

하지만 이상한 점이 몇가지 있는데,

1. 소문자는 항상 대문자보다 크다.
2. 분음부호가 있는 문자는 순서가 없다.

```js
alert('a' > 'Z'); // true
alert('Österreich' > 'Zealand'); // true
```

### str.codePointAt(pos)

위치에 있는 문자의 코드를 반환한다.

```js
alert('z'.codePointAt(0)); // 122
alert('Z'.codePointAt(0)); // 90
```

### str.fromCodePoint(code)

코드로 문자를 만든다.

```js
alert(String.fromCodePoint(90)); // Z
```

`\u`와 16진수 코드를 사용하여 코드별로 유니코드문자를 만들 수 있다.

```js
alert('\u005a'); // Z
```

코드로 문자를 만드는 작업을 해보자.

```js
let str = '';

for (let i = 65; i <= 220; i++) {
  str += String.fromCodePoint(i);
}
alert(str);
// ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
// ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜ
```

어떤게 더 큰 값인지 알 수 있다. 분음이 붙은 문자는 알파벳과 다른 값을 갖는다.

### 정확한 비교

문자열을 비교하는 올바른 알고리즘은 알파벳이 언어마다 다르기 때문에 생각보다 복잡한다.

따라서 비교할 언어를 알아야한다. 운이 좋게도 모든 최신 브라우저(IE10-는 intl.js를 추가하여 사용하자)는 국제표준을 지원한다.

`str.localeCompare(str2)`는 언어 규칙에 따라 str보다 str2이 큰지 작은지를 반환한다.

- str보다 작은경우 음수
- str보다 큰경우 양수
- 동등하면 0

```js
alert('Österreich'.localeCompare('Zealand')); // -1
```

## 내부, 유니 코드

### 대리 쌍

자주 사용하는 모든 문자에는 2바이트 코드가 있다. 대부분의 유럽 언어, 숫자 및 대부부ㅜㄴ의 상형 문자로 된 문자는 2바이트로 표시된다.

그러나 2바이트는 65536 조합만 허용하며 모든 기호에는 충분하지 않다. 따라서 드문 심볼은 `대리 쌍`이라는 2바이트 문자 쌍으로 인코딩된다.

기술적으로 대리쌍은 아래처럼 감지할 수 있다.

```js
alert('𝒳'.charCodeAt(0).toString(16)); // d835,  0xd800 에서 0xdbff 사이
alert('𝒳'.charCodeAt(1).toString(16)); // dcb3,  0xdc00 에서 0xdfff 사이
```

### 분음 부호 및 정규화

많은 언어에는 위 또는 아래에 표시가 있는 기본 문자로 구성된 기호가 있다.

예를 들면 `a`는 다음처럼 될 수 있다. `àáâäãåā`. 문자 뒤에 특수 마크 기호를 사용하면 만들 수 있다.

```js
alert('S\u0307'); // Ṡ, S + dot upper
alert('S\u0307\u0323'); // Ṩ, S + dot upper + dot below
```

이 확장성 때문에 재밌는 일이 발생한다.

```js
let s1 = 'S\u0307\u0323'; // Ṩ, S + dot above + dot below
let s2 = 'S\u0323\u0307'; // Ṩ, S + dot below + dot above

alert(`s1: ${s1}, s2: ${s2}`);

alert(s1 == s2); // false
```

정규화시켜 비교하면 된다.

```js
alert('S\u0307\u0323'.normalize() == 'S\u0323\u0307'.normalize()); // true
```

# 숙제

## 첫문자를 대문자로 바꾸는 함수를 작성해보자

```js
ucFirst('john') == 'John';
```

<details markdown="1">
<summary>답</summary>

```js
function ucFirst(str) {
  if (!str) return str;

  return str[0].toUpperCase() + str.slice(1);
}

alert(ucFirst('john')); // John
```

</details>

## 스팸 확인

`viagra`, `xxx`를 포함하는 문장을 확인하는 함수를 작성해보자.

```js
checkSpam('buy ViAgRA now') == true;
checkSpam('free xxxxx') == true;
checkSpam('innocent rabbit') == false;
```

<details markdown="1">
<summary>답</summary>

```js
function checkSpam(str) {
  let lowerStr = str.toLowerCase();

  return lowerStr.includes('viagra') || lowerStr.includes('xxx');
}

alert(checkSpam('buy ViAgRA now'));
alert(checkSpam('free xxxxx'));
alert(checkSpam('innocent rabbit'));
```

</details>

## 텍스트 자르기

str의 길이를 확인하고 maxlength를 초과할 경우 줄임표 문자로 바꾸는 함수를 만들어보자.

`truncate(str, maxlength)`

```js
truncate(
  "What I'd like to tell on this topic is:",
  20
) = "What I'd like to te…";

truncate('Hi everyone!', 20) = 'Hi everyone!';
```

```js
checkSpam('buy ViAgRA now') == true;
checkSpam('free xxxxx') == true;
checkSpam('innocent rabbit') == false;
```

<details markdown="1">
<summary>답</summary>

```js
function truncate(str, maxlength) {
  return str.length > maxlength ? str.slice(0, maxlength - 1) + '…' : str;
}
```

말줌임 문자는 점 세개가 아닌 하나의 유니코드 문자이다.

</details>

## 돈 추출

`$120` 에서 120을 추출하자

```js
alert(extractCurrencyValue('$120') === 120); // true
```

<details markdown="1">
<summary>답</summary>

```js
function extractCurrencyValue(str) {
  return +str.slice(1);
}
```

</details>
