---
layout: post
title: 嵌套ScrollView解决方案
date: 2018/03/14 13:31:11
feature-img: "assets/img/pexels/awesome-picture-3915112.jpg"
thumbnail: "assets/img/thumbnails/awesome-picture-3915112.jpg"
categories: [React Native]
tags: [react-native, scrollview, 嵌套]
---

### 场景
虽然设计上不赞成使用ScrollView进行嵌套，毕竟控制多个ScrollView的滑动事件是个坑，但是有时候还是架不住PM的需求😫

既然这样就只能想办法解决了

#### 思路
ScrollView嵌套以后，必然会发生滑动事件冲突，我们只要每次只允许一个ScrollView可以滑动，应该就能避免冲突，嗯 就是这样

#### 实现
ScrollView有一个scrollEnabled属性，可以用于控制ScrollView是否可以滑动，只要将其设置为`false`就能禁止其滑动操作

既然这样我们就用`state`来控制`scrollEnabled`，
```javascript
scrollEnabled={this.state.enabled}
```
滑动上面的一个ScrollView的时候，就禁止底层ScrollView的滑动
```javascript
this.setState({enabled: false})
```

### 实例

#### code

```javascript
import React, { Component } from 'react';
import { View, ScrollView } from 'react-native';

export default class App extends Component {
  constructor() {
    super();
    this.state = {
	   enabled:true
    };
  }
  
  render() {
  return (
    <ScrollView scrollEnabled={this.state.enabled}>
      <View style={ {height:600,backgroundColor:'violet'}}></View>
      <View style={ { height: 2000, backgroundColor: 'red' }} >
      <ScrollView
        onTouchStart={(ev) => {this.setState({enabled:false }); }}
        onMomentumScrollEnd={(e) => { this.setState({ enabled:true }); }}
        onScrollEndDrag={(e) => { this.setState({ enabled:true }); }}
        style={ { margin: 10, maxHeight: 200 }}
    >
        <View style={ { height: 200, backgroundColor: 'blue' }} />
        <View style={ { height: 200, backgroundColor: 'pink' }} />
	     <View style={ { height: 200, backgroundColor: 'blue' }} />
        <View style={ { height: 200, backgroundColor: 'pink' }} />
        <View style={ { height: 200, backgroundColor: 'blue' }} />
        <View style={ { height: 200, backgroundColor: 'pink' }} />
        <View style={ { height: 200, backgroundColor: 'blue' }} />
        <View style={ { height: 200, backgroundColor: 'pink' }} />
        <View style={ { height: 200, backgroundColor: 'blue' }} />
        <View style={ { height: 200, backgroundColor: 'pink' }} />
        <View style={ { height: 200, backgroundColor: 'blue' }} />
        <View style={ { height: 200, backgroundColor: 'pink' }} />
      </ScrollView>
      </View>
    </ScrollView>
  );
}
}
```

#### 效果

![nestedscrollview]({{ site.url }}/assets/img/postpics/nestedscrollview.gif)
