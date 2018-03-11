---
title: Dialog系统功能
date: 2015/2/1 20:46:25
categories: Android
tags:
  - android
  - dialog
---
### **Icon、标题、消息、按钮**
Dialog的创建非常简单

```
AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
builder.create();
builder.show();
```

#### **Icon、标题、消息**
添加Icon、标题、消息的代码如下
<!--more-->

```
builder.setIcon(R.mipmap.luffy);
builder.setTitle("我是Title");
builder.setMessage("我是Message");
```
效果图
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-019f4abfe7ac6722?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
#### **按钮**
添加按钮的代码如下

```
builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Toast.makeText(MainActivity.this, "确定", Toast.LENGTH_SHORT).show();
                    }
                });
                builder.setNeutralButton("忽略", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Toast.makeText(MainActivity.this, "忽略", Toast.LENGTH_SHORT).show();
                    }
                });
                builder.setNegativeButton("取消", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Toast.makeText(MainActivity.this, "取消", Toast.LENGTH_SHORT).show();
                    }
                });
```
效果
[站外图片上传中...(image-b87ca0-1516253750082)]
### 自定义布局
首先自定义一个布局文件

```
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:src="@mipmap/luffy" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="我是要成为海贼王的男人"
        android:textSize="25dp" />
</LinearLayout>
```
效果如下：
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-0a404e41c14f6472?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在Dialog中添加View

```
View view = LayoutInflater.from(MainActivity.this).inflate(R.layout.layout_dialog,null);
AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
builder.setIcon(R.mipmap.luffy);
builder.setTitle("我是Title");
builder.setMessage("我是Message");
builder.setView(view);
```
效果如下
![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-f3707f9ffecbef7a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


