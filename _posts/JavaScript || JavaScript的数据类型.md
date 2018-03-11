---
title: JavaScript的数据类型
date: 2016/8/3 20:46:25
categories: JavaScript
tags:
  - JavaScript
  - 数据类型
---
### Number
在JavaScript中，不区分整型和浮点型。例如
```
1           //整数
1.1         //浮点数
0.232e4     //科学计数法 等同于0.232×10000
-23         //负数
NaN         //not a number ,表示结果无法集散
Infinity    //无限大  超出Number的取值范围
```
<!--more-->
两个例子
> `2 / 0 = Infinity` </br>
> `0 / 0 = NaN`
---

### 布尔类型
和所有语言一样，布尔类型只有两种取值，true和false
```
true        //true
false       //false
2 > 1       //true
2 < 1       //false
```
跟布尔类型密切相关的是***与或非***三种运算
#### 与运算
运算符 &&
```
true && true        //true
true && false       //false
false && false      //false
```
#### 或运算
运算符 ||
```
true || true        //true
true || false       //true
false || false      //false
```
#### 非运算
运算符 ！
```
!true       //false
!false      //true
```
---
### 字符串
字符串是使用单引号'或者双引号"括起来的任意文本</br>
例如`'android'`  `"ios"`</br>
但是`''`或者`""`本身并不是字符串的一部分

---
### 数组
数组是一串按照顺序排列的元素的集合，例如：
```
[1, 2, 3, 4, 6, 7]
[23, 54, 54, '12', 'adc']
['12', '23', 'av', {a:b,c:d}, [1, 2]]
```
创建数组的两种方法
- `var arr = new Array('a', 'c', 'd')`
- `var arr = ['a', 'c', 'd']`
推荐使用第二种方法，该方法申明的数组可读性更好

---
### 对象
由key-value组成的无序集合
```
var company = {
    google: 'android',
    apple: 'ios',
    microsoft: ['office', 'windows', 'vs'],
    facebook: 'facebook',
    beijing: true,
    money: null
}
```
#### 取值
```
company.google       //'android'
company.microsoft    //['office', 'windows', 'vs']
company.monet        //null
```
#### 添加
```
var company = {...}
company['china'] = '1949'
console.log(company)
```
结果
```
{
    apple: "ios"
    beijing: true
    china: "1949"
    facebook: "facebook"
    google: "android"
    microsoft: ["office", "windows", "vs"]
    money: null
}
```
---
### null和undefined
null是什么都么有，空的，和`0`以及空字符串`null`都不同</br>
undefined是未定义</br>
两者的区别未见啥大的意义，一般情况下，都应该使用null，undefined可用于判断参数是否传递，未传递则为undefined</br>
一个生动形象的例子
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-355b9bb1dbafffe5?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





