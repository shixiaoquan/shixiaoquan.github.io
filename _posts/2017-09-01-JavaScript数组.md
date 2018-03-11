---
layout: post
title: JavaScript数组
date: 2017/9/1 20:46:25
feature-img: "assets/img/pexels/javascript-featured.png"
thumbnail: "assets/img/thumbnails/javascript-featured.png"
categories: [JavaScript]
tags: [javascript, 数组]
---

数组可以包含任意类型的数据，通过索引获取元素</br>

- 获取数组的长度，可以使用length属性
- 
```javascript
var arr = [1, 2, 3, '456']
arr.length      //  4
```

<!--more-->
-  给数组的length属性赋新值时，会导致数组的大小发生变化

```javascript
var arr = [1, 2, 3, '456']
arr.length                  //  4
arr.length = 6
arr                         // [1, 2, 3, '456', undefined, undefined]
arr.length = 2
arr                         // [1, 2]
```
- 可以通过索引修改指定元素

```javascript
var arr = [1, 2, 3, '456']
arr[2] = 666
arr                         // [1, 2, 666, '456']
```
- 如果索引超出范围，不回报错，会改变数组的大小

```javascript
var arr = [1, 2, 3, '456']
arr[5] = 666
arr                         //[1, 2, 3, '456', undefined, 666]
```

### indexOf
获取某个元素的索引，如果改元素不存在，则返回-1

```javascript
var arr = [1, 2, 3, '456']
arr.indexOf(1)              // 0
arr.indexOf(2)              // 1
arr.indexOf(3)              // 2
arr.indexOf('456')          // 3
arr.indexOf(666)            // -1
```
### slice
- 通过指定起始索引和终止索引，截取数组的部分元素,返回新的数组

```javascript
var arr = [1, 2, 3, '456']
arr.slice(1,3)      //从索引1开始到索引3，不包括索引3  [2, 3]
```
- 只传一个参数时,从指定索引到结束
```
var arr = [1, 2, 3, '456']
arr.slice(2)      // [3, '456']

```javascript
- 不传参数，复制该数组
```
var arr = [1, 2, 3, '456']
arr.slice()      // [1, 2, 3, '456']

```javascript
### push
从末尾添加元素, 返回新数组长度

```javascript
var arr = [1, 2, 3, '456']
arr.push(666)       // 5
arr                 // [1, 2, 3, '456', 666]
var newArr []
newArr.pop()        // undefined  空数组时 不会报错，返回undefined
```

### pop
从末尾删除一个元素，返回被删除的元素

```javascript
var arr = [1, 2, 3, '456']
arr.pop()           // '456'
arr                 // [1, 2, 3]
```

### unshift
从开头添加元素, 返回修改后的数组的长度

```javascript
var arr = [1, 2, 3, '456']
arr.unshift(666, 777)   // 6
arr                     // [666, 777, 1, 2, 3, '456']
```

### shift
从开头删除一个元素

```javascript
var arr = [1, 2, 3, '456']
arr.shift()             // 1
arr                     // [2, 3, '456']
```

### sort
对数组元素进行排序

```javascript
var arr = ['B', 'A', 'D']
arr.sort()              // ['A', 'B', 'D']
arr                     // ['A', 'B', 'D']
```

### reverse
将元素掉转过来

```javascript
var arr = [1, 2, 3, '456']
arr.reverse()           //  ["456", 3, 2, 1]
arr                     //  ["456", 3, 2, 1]
```

### splice
这是个万能的方法，可以在指定位置删除指定个数的元素，并添加新的元素</br>
返回删除的元素

```javascript
var arr = [1, 2, 3, '456']
arr.splice(1, 2, 666666)    // [2, 3]
arr                         // [1, 666666, '456']
```

### concat
将数组连接起来,返回一个新的数组，并不会改变原数组

```javascript
var arr = [1, 2, 3, '456']
arr.concat('123', '234')        // [1, 2, 3, "456", "123", "234"]
arr.concat('123', ['1', '2'])   // [1, 2, 3, "456", "123", "1", "2"]
```

### join
使用指定的字符串将数组的元素串联起来，生成一个新的字符串,返回生成的字符串

```javascript
var arr = [1, 2, 3, '456']
arr.join('=')           // "1=2=3=456"
```
