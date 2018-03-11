---
title: Android四大组件之Activity
date: 2016/3/11 20:46:25
categories: Android
tags:
  - android
  - 四大组件
  - Activity
---
概述
==
## 简介 ##

 - Activity是Android组件中最基本也是最为常见的四大组件（Activity，Service服务,ContentProvider内容提供者，BroadcastReceiver广播接收器）之一 。它是一个应用程序组件，提供一个屏幕，用户可以用来交互为了完成某项任务；
 - Activity中所有操作都与用户密切相关，是一个负责与用户交互的组件，可以通过setContentView(View)来显示指定控件；
 - 在一个android应用中，一个Activity通常就是一个单独的屏幕，它上面可以显示一些控件也可以监听并处理用户的事件做出响应；
 - Activity之间通过Intent进行通信。

## 本质 ##
<!--more-->
官方给的解释：An Activity is an application component that provides a screen with which users can interact in order to do something, such as dial the phone, take a photo, send an email, or view a map.
Activity就是一个为用户提供可以和其他事物进行交互的屏幕的组件，例如：打电话、拍照、发送邮件、浏览地图等等。
生命周期
==
## 简介##
![Activity生命周期思维导图](http://upload-images.jianshu.io/upload_images/3161942-aa13ffd85c5931da?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这是官方给出的Activity生命周期的思维导图，Activity的整个生命周期都是依赖onCreate(),onStart(),onResume(),onPause(),onStop(),onDestory(),onRestart()这7个方法来完成。
**举个栗子**
创建一个最简单的Android程序，该程序只有一个Activity，程序运行时打开Activity，点击back键关闭Activity。这个过程就会将6个方法全部调用一遍。详情如下：
在加载程序时，依次调用onCreate()创建Activity；onStart()启动Activity；onResume()使得Activity可见。
back键关闭Activity时依次调用onPause()暂停Activity；onStop停止Activity但不释放资源；onDestory()销毁Activity。

## Activity的四种状态 ##

 1. Active/Runing
一个新 Activity 启动入栈后，它显示在屏幕最前端，处理是处于栈的最顶端（Activity栈顶），此时它处于可见并可和用户交互的激活状态,叫做活动状态或者运行状态（active or running）。
 2. Paused
当 Activity失去焦点， 被一个新的非全屏的Activity 或者一个透明的Activity 覆盖，此时的状态叫做暂停状态（Paused）。此时它依然与窗口管理器保持连接，Activity依然保持活力（保持所有的状态，成员信息，和窗口管理器保持连接），但是在系统内存不足的时候会被强行终止掉。所以它仍然可见，但已经失去了焦点，不可与用户进行交互。
 3. Stoped
如果一个Activity被另外的Activity完全覆盖掉，叫做停止状态（Stopped）。它依然保持所有状态和成员信息，但是它不再可见，所以它的窗口被隐藏，当系统内存需要被用在其他地方的时候，Stopped的Activity将被强行终止掉。
 4. Killed
如果一个Activity是Paused或者Stopped状态，系统可以将该Activity从内存中删除，Android系统采用两种方式进行删除，要么要求该Activity结束，要么直接终止它的进程。当该Activity再次显示给用户时，它必须重新开始和重置前面的状态。

**举几个实实在在的栗子**
创建一个只有一个Activity的Android程序，命名ActivityLifeCycleTest，并重写7个方法(这里不会用到onRestart方法，但是先写上)，在每个方法中打印日志，代码如下

```

    public static final String TAG = "lifecircle";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(TAG, "MainActivity   onCreate");
        setContentView(R.layout.activity_main);
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.i(TAG, "MainActivity   onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.i(TAG, "MainActivity   onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.i(TAG, "MainActivity   onPause");
    }

    @Override
    protected void onStop() {
        super.onStop();
        Log.i(TAG, "MainActivity   onStop");
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        Log.i(TAG, "MainActivity   onRestart");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.i(TAG, "MainActivity   onDestroy");
    }
```
然后运行程序，查看logcat中的日志（查看前先设置一下日志过滤器），如下图

```
01-28 15:19:28.811 28369-28369/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onCreate
01-28 15:19:28.913 28369-28369/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onStart
01-28 15:19:28.913 28369-28369/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onResume
```
根据日志可知，当加载一个Activity依次调用onCreate(),onStart(),onResume()
然后点击back键，关闭Activity，log如下

```
......
......
01-28 15:24:47.101 28369-28369/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onPause
01-28 15:24:47.535 28369-28369/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onStop
01-28 15:24:47.536 28369-28369/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onDestroy
```
所以，关闭Activity时依次执行onPause(),onStop(),onDestory().
接下来点儿复杂滴
在项目中新建一个Activity，命名为NormalActivity，从MainActivity中跳转过去，在NormalActivity中也重写6个方法。代码如下

```
public static final String TAG = "lifecircle";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(TAG, "NormalActivity   onCreate");
        setContentView(R.layout.activity_normal);
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.i(TAG, "NormalActivity   onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.i(TAG, "NormalActivity   onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.i(TAG, "NormalActivity   onPause");
    }
    @Override
    protected void onStop() {
        super.onStop();
        Log.i(TAG, "NormalActivity   onStop");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.i(TAG, "NormalActivity   onDestroy");
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        Log.i(TAG, "NormalActivity   onRestart");
    }
```
现在重新运行程序，使用intent跳转到NormalActivity（代码略过），查看log

```
......
......
01-28 15:42:38.994 18105-18105/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onPause
01-28 15:42:39.028 18105-18105/com.activitylifecycletest.app.activity I/lifecircle: NormalActivity   onCreate
01-28 15:42:39.038 18105-18105/com.activitylifecycletest.app.activity I/lifecircle: NormalActivity   onStart
01-28 15:42:39.038 18105-18105/com.activitylifecycletest.app.activity I/lifecircle: NormalActivity   onResume
01-28 15:42:39.564 18105-18105/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onStop

```
首先调用MainActivity的onPause方法将其暂停，然后三部曲创建NormalActivity，然后再onStop掉MainActivity，（这里为什么不直接onStop掉MainActivity再创建NormalActivity，因为伟大的Android开发者早已想到万一NormalActivity创建失败，MainActivity还可以继续使用，避免出现黑屏，影响用户体验），此时MainActivity并没有销毁，仍然保存在内存中，如果此时内存不足，系统会将其销毁。既然没有销毁，自然是可以恢复的，恢复就需要调用onRstart方法，按back键返回MainActivity，查看log

```
......
......
01-28 15:53:27.319 7680-7680/com.activitylifecycletest.app.activity I/lifecircle: NormalActivity   onPause
01-28 15:53:27.334 7680-7680/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onRestart
01-28 15:53:27.336 7680-7680/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onStart
01-28 15:53:27.336 7680-7680/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onResume
01-28 15:53:27.698 7680-7680/com.activitylifecycletest.app.activity I/lifecircle: NormalActivity   onStop
01-28 15:53:27.698 7680-7680/com.activitylifecycletest.app.activity I/lifecircle: NormalActivity   onDestroy

```

先暂停NormalActivity，然后执行onRestart方法，重启MainActivity，不需要重新创建，最后销毁掉NormalActivity。

如果不是跳转到另一个普通的Activity，而是启动一个弹出框会怎样呢？
创建一个DialogActivity，重写7个方法，代码如下

```

    public static final String TAG = "lifecircle";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dialog);
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.i(TAG, "DialogActivity   onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.i(TAG, "DialogActivity   onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.i(TAG, "DialogActivity   onPause");
    }
    @Override
    protected void onStop() {
        super.onStop();
        Log.i(TAG, "DialogActivity   onStop");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.i(TAG, "DialogActivity   onDestroy");
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        Log.i(TAG, "DialogActivity   onRestart");
    }
```
运行程序，启动DialogActivity（启动代码省略），查看log

```
......
......
01-28 16:11:12.277 1854-1854/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onPause
01-28 16:11:12.313 1854-1854/com.activitylifecycletest.app.activity I/lifecircle: DialogActivity   onStart
01-28 16:11:12.313 1854-1854/com.activitylifecycletest.app.activity I/lifecircle: DialogActivity   onResume
```
此时MainActivity只是暂停，并不会stop，此时Activity处于前面所说的第二种状态：Paused；按back键返回，查看log

```
......
01-28 16:14:05.881 1854-1854/com.activitylifecycletest.app.activity I/lifecircle: DialogActivity   onPause
01-28 16:14:05.911 1854-1854/com.activitylifecycletest.app.activity I/lifecircle: MainActivity   onResume
01-28 16:14:05.960 1854-1854/com.activitylifecycletest.app.activity I/lifecircle: DialogActivity   onStop
01-28 16:14:05.960 1854-1854/com.activitylifecycletest.app.activity I/lifecircle: DialogActivity   onDestroy
```
此时只需调用onResume方法，即可返回到MainActivity。

项目源码下载地址
Github：https://github.com/yueryouayou/ActivityLifeCycleTest
CSDN：http://download.csdn.net/detail/shiquanqq/9421165
