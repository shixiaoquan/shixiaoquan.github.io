---
layout: post
title: ReactNative 自定义字体 Icon 的方法
date: 2018/06/24 21:35:30
author: 石小泉
feature-img: "assets/img/pexels/reactnativecustomiconfeatureimg.jpg"
thumbnail: "assets/img/thumbnails/reactnativecustomiconthumbnail.jpg"
categories: [React Native]
tags: [React Native]
---

## 简介
将svg制作成字体文件，然后以 Icon 的形式调用，既能保持 svg 矢量图的特性，又能减小 App 的体积。

实现这一功能需要使用 `react-native-vector-icons`，其提供了两种途径，一种是 IconMoon，一种是 Fontello。接下来将以 icoMoon 为例，说明使用方法， Fontello 只有一处不同，会在文中提及。

## 安装 `react-native-vector-icons`
以 yarn 为例，因为最近喜欢用 yarn
```
yarn add react-native-vector-icons

react-native link
```

只要两步

## 制作字体文件
### 准备 svg
如果有已完成的 svg 可以直接使用，当然最好；

如果没有可以 http://www.iconfont.cn/ 下载一些简单实用的；

我这里不再下载，直接使用网站提供的示例
### 使用相应的网站工具
icoMoon 和 Fontello 分别有网站提供字体文件制作。分别是 http://fontello.com/ 和 https://icomoon.io/app。

操作简单，很快就能制作完成，这两个网站都不用翻墙😀

## 导入字体文件
将制作好的字体文件（xxx.ttf）导入到 Android 和 iOS 的原生项目中，这一步是最关键的，稍有不慎，容易出错

我已经得到 icomoon 的字体文件，结构如下：


### Android


### iOS




## 本文结束，欢迎大家加群共同学习

|![QQ群：672509442]({{ site.url }}/assets/img/postpics/QQGroupQR.png)|
| :-: |
|**QQ群：672509442**|
