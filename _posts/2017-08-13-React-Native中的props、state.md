---
layout: post
title: React-Native中的props、state
feature-img: "assets/img/pexels/blackmask.png"
thumbnail: "assets/img/thumbnails/blackmask.png"
date: 2017/8/13 21:19:28
categories: [React Native]
tags: [react-naive, state, props]
---
# 属性{ {
大多数组件在创建时就可以使用各种参数来进行定制。用于定制的这些参数就称为props（属性）。
## 原生组件的prop
以常见的基础组件Image为例，在创建一个图片时，可以传入一个名为source的prop来指定要显示的图片的地址，以及使用名为style的prop来控制其尺寸。

<!--more-->
```javascript
import React, { Component } from 'react';
import { AppRegistry, Image } from 'react-native';

class Bananas extends Component {
  render() {
    let pic = {
      uri: 'https://upload.wikimedia.org/wikipedia/commons/d/de/Bananavarieties.jpg'
    };
    return (
      <Image source={pic} style={ {width: 193, height: 110}} />
    );
  }
}

AppRegistry.registerComponent('Bananas', () => Bananas);
```

## 自定义组件的prop
自定义的组件也可以使用props。通过在不同的场景使用不同的属性定制，可以提高自定义组件的复用性。只需在render函数中引用this.props，然后按需处理即可。下面是一个例子：

```javascript
import React, { Component } from 'react';
import { AppRegistry, Text, View } from 'react-native';

class Greeting extends Component {
  render() {
    return (
      <Text>Hello {this.props.name}!</Text>
    );
  }
}

class LotsOfGreetings extends Component {
  render() {
    return (
      <View style={ {alignItems: 'center'}}>
        <Greeting name='Rexxar' />
        <Greeting name='Jaina' />
        <Greeting name='Valeera' />
      </View>
    );
  }
}

AppRegistry.registerComponent('LotsOfGreetings', () => LotsOfGreetings);
```

在Greeting组件中将name作为一个属性来定制，这样就能使用name这个属性来设置不同的问候语

效果图：

# 状态
一个组件可以通过props和state来进行控制，props在父组件中设置，一旦设置完毕，在其生命周期内就不再改变；对于那些需要时时变化的属性，我们使用state来进行控制。

假如我们需要制作一个简单的文字闪烁的效果，对于文字的大小、字体、颜色，可以使用props设置好，我们只需要实时控制文字的可见性即可，这就用到state。

```javascript
import React, { Component } from 'react';
import { AppRegistry, Text, View } from 'react-native';

class Blink extends Component {
  constructor(props) {
    super(props);
    this.state = { showText: true };

    // 每1000毫秒对showText状态做一次取反操作
    setInterval(() => {
      this.setState({ showText: !this.state.showText });
    }, 1000);
  }

  render() {
    // 根据当前showText的值决定是否显示text内容
    let display = this.state.showText ? this.props.text : ' ';
    return (
      <Text>{display}</Text>
    );
  }
}

class BlinkApp extends Component {
  render() {
    return (
      <View>
        <Blink text='I love to blink' />
        <Blink text='Yes blinking is so great' />
        <Blink text='Why did they ever take this out of HTML' />
        <Blink text='Look at me look at me look at me' />
      </View>
    );
  }
}

AppRegistry.registerComponent('BlinkApp', () => BlinkApp);
```
