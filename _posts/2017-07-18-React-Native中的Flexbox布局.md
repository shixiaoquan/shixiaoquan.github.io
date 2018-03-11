---
layout: post
title: React-Native中的Flexbox布局
feature-img: "assets/img/pexels/kwaaow.jpeg"
thumbnail: "assets/img/thumbnails/kwaaow.jpeg"
date: 2017/7/18 10:06:00
categories: [React Native]
tags: [react-native, flexbox]
---
# 简介
我们在React Native中使用flexbox规则来指定某个组件的子元素的布局。Flexbox可以在不同屏幕尺寸上提供一致的布局结构。相对于Native开发的布局更加快捷方便。

Flexbox使用flexDirection、alignItems和 justifyContent三个样式属性就已经能满足大多数布局需求

# flexDirection
flexDirection可以决定zu jian组件布局的主轴，子元素会沿着主轴排列，或水平或垂直。

<!--more-->
*flexDirection的默认值是竖直轴（column）方向*
## column（默认）

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ {flex: 1}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-670aabe0e85dd1a3?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
## column-reverse

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ {flex: 1, flexDirection: 'column-reverse'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-cb3d6639467be368?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## row

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ {flex: 1, flexDirection: 'row'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);

```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-efb0367e1bbf2133?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## row-reverse

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ {flex: 1, flexDirection: 'row-reverse'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);

```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-d2b7e3dfadd9df26?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# justifyContent
在组件的style中指定justifyContent可以决定其子元素沿着主轴的排列方式。子元素是应该靠近主轴的起始端还是末尾段分布呢？亦或应该均匀分布？对应的这些可选项有：flex-start、center、flex-end、space-around以及space-between。

## flex-start

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column',justifyContent: 'flex-start'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-bdde7778b91f4123?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## center

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column',justifyContent: 'center'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-f98ec8cd36ba4aa2?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## flex-end

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column',justifyContent: 'flex-end'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-de752c9626edfdc1?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## space-around

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column',justifyContent: 'space-around'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-bb90cba7698f5541?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## space-between

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column',justifyContent: 'space-between'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-59bfdc06f48105b8?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# alignItems

在组件的style中指定alignItems可以决定其子元素沿着次轴（与主轴垂直的轴，比如若主轴方向为row，则次轴方向为column）的排列方式。子元素是应该靠近次轴的起始端还是末尾段分布呢？亦或应该均匀分布？对应的这些可选项有：flex-start、center、flex-end以及stretch。

## flex-start

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column', justifyContent: 'center', alignItems: 'flex-start'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-6aacf1d5e558f677?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## center


```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-9681ead971266165?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## flex-end

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column', justifyContent: 'center', alignItems: 'flex-end'}}>
                <View style={ {width: 50, height: 50, backgroundColor: 'red'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'green'}} />
                <View style={ {width: 50, height: 50, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-4a171984757edf89?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## stretch

**注意：**

要使stretch选项生效的话，子元素在次轴方向上不能有固定的尺寸。以下面的代码为例：只有将子元素样式中的width: 50去掉之后，alignItems: 'stretch'才能生效。

```javascript
export default class AsomeProject extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={ { flex: 1, flexDirection: 'column', justifyContent: 'center', alignItems: 'stretch'}}>
                <View style={ {height: 50, backgroundColor: 'red'}} />
                <View style={ {height: 150, backgroundColor: 'green'}} />
                <View style={ {height: 100, backgroundColor: 'blue'}} />
            </View>
        );
    }
}

AppRegistry.registerComponent('AsomeProject', () => AsomeProject);
```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/3161942-96078c32d83d3fda?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
