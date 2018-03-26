---
layout: post
title: React Native 如何适配 iPhone X
date: 2018/03/26 19:54:10
feature-img: "assets/img/pexels/iphonex.png"
thumbnail: "assets/img/thumbnails/iphonex.png"
categories: [React Native]
tags: [react-native, iPhone X]
---

**使用SafeAreaView轻松更新和创建 iPhone X 布局**

![safeareaview]({{ site.url }}/assets/img/pexels/safeareaview.png)

在0.50.1版本中，React Native 团队介绍了一个新的API，用于处理全新的 iPhoneX 页面布局，这个 API 就是 SafeAreaView。

借助SafeAreaView，可以轻松更新现有的代码库与 iPhone X 进行集成。


下面就是一个示例：

```javascript
import {
  ...
  SafeAreaView
} from 'react-native';
class Main extends React.Component {
  render() {
    return (
      <SafeAreaView style={styles.safeArea}>
        <App />
      </SafeAreaView>
    )
  }
}
const styles = StyleSheet.create({
  ...,
  safeArea: {
    flex: 1,
    backgroundColor: '#ddd'
  }
})
```

SafeAreaView 的工作原理是设置一些与现有应用程序匹配的背景色，在上面的例子中，设置了背景色为浅灰色、 flex: 1, 我们只在 SafeAreaView 中包装我们的顶级UI组件，这样操作起来很方便。

正如在上面的截图中所见， SafeAreaView 已经和 React Navigation 进行了整合

如果您无法升级到较新版本的React Native，那么还有一个 JS 版本的 npm 模块可用，react-native-safe-area-view。
