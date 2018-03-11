---
layout: post
title: React-Native中Android双击Back键退出应用(已废弃)
date: 2016/2/17 20:46:25
feature-img: "assets/img/pexels/pressbackbutton.jpg"
thumbnail: "assets/img/thumbnails/pressbackbutton.jpg"
categories: [React Native]
tags: [react-native, android, 双击back键]
---

### 废话
这是个很常用的小功能，做开发很实用哟
### 先上代码
<!--more-->

```javascript
import {......, BackAndroid, ToastAndroid} from 'react-native';

componentWillMount(){
    BackAndroid.addEventListener('hardwareBackPress', this.onBackAndroid);
}
componentWillUnmount() {
    BackAndroid.removeEventListener('hardwareBackPress', this.onBackAndroid);
}
onBackAndroid = () => {
    if (this.lastBackPressed && this.lastBackPressed + 2000 >= Date.now()) {
        //最近2秒内按过back键，可以退出应用。
        return false;
    }
    this.lastBackPressed = Date.now();
    ToastAndroid.show('再按一次退出应用', ToastAndroid.SHORT);
    return true;
};
```

在componentWillMount()和componentWillUnmount()方法中监听back点击事件，然后自定义onBackAndroid()方法，监听两次点击的时间间隔

### 上个效果图
自己写的demo中用到，其他的东西请自行忽略

![Paste_Image.png](http://upload-images.jianshu.io/upload_images/3161942-d52a5038754f691e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
