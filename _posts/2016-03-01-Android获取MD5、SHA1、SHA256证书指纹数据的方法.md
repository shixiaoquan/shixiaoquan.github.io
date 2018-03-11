---
layout: post
title: Android获取MD5、SHA1、SHA256证书指纹数据的方法
date: 2016/2/1 20:46:25
feature-img: "assets/img/pexels/android-code.jpg"
thumbnail: "assets/img/thumbnails/android-code.jpg"
categories: [Android]
tags: [android, MD5, SHA1, SHA256]
---
以Mac为例
### 切换到.android目录

```
cd ~/.android
```
### 使用命令（需要输入密码）
debug的默认口令为：android
如果使用自己提供的keystore，就是自己的密码了
```
keytool -list -v -keystore debug.keystore
```

<!--more-->
### 结果
![20171122172922201.jpeg](http://upload-images.jianshu.io/upload_images/3161942-28e9f730b9cae1d4.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
