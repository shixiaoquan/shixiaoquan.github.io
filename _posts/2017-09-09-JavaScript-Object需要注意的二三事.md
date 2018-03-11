---
layout: post
title: JavaScriptd-Object需要注意的二三事
date: 2017/9/9 20:46:25
feature-img: "assets/img/pexels/javascript-computer.jpeg"
thumbnail: "assets/img/thumbnails/javascript-computer.jpeg"
categories: [JavaScript]
tags: [javascript, object]
---

- 取值
用object.prop方式取值

```javascript
var company = {
    name: 'google',
    age: '28',
    money: 'I do not known'
}
company.name            //'google'
```

<!--more-->
- 用object['propname']
当属性名不是一个有效的变量名时，只能使用这种方法获取

```javascript
var company = {
    name: 'google',
    age: '28',
    money: 'I do not known',
    'my-job': 'coding'
}
company['my-job']       // 'coding'
```

注意：定义一个Object时，属性名尽量为有效的变量名，这样便于取值

- 可以自由的添加删除对象的属性

```javascript
var jake = {
    name: '小明'
};
jake.age; // undefined
jake.age = 18; // 新增一个age属性
jake.age; // 18
delete jake.age; // 删除age属性
jake.age; // undefined
delete jake['name']; // 删除name属性
jake.name; // undefined
delete jake.school; // 删除一个不存在的school属性也不会报错
```

判断Object的某个属性是否存在

- in

```javascript
var company = {
    name: 'google',
    age: '28',
    money: 'I do not known'
}
'name' in company       // true
'age' in company       // true
```

- hasOwnProperty

```javascript
var company = {...}
'name' in company       // true
'toString' in company   // true
```
in虽然能判断属性是否存在，但是对象继承的属性也会参与判断，就导致上面这种情况，这时就需要使用hasOwnProperty

```javascript
var company = {...}
company.hasOwnProperty('name')       // true
company.hasOwnProperty('toString')   // false
```



