---
layout: post
title: react-navigation重复点击多次跳转的解决方案
date: 2017/12/13 20:46:25
feature-img: "assets/img/pexels/desk-messy.jpeg"
thumbnail: "assets/img/thumbnails/desk-messy.jpeg"
categories: [ReactNative]
tags: [react-native, react-navigation, 快速点击, 重复加载]
---
## 废话
- 在react-native@0.44版本之后，官方废弃了之前的导航Navigator，用react-navigation 替代
- react-natvigation于2017年1月份开源，在3个月时间内，GitHub上star数达4000+，备受推崇，由于其性能体验堪比原生，而且使用方便，最后被FB钦点为“御用导航”
- 但是在使用过程中还是发现了一个问题：在触发页面跳转的View上 重复、快速点击时，即将被加载的页面会多次被加载（*感谢测试小姐姐丧心病狂的操作*），症状如下图
![01.gif](http://upload-images.jianshu.io/upload_images/3161942-a0fc426d042f7fb1.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
<!--more-->

### 分析问题

经过观察发现，在onPress事件执行后会触发`navigation.navigate(...)`方法，加载新的页面。
但是当页面加载缓慢时，多余的点击会多次触发该事件，导致页面重复加载

**看源码**
*位置：../node_modules/react-navigation/src/addNavigationHelper.js*

```javascript
......
navigate: (
    routeName: string,
    params?: NavigationParams,
    action?: NavigationNavigateAction
): boolean =>
    navigation.dispatch(
        NavigationActions.navigate({ routeName, params, action })
    ),
.....
```
显然，页面跳转时，并未对事件进行控制，只要触发，就会加载新的页面
### 解决方案
既然源码未加控制，我们就手动加上，目前思路有2种:

- **普通版** 在`onPress`事件处控制，第一次点击后，加上延时，禁止之后的点击操作，但是需要每个点击事件都添加
- **进阶版** 直接修改源码，给`navigation.dispatch`加延时，一劳永逸

## 普通版

### 在`constructor`中初始化一个记录是否等待的`state`

```javascript
constructor(props) {
    super(props)
    this.state = {
        waiting: false,//防止多次重复点击
    }
}
```

### 利用`this.state.waiting`控制`TouchableOpacity`的`disabled`属性

```javascript
<TouchableOpacity
    disabled={this.state.waiting}
    onPress={() => this.repeatClick(this.props.navigation)}
>
    <Text style={ {padding: 10, color: 'red'}} >goto detail page</Text>
</TouchableOpacity>
...
repeatClick(navigation){
    this.setState({waiting: true});
    /*-------这中间写你需要实现的逻辑------------*/
    navigation.navigate('Detail')
    /*-------这中间写你需要实现的逻辑------------*/
    setTimeout(()=> {
        this.setState({waiting: false})
    }, 3000);//设置的时间间隔根据实际需要
}
```

### 效果展示

![03.gif](http://upload-images.jianshu.io/upload_images/3161942-57e4289b1a6a5839.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 进阶版

### 修改源码

*位于：../node_modules/react-navigation/src/addNavigationHelper.js*
此次修改基于`"react-navigation": "^1.0.0-beta.27"`，
修改后的代码如下：

```javascript
......
......
export default function<S: {}>(
  navigation: NavigationProp<S>
): NavigationScreenProp<S> {
  /*  ------------此处为添加的代码--------- */
  let debounce = true;//  定义判断变量
  /*  ------------此处为添加的代码--------- */
  return {
    ...navigation,
    goBack: (key?: ?string): boolean => {
      let actualizedKey: ?string = key;
      if (key === undefined && navigation.state.key) {
        invariant(
          typeof navigation.state.key === 'string',
          'key should be a string'
        );
        actualizedKey = navigation.state.key;
      }
      return navigation.dispatch(
        NavigationActions.back({ key: actualizedKey })
      );
    },
    navigate: (
      routeName: string,
      params?: NavigationParams,
      action?: NavigationNavigateAction
  /*  ------------此处为修改后的的代码--------- */
    ): boolean =>{
      if (debounce) {
        debounce = false;
        navigation.dispatch(
          NavigationActions.navigate({
            routeName,
            params,
            action,
          }),
        );
        setTimeout(
          () => {
            debounce = true;
          },
          5000,
        );
        return true;
      }
      return false;
    },
  /*  ------------此处为修改后的的代码--------- */
......
......
```

此时onPress事件无需再加控制

```javascript
<TouchableOpacity
    // disabled={this.state.waiting}
    onPress={() => this.props.navigation.navigate('Detail')}
>
    <Text style={ {padding: 10, color: 'red'}}>goto detail page</Text>
</T
```
### 看效果

![03.gif](http://upload-images.jianshu.io/upload_images/3161942-ea3fd2e66995fc61.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 本文结束，欢迎大家加群共同学习
**QQ群：672509442**

![😊😊😊😊](http://upload-images.jianshu.io/upload_images/3161942-5d817b58c736e47d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



