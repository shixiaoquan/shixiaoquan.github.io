---
layout: post
title: React-Native开发环境搭建、Hello-World
feature-img: "assets/img/pexels/react-native-for-cross-platform-mobile-app-development.jpg"
thumbnail: "assets/img/thumbnails/react-native-for-cross-platform-mobile-app-development.jpg"
date: 2016/6/13 20:46:25
categories: [React Native]
tags: [react-native, 开发环境]
---
## 简述
为了避免Android平台和IOS平台的重复开发，对于性能要求不太高的应用可以采用React Native进行开发，以减少开发成本，这里就简单介绍一下React Native的开发环境搭建。

（**以Mac为例**）

## 必须安装的软件
因为React Native离不开JavaScript，不管是Android还是IOS都需要安装以下软件
### Homebrew
Homebrew是Mac系统的包管理器，安装的目的是方便安装Node等其他的软件

<!--more-->
安装方法：

`
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
`

Tips：在Max OS X 10.11（El Capitan)版本中，homebrew在安装软件时可能会碰到/usr/local目录不可写的权限问题。可以使用下面的命令修复：

`
sudo chown -R `whoami` /usr/local
`

### Node
使用刚刚安装的Homebrew来安装Node（React Native目前需要NodeJS5.0或者更高版本）

安装方法：

`
brew install node
`

安装完以后建议设置npm镜像以加速

`npm config set registry https://registry.npm.taobao.org --global`
`npm config set disturl https://npm.taobao.org/dist --global`

### Yarn、React Native的命令行工具（react-native-cli）

**Yarn**是Facebook提供的替换npm的工具，可以加速node模块的下载

**react-native-cli**用于完成创建项目、初始化、运行、更新、打包等任务

安装方法：

`brew install node`

Tips：如果你看到EACCES: permission denied这样的权限报错，那么请参照上文的homebrew译注，修复/usr/local目录的所有权：

`sudo chown -R `whoami` /usr/local`

## Android需要做的
### 配置ANDROID_HOME环境变量
确保ANDROID_HOME环境变量正确地指向了你安装的Android SDK的路径。具体的做法是把下面的命令加入到~/.bash_profile文件中

如果你不是通过Android Studio安装的sdk，则其路径可能不同，请自行确定清楚。

`export ANDROID_HOME=~/Library/Android/sdk`

然后使用下列命令使其立即生效（否则重启后才生效）：

`source ~/.bash_profile`

可以使用echo $ANDROID_HOME检查此变量是否已正确设置。

`$ echo $ANDROID_HOME`
`~/Library/Android/sdk`

### Android Studio
需要Android Studio2.0或更高版本
。。。。。。
安装教程略过

安装Android Studio只有一个目的：使用Android模拟器，当然使用Genymotion也是可以的,用真机当然更好了。
## IOS需要做的
Apple大法好，Apple就是吊，IOS要做的很简单，打开App Store，安装Xcode，然后就咩有然后了，开干。

## 推荐安装的软件
### Watchman
Watchman是由Facebook提供的监视文件系统变更的工具。安装此工具可以提高开发时的性能（packager可以快速捕捉文件的变化从而实现实时刷新），总之就是为了更快。

`brew install watchman`

其实还有很多工具例如：Flow、Nuclide等，但是没那么常用，像Flow入门较麻烦，就不说了。我们常用WebStorm或Sublime Text就行了。

Nuclide，这个要说一下，由于RN开发主要是编写JS代码，我们使用自己顺手的工具就好，但是程序编译、打包都需要敲命令行完成，所以Nuclide就是为了解决这个问而生的，但是目前只是基于Atom的一个插件，使用Nuclide之前必须安装Atom，效果不是很好，但是相信FB会把它越做越好吧，就像Android Studio之于Eclipse。
## 测试安装
重点来了，忙了半天，试试行不行。

`react-native init MyApp`
`cd MyApp`

这两步走完，项目已经创建好了，并且已经切换到项目目录。
接下来打开Android和IOS的模拟器，运行项目就行了

***Android***

`react-native run-android`

***IOS***

`react-native run-ios`
如下图

![WX20161221-143954.png](http://upload-images.jianshu.io/upload_images/3161942-5a2fefe582169fa3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 出Hello World
修改index.android.js和index.ios.js，增加Android和IOS<Text>标签
如下图

![WX20161221-144824.png](http://upload-images.jianshu.io/upload_images/3161942-88f1c84fb68d683f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
