---
layout: post
title:  "基于 CentOS，Maven 安装"
date:   2020-10-16 00:41
categories: Maven
---

## 下载安装包
```
🙈: wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
```

## 使用 yum 安装
```
🙈: yum -y install apache-maven
```
## 查看版本
```
🙈: mvn -v
```
