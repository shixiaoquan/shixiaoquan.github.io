---
title: Android-widget之PopupWindow
date: 2016/3/11 20:46:25
categories: Android
tags:
  - android
  - popupwindow
---
概述
---
Android应用中经常会弹出一个窗体，进行一些操作，比如说分享、选择城市等等，类似于AlertDialog,下面将详细讲解PopupWindow。
构造方法
----
PopupWindow的构造方法，官方给出的有9种，项目中常用的只有最后两种

1. `PopupWindow(Context context) `
Create a new empty, non focusable popup window of dimension (0,0).
创建一个宽度为0、高度为0的无焦点的空弹窗。
这种方法创建的弹窗，提供了背景
context为上下文。
<!--more-->

2. `PopupWindow(Context context, AttributeSet attrs) `
Create a new empty, non focusable popup window of dimension (0,0).
创建一个宽度为0、高度为0的无焦点的空弹窗。
这种方法创建的弹窗，提供了背景

3. `PopupWindow(Context context, AttributeSet attrs, int defStyleAttr)`
Create a new empty, non focusable popup window of dimension (0,0).
创建一个宽度为0、高度为0的无焦点的空弹窗。
这种方法创建的弹窗，提供了背景

4. `PopupWindow(Context context, AttributeSet attrs, int defStyleAttr, int defStyleRes) `
Create a new empty, non focusable popup window of dimension (0,0).
创建一个宽度为0、高度为0的无焦点的空弹窗。
这种方法创建的弹窗，提供了背景

5.  `PopupWindow()`
Create a new empty, non focusable popup window of dimension (0,0).
The popup does not provide any background. This should be handled by the content view.
创建一个宽度为0、高度为0的无焦点的空弹窗。
这种方法创建的弹窗，没有背景，需要自己填充

6.  `PopupWindow(View contentView)`
Create a new non focusable popup window which can display the contentView. The dimension of the window are (0,0).
The popup does not provide any background. This should be handled by the content view.
创建一个宽度为0、高度为0，可以自定义内容的无焦点弹窗。
这种方法创建的弹窗没有背景，需要自己填充
contentView：弹窗展示的内容

7.  `PopupWindow(int width, int height) `
Create a new empty, non focusable popup window. The dimension of the window must be passed to this constructor.
The popup does not provide any background. This should be handled by the content view.
创建一个宽度为width、高度为height的无焦点空弹窗。
这种方法创建的弹窗没有背景，需要自己填充
height：弹窗的高度
width：弹窗的宽度

8.  `PopupWindow(View contentView, int width, int height)`
Create a new non focusable popup window which can display the contentView.
创建一个自定义宽度、高度、显示内容的无焦点弹窗。
contentView：自定义的弹窗显示内容
width：弹窗宽度
height：弹窗高度
**举个栗子**
```
View view=getLayoutInflater().inflate(R.layout.window, null);
PopupWindow  mPop =new
PopupWindow(view,LayoutParams.WRAP_CONTENT,
LayoutParams.WRAP_CONTENT);
```

9.  `PopupWindow(View contentView, int width, int height, boolean focusable) `
Create a new popup window which can display the contentView.
创建一个自定义宽度、高度、显示内容、是否有焦点的弹窗。
contentView：自定义的弹窗显示内容
width：弹窗宽度
height：弹窗高度
focusable：是否有焦点，true：有焦点；false：无焦点（默认为false，与第8中构造方法效果相同）
**举个栗子**
```
View view=getLayoutInflater().inflate(R.layout.window, null);
PopupWindow  mPop =new
PopupWindow(view,LayoutParams.WRAP_CONTENT,
LayoutParams.WRAP_CONTENT,true);
```

显示方式
----
PopupWindow一般有两种展示方法，用showAsDropDown()和showAtLocation()两种方法实现。一般参数有两种，有偏移和无偏移。
官方的方法如下
**showAsDropDown()**
 - `showAsDropDown(View anchor, int xoff, int yoff, int gravity)`
 - `showAsDropDown(View anchor, int xoff, int yoff) `
 - `showAsDropDown(View anchor) `
anchor可以理解为锚，弹窗显示在anchor下面，xoff为X轴偏移量，yoff为Y轴偏移量，gravity为显示方式
**上栗子**
 - `mPop.showAsDropDown(anchor);`
弹窗显示在anchor正下方，无任何偏移。
 -  `mPop.showAsDropDown(anchor,xoff,yoff);`
弹窗在anchor下方显示，X轴偏移xoff,Y轴偏移yoff。
 - `mPop.showAsDropDown(anchor,xoff,yoff,Gravity.CENTER);`
弹出在anchor下方居中显示，同时X轴偏移xoff,Y轴偏移yoff。

**showAtLocation()**
 - `showAtLocation(View parent, int gravity, int x, int y)`
按函数名来理解，很容易看出该函数的意义，即在某个位置显示弹窗，我们要做的就是为弹窗设置Location。
parent：弹窗显示的父容器
gravity：显示方式
x：X轴偏移量
y：Y轴偏移量
**栗子来啦**
```
mPop.showAtLocation(PopWindow.this.findViewById(R.id.rl),
Gravity.TOP | Gravity.LEFT, 20, 20);
```
在屏幕顶部|居右，X轴偏移20，Y轴偏移20；

实栗
--
这里实现一个常见的分享弹窗，点击弹窗外面或者点击back键，关闭弹窗
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-de15978eba081e54?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) ![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-a13b8e298344ce5c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) ![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-2a8bd3b554d6b177?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两个布局文件，一个主界面布局文件、一个弹框内容布局文件
activity_main.xml
```
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <Button
        android:id="@+id/btn1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="showAsDropDown无偏移"  />
    <Button
        android:id="@+id/btn2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="showAsDropDown有偏移"  />

</LinearLayout>
```
popup_share.xml

```
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white">
 	<LinearLayout
 	    android:layout_marginLeft="10dp"
 	    android:layout_weight="1"
 	    android:layout_width="0dp"
 	    android:layout_height="wrap_content"
 	    android:orientation="vertical">
 	    <ImageView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:src="@drawable/umeng_socialize_wechat"/>
 	    <TextView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:textSize="10sp"
 	        android:textColor="@color/black"
 	        android:layout_gravity="center"
 	        android:text="微信好友"/>
 	</LinearLayout>
 	<LinearLayout
 	    android:layout_weight="1"
 	    android:layout_width="0dp"
 	    android:layout_height="wrap_content"
 	    android:orientation="vertical">
 	    <ImageView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:src="@drawable/umeng_socialize_wxcircle"/>
 	    <TextView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:textSize="10sp"
 	        android:textColor="@color/black"
 	        android:layout_gravity="center"
 	        android:text="微信朋友圈"/>
 	</LinearLayout>
 	<LinearLayout
 	    android:layout_weight="1"
 	    android:layout_width="0dp"
 	    android:layout_height="wrap_content"
 	    android:orientation="vertical">
 	    <ImageView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:src="@drawable/umeng_socialize_qq_on"/>
 	    <TextView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:textSize="10sp"
 	        android:textColor="@color/black"
 	        android:layout_gravity="center"
 	        android:text="QQ好友"/>
 	</LinearLayout>
 	<LinearLayout
 	    android:layout_weight="1"
 	    android:layout_width="0dp"
 	    android:layout_height="wrap_content"
 	    android:orientation="vertical">
 	    <ImageView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:src="@drawable/umeng_socialize_qzone_on"/>
 	    <TextView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:textSize="10sp"
 	        android:textColor="@color/black"
 	        android:layout_gravity="center"
 	        android:text="QQ空间"/>
 	</LinearLayout>
 	<LinearLayout
 	    android:layout_marginRight="10dp"
 	    android:layout_weight="1"
 	    android:layout_width="0dp"
 	    android:layout_height="wrap_content"
 	    android:orientation="vertical">
 	    <ImageView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:src="@drawable/umeng_socialize_sina_on"/>
 	    <TextView
 	        android:layout_width="wrap_content"
 	        android:layout_height="wrap_content"
 	        android:textSize="10sp"
 	        android:textColor="@color/black"
 	        android:layout_gravity="center"
 	        android:text="微博"/>
 	</LinearLayout>
</LinearLayout>

```
重新activity的onCreate方法

```
@Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        popupView= getLayoutInflater().inflate(R.layout.popup_share, null);
        mPop = new PopupWindow(popupView,
        	LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT,true);
        mPop.setBackgroundDrawable(new ColorDrawable(0));

        btn1=(Button) findViewById(R.id.btn1);
        btn1.setOnClickListener(this);
        btn2=(Button) findViewById(R.id.btn2);
        btn2.setOnClickListener(this);
    }
```
两种显示方法的触发事件

```
@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		switch (v.getId()) {
		case R.id.btn1:
			mPop.showAsDropDown(btn1);
			break;
		case R.id.btn2:
			mPop.showAsDropDown(btn2,290,-50);
			break;
		default:
			break;
		}
	}
```
