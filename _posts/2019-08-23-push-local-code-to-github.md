---
layout: post
title:  "Push Local Code To Github"
date:   2019-08-23 23:44
categories: OPS
---

本地创建项目后想上传到 GitHub ,该如何操作

* 在本地初始化 Git

```bash
git init
```

初始化完成后,会产生一个 .git 目录

* Add 和 Commit

```bash
git add .
git commit -m "first init"
```

* 在 GitHub 上创建一个 repo

略过

* 将本地代码关联到 GitHub

```bash
git remote add origin (GitHub repo 地址)
```

* push

```bash
git push
```
