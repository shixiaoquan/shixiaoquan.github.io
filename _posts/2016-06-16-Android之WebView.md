---
layout: post
title: Android之WebView
feature-img: "assets/img/pexels/Android-Privacy.jpg"
thumbnail: "assets/img/thumbnails/Android-Privacy.jpg"
date: 2016/6/16 20:46:25
categories: [Android]
tags: [android, webwiew]
---
## 简介
WebView是Android中用于加载web页面的控件

### 优点

 - 可以直接内嵌到App中用于显示和渲染web页面
 - 可以直接用html文件（网络上或本地assets中）作布局

<!--more-->
### 配置权限
android:name="android.permission.INTERNET"
如果需要定位功能，还需要配置下面两个权限
android:name="android.permission.ACCESS_FINE_LOCATION"
android:name="android.permission.ACCESS_COARSE_LOCATION"

### 两个实现方法

 - setWebClient：主要处理解析，渲染网页等浏览器做的事情
 - setWebChromeClient：辅助WebView处理Javascript的对话框，网站图标，网站title，加载进度等
WebViewClient就是帮助WebView处理各种通知、请求事件的。

## 加载网页字符串
使用loadData()加载一段HTML内容

```java
mWebView = (WebView) findViewById(R.id.id_webView);
String summary = "<html><body>You scored <b>192</b> points.</body></html>";
mWebView.loadData(summary, "text/html", null);
```

如下图：

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-c0ac92045cbe815c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 加载网络资源
使用loadUrl()加载网络url

```java
String htmlurl = "http://baidu.com";
mWebView.loadUrl(htmlurl);
```
加载时，会自动跳转到系统浏览器打开，如下图：

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-94d77c0009b7d9ff?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

而我们使用WebView就是为了展示网页，还跳转个鸡毛啊，为了解决这个问题，就要使用WebViewClient这个Class

```java
mWebView.setWebViewClient(new WebViewClient() {
	public boolean shouldOverrideUrlLoading(WebView view, String url){
		//  重写此方法表明点击网页里面的链接还是在当前的webview里跳转，不跳到浏览器那边
	    view.loadUrl(url);
	    return true;
	}
});
```

效果如下图：

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-957deeb6d00c68fb?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 实例
创建Android项目名曰：WebViewTest
添加一个Activity，MainActivity
xml文件如下

```java
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    >
<WebView
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:id="@+id/webView"
    />
</LinearLayout>
```

java代码如下：

```java
package com.webviewurl.test;

import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.GeolocationPermissions.Callback;
import android.graphics.Bitmap;

public class MainActivity extends Activity {
 private static final String TAG = "MainActivity";
    private WebView webView;
    private static final String htmlurl="http://baidu.com";
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        webView = (WebView)this.findViewById(R.id.webView);
		WebSettings settings = webView.getSettings();
		//设置Webview可以调用javascript
        settings.setJavaScriptEnabled(true);
        //设置webview可以调用地理位置信息
		settings.setGeolocationEnabled(true);
		//设置webview调用地理位置信息的缓存路径
				settings.setGeolocationDatabasePath(getFilesDir().getPath());
		//配置获取设备位置信息的权限
        webView.setWebChromeClient(new WebChromeClient() {
        	@Override
        	public void onGeolocationPermissionsShowPrompt(String origin,Callback callback) {
        		callback.invoke(origin, true, false);
        		super.onGeolocationPermissionsShowPrompt(origin, callback);
        	}
        });
		webView.setWebViewClient(new WebViewClient() {
			public boolean shouldOverrideUrlLoading(WebView view, String url){
				//  重写此方法表明点击网页里面的链接还是在当前的webview里跳转，不跳到浏览器那边
			    view.loadUrl(url);
			    return true;
			}
		});

		webView.addJavascriptInterface(new ContactPlugin(), "contact");
        webView.loadUrl(htmlurl);
    }
}
```

### 加载本地资源
方法同上，只是加载方法不同

```java
webView.loadUrl("file:///android_asset/test.html");
```
