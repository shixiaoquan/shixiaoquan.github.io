---
title: AAPT-err----ERROR--Unable-to-open-PNG-file的解决方案
date: 2016/3/11 20:46:25
categories: Android
tags:
  - android
  - Error
---
# 1 png图片错误
使用Gradle在AndroidStudio中编译时，爆出如下错误

```
AAPT err(Facade for 1040283565): D:\projects\013网格化标准产品\03-开发\Android\InformationCollector\app\src\main\res\mipmap-xxxhdpi\ic_back.png ERROR: Unable to open PNG file
```
<!--more-->
用Android Studio打开ic_back.png，发现该文件其实是jpg格式，被强行改为.png。
之前在Eclipse中，IDE不回去检查这个问题，所以不会报错。
解决方案有两个：

 1. 把图片换成正宗的png图片
 2. 在build.gradle中添加两句代码

```
aaptOptions.cruncherEnabled = false
aaptOptions.useNewCruncher = false
```
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-23546ba82c3ed4f9?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

重新编译，解决问题


# 2 文件路径太长(仅限windows)
在windows系统中，由于对文件路径有长度限制，256个字节，如果图片的路径长度超过了这个限制，IDE也会报错
比如下面这个

```
AAPT err(Facade for 1040283565): D:\projects\013网格化标准产品\03-开发\Android\InformationCollector\app\src\main\res\mipmap-xxxhdpi\ic_up.png ERROR: Unable to open PNG file
```
已经超过限制。
这个问题比较隐蔽，而且IDE的报错和第一种情况相同，很难发现，最后在stackoverflow找到解决方案，

把项目名称改短一些，或者把项目不要放到太深的目录里即可
[站外图片上传中...(image-c7dc1e-1516253830384)]
地址：http://stackoverflow.com/questions/21222923/android-studio-error-unable-to-open-png-file
