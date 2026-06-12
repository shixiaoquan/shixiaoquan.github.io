---
layout: post
title:  "一些实用的正则表达式"
date:   2019-12-21 10:20
categories: javascript
---

## 一些实用的正则表达式

```javascript
/* 合法uri */
export function validateURL(textval) {
 const urlregex = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\*\+,;=.]+$/
 return urlregex.test(textval)
}
/* 小写字母 */
export function validateLowerCase(str) {
 const reg = /^[a-z]+$/
 return reg.test(str)
}
/* 大写字母 */
export function validateUpperCase(str) {
 const reg = /^[A-Z]+$/
 return reg.test(str)
}
/* 大小写字母 */
export function validateAlphabets(str) {
 const reg = /^[A-Za-z]+$/
 return reg.test(str)
}
/* 市场售价 */
export function validatePrice(str) {
 const reg = /(^[1-9]\d*(\.\d{1,2})?$)|(^0(\.\d{1,2})?$)/
 return reg.test(str)
}
/* 库存预警值 匹配非负整数（正整数 + 0） */
export function validatestockWarn(str) {
 const reg = /^(0|[1-9][0-9]*)$/
 return reg.test(str)
}
/* 比价网站 只验证京东和苏宁网站 */
export function validateCompareWebsite(str) {
 const reg = /^((https\:\/\/[0-9a-zA-Z\_]+\.|http\:\/\/[0-9a-zA-Z\_]+\.|https\:\/\/|http\:\/\/)|([0-9a-zA-Z\_]+\.){0,1})(jd|suning)\.(com$|com\/[\S]*)/i
 return reg.test(str)
}
/* 固定电话 */
export function validateTelephone(str) {
 const reg = /^(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}$/
 return reg.test(str)
}
/* 手机号码 */
export function validatePhoneNumber(str) {
 const reg = /^[1][3,4,5,6,7,8,9][0-9]{9}$/
 return reg.test(str)
}
/* 手机号码和固定电话 */
export function validatePhTelNumber(str) {
 const reg = /^((0\d{2,3}-\d{7,8})|(1[3456789]\d{9}))$/
 return reg.test(str)
}
/* 电子邮箱 */
export function validateEmail(str) {
 const reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
 return reg.test(str)
}
/* 邮编 */
export function validateZipCode(str) {
 const reg = /^[1-9][0-9]{5}$/
 return reg.test(str)
}
/* 身份证 */
export function validateIDCard(str) {
 const reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
 return reg.test(str)
}
/* 银行卡号 15位或者16位或者19位 */
export function validateBank(str) {
 const reg = /^([1-9]{1})(\d{14}|\d{18}|\d{15})$/
 return reg.test(str)
}
/* 纳税人识别码 */
export function validateTaxpayer(str) {
 const reg = /^([1-9]{1})(\d{14}|\d{18}|\d{15})$/
 return reg.test(str)
}
/* 匹配全空格 */
export function validateAllBlank(str) {
 const reg = /^\s+$/gi
 return reg.test(str)
```
