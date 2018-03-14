**博客来来回回换了好几次了，这次是我比较满意的版本**

- 导航中有文章分类
- 文章预览和详情页面都可以展示图片
- markdown中的图片可以调用本地静态资源（这一点太好了，再也不用担心图床迁移的问题了）
- jekyll引擎使用简单，对于以后的需求可以自己修改

### 2018-03-14
- 今天抽空把菜单栏的样式改了，之前的选中没有效果停留，并不知道当前所在的页面
- 使用jquery和scss完成
- 写了一篇文章，关于nested scrollview

### 2018-03-11
- 今天把之前写的所有的博客迁移过来了，麻烦的一笔哎，以后要考虑博客迁移的问题，最好不要换了
- 发现`Android`的分类有点多了，下一步得考虑下分类页面中的分页问题了

### 2018-03-10
- 昨天在`pages`和`_layout`中分别创建了每个分类的页面，这样导致代码重复太多，一点儿都不优雅
- 今天早上起来突然想到，可以将重复的代码放在`_include`中，每个只要使用相同的layout，然后各自引用重复的部分
- 虽然解决了代码重复的问题，但是还是没法配置化，待解决...
- 增加了程序人生的类别，以后要写一些生活和工作的感悟

### 2018-03-09
- 增加了文章分类功能，将类别列举着`navmenu`，但是由于静态页面无法实现传值，暂时只能针对每种类型创建相应的页面
- 但这样并不优雅，待解决

## 感谢
- [GitHubPage](https://pages.github.com/) 提供免费空间
- [Jekyll](https://jekyllrb.com/) 提供优秀的静态页面构建工具（[中文站](https://www.jekyll.com.cn/)）
- [Type on Strap](https://github.com/Sylhare/Type-on-Strap) 感谢作者（[Sylhare](https://github.com/Sylhare)）提供优秀的模版

## License

[The MIT License (MIT)](https://raw.githubusercontent.com/Sylhare/Type-on-Strap/master/LICENSE)
