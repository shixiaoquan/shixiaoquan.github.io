---
layout: post
title: PanResponder的使用总结
date: 2018/03/14 13:31:11
feature-img: "assets/img/pexels/awesome-picture-3915112.jpg"
thumbnail: "assets/img/thumbnails/awesome-picture-3915112.jpg"
categories: [React Native]
tags: [react-native, PanResponder]
---

### 简介
对于简单的 touch 事件，React Native有4个专门的 touch 组件进行处理

- TouchableHighlight
- TouchableNativeFeedback
- TouchableOpacity
- TouchableWithoutFeedback

他们可以绑定4种不同的响应方法

- onPress
- onPressIn
- onPressOut
- onLonePress

而对于手指滑动操作，利用上面的方法无法实现，这时就用到 gesture responder system

在React Native中，响应手势的基本单位是responder，具体来说，就是最常见的View组件。任何的View组件，都是潜在的responder，如果某个View组件没有响应手势操作，那是因为它还没有被“开发”。

将一个普通的View组件开发成为一个能响应手势操作的responder，非常简单，只需要按照React Native的gesture responder system的规范，在props上设置几个方法即可。具体如下：

View.props.onStartShouldSetResponder
View.props.onMoveShouldSetResponder
View.props.onResponderGrant
View.props.onResponderReject
View.props.onResponderMove
View.props.onResponderRelease
View.props.onResponderTerminationRequest
View.props.onResponderTerminate

这个是系统级别的手势相应，处理起来相对复杂，最常见的是使用 PanResponder

### PanResponder

PanResponder 是 React Native 实现的一套手势相应方法，与gesture responder system 比起来，PanResponder 方法的抽象成都更高，使用起来也更加方便

使用方法很简单，只要View.props中设置相应的方法即可

```javascript
panResponder = PanResponder.create({
    onStartShouldSetPanResponder: (evt, gestureState) => true,
    onMoveShouldSetPanResponder: (evt, gestureState) => true,
    onPanResponderGrant: (evt, gestureState) => {
        console.log('evt', evt)    
        console.log('gestureState', gestureState)
    },
    onPanResponderMove: (evt, gestureState) => {
        console.log('evt', evt)    
        console.log('gestureState', gestureState)
    },
    onPanResponderRelease: (evt, gestureState) => {
        console.log('evt', evt)    
        console.log('gestureState', gestureState)
    },
})
render() {
    <View style={styles.container}
        {...this.panResponder.panHandlers}
    > 
    ...
    </View>
}
```

简单说明5个方法

| 方法名 | 说明 |
| :-: | :-: |
| onStartShouldSetPanResponder | 负责处理用户通过触摸来激活一个 responser，如果返回值为 true，则表示这个 View 能够响应触摸手势被激活 |
| onMoveShouldSetPanResponder | 负责处理用户通过移动来激活一个 responser，如果返回值为 true，则表示这个 View 能够响应滑动手势被激活 |
| onPanResponderGrant | 如果组件被 responser 激活，则调用该方法 |
| onPanResponderMove | 用户滑动手指时，调用该方法 |
| onPanResponderRelease | 用户手指离开屏幕时，调用该方法 |

在5个方法中，我们能够使用的参数有2个，分别是 evt 和 gesture

| 参数 | 说明 |
| :-: | :-: |
| evt | 获取触摸的位置在被响应的 View 中的相对坐标，evt.nativeEvent.locationX 和 evt.nativeEvent.locationY（这个方法很实用） |
| gesture | dx/dy：手势进行到现在的横向/纵向相对位移<br> vx/vy：此刻的横向/纵向速度<br> numberActiveTouches：responder上的触摸的个数 |

一个简单的拖拽 View 的例子

```javascript
panResponder = PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onMoveShouldSetPanResponder: ()=> true,
      onPanResponderGrant: ()=>{
        this._top = this.state.top
        this._left = this.state.left
        this.setState({bg: 'red'})
      },
      onPanResponderMove: (evt,gs)=>{
        console.log(gs.dx+' '+gs.dy)
        this.setState({
          top: this._top+gs.dy,
          left: this._left+gs.dx
        })
      },
      onPanResponderRelease: (evt,gs)=>{
        this.setState({
          bg: 'white',
          top: this._top+gs.dy,
          left: this._left+gs.dx
      })}
    })

render() {
    return(
        <View
            {...this.panResponder.panHandlers}
            style={[styles.rect,{
                "backgroundColor": this.state.bg,
                "top": this.state.top,
                "left": this.state.left
            }]}
        >
        ...
        </View>
    )
}
```

![演示]({{ site.url }}/assets/img/postpics/panResponser.gif)

## 本文结束，欢迎大家加群共同学习

**QQ群：672509442**

![😊😊😊😊]({{ site.url }}/assets/img/postpics/QQGroupQR.png)
