---
title: React-Native中加载图片的各种姿势
date: 2016/7/15 20:46:25
categories: ReactNative
tags:
  - react-native
  - image
---
初使用Image，由于在React Native中图片资源来源丰富，刚开始我也是一脸懵逼，在几番尝试以后，终于了然
## 加载项目目录图片
在项目目录中新建一个Directory，命名img，拷贝一张名为‘myicon.png’的图片
### 基本姿势
加载方法：

```
<View>
    <Text>Image的各种姿势</Text>
    <Image source={require('./img/myicon.png')} />
</View>
```
<!--more-->
效果如下图：
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-205f67acf20f9949?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
### 高级姿势
由于RN的图片资源文件的查找和 JS 模块相似，该会根据填写的图片路径相对于当前的 js 文件路径进行搜索。RN更加好的是Packager会根据平台选择相应的文件，例如 : myicon.ios.png 和 myicon.android.png 两个文件 ( 命名方式 android 或者 ios) 。该会根据 android 或者 ios 平台选择相应的文件。

我有两张图片，分别命名为myicon1.android.png和myicon1.ios.png

分别长这样：
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-925b8bf6dd61293f?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-73a968fd7625b291?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
<View>
    <Text>Image的各种姿势</Text>
    <Image source={require('./img/myicon1.png')} />
</View>
```
Android运行结果：
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-216fb3e54b59516c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
IOS运行结果：
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-3ff036543e4778aa?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**Tips：**
这边使用 Image 组件， require 中的图片名称必须为一个静态的字符串信息。不能在 require 中进行拼接。例如 :

```
<Image source={require('./img/myicon'+'.png')} />
```
这样之后运行就报错了 :
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-688977caf005f521?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
## 加载App中的图片
现阶段做原生 APP 的需求还是比较多的，不过现在使用了React   Native 之后，我们可以进行混合开发APP ( 一部分采用 ReactNative ，另一部分采用原生平台代码 ). 甚至可以使用已经打包在APP中的图片资源 ( 例如 :xcode ass et 文件夹以及 Android drawable 文件夹 )

以Android为例，加载ic_launcher
```
<View>
    <Text>Image的各种姿势</Text>
    <Image source={{uri:'ic_launcher'}} style={{width: 100, height: 100}} />
</View>
```
效果如下：
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-436a018b752c375b?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**Tips：**
1、加载App中的图片时，必须指定Image的大小，否则加载不出来
2、目前只支持访问drawable文件下的图片，mipmap文件夹下的图片不能访问

## 加载网络图片
很多时候，需要加载的是网络图片，网络图片的加载方法与本地图片的加载方法有所区别，这里必须指定图片的大小，类似于加载App图片

示例代码：

```
<View>
    <Text>Image的各种姿势</Text>
    <Image source={{uri:'http://avatar.csdn.net/2/1/1/1_shiquanqq.jpg'}}  style={{width:100,height:100}}/>
</View>
```
效果如下：
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-b3a825a653b93629?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
