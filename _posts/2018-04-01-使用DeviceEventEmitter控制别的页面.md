---
layout: post
title: 使用 DeviceEventEmitter 控制别的页面
date: 2018/04/01 10:44:31
feature-img: "assets/img/pexels/deviceeventemiter.png"
thumbnail: "assets/img/thumbnails/deviceeventemiter.png"
categories: [React Native]
tags: [react-native, DeviceEventEmitter]
---

在 native 开发中，我们可以使用广播实现事件的订阅和事件的触发，从而实现不在该页面但是可以调用该页面的方法。

在 React Native 中，我们也可以使用 DeviceEventEmitter 实现类似的功能

该方法是官方 API，调用时，直接引用就行了。

```javascript
import {
    View,
    DeviceEventEmitter
} from 'react-native';
```

如果我们要实现
- 在A页面：点击按钮传递参数到B页面
- 在B页面：使用接收的参数刷新列表

**操作如下**

- 在B页面实现事件的监听，假设我们将事件命名为 refreshListListener

```javascript
// 加载页面时，添加事件监听
componentDidMount() {
    this.emitter =     
    DeviceEventEmitter.addListener('refreshListListener', (param) => {
        refreshList(param)
    });
}
...
// 页面卸载时，删除事件监听
componentWillUnmount() {
    this.emitter.remove()
}
```

- 在A页面中，发送消息，触发B页面订阅的事件

```javascript
<TouchableOpacity 
    onPress={() => {
        DeviceEventEmitter.emit('refreshListListener', {name: 'jerry', age: 100});
    }
}>
    <Text>刷新B页面的列表</Text>
</TouchableOpacity>
```

## 本文结束，欢迎大家加群共同学习

|![QQ群：672509442]({{ site.url }}/assets/img/postpics/QQGroupQR.png)|
| :-: |
|**QQ群：672509442**|
