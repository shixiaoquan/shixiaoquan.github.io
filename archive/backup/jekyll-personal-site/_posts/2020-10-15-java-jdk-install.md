---
layout: post
title:  "基于 CentOS，JDK安装"
date:   2020-10-15 23:41
categories: Java
---

使用 yum 安装
## 查看 Java 可安装列表
```
🙈: yum -y list java*
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
Available Packages
java-1.6.0-openjdk.x86_64                                    1:1.6.0.41-1.13.13.1.el7_3                     base
....
```
## 指定版本安装
```
🙈: yum install java-1.8.0-openjdk.x86_64
```
## 查看 Java 版本
```
🙈: java -version
openjdk version "1.8.0_262"
OpenJDK Runtime Environment (build 1.8.0_262-b10)
OpenJDK 64-Bit Server VM (build 25.262-b10, mixed mode)
```
## 通过yum安装的默认路径为：/usr/lib/jvm，查看一下
```
🙈: ls -al /usr/lib/jvm
total 12
drwxr-xr-x   3 root root 4096 Oct 16 00:02 .
dr-xr-xr-x. 41 root root 4096 Oct 16 00:02 ..
drwxr-xr-x   3 root root 4096 Oct 16 00:02 java-1.8.0-openjdk-1.8.0.262.b10-0.el7_8.x86_64
lrwxrwxrwx   1 root root   21 Oct 16 00:02 jre -> /etc/alternatives/jre
lrwxrwxrwx   1 root root   27 Oct 16 00:02 jre-1.8.0 -> /etc/alternatives/jre_1.8.0
lrwxrwxrwx   1 root root   35 Oct 16 00:02 jre-1.8.0-openjdk -> /etc/alternatives/jre_1.8.0_openjdk
lrwxrwxrwx   1 root root   51 Oct 16 00:02 jre-1.8.0-openjdk-1.8.0.262.b10-0.el7_8.x86_64 -> java-1.8.0-openjdk-1.8.0.262.b10-0.el7_8.x86_64/jre
lrwxrwxrwx   1 root root   29 Oct 16 00:02 jre-openjdk -> /etc/alternatives/jre_openjdk
```
## 配置环境变量
```
🙈: vim bash_profile
```
加入一下内容：
```
#set java environment
JAVA_HOME=/usr/lib/jvm/jre-openjdk
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME CLASSPATH PATH
```
快速生效
```
🙈: source .bash_profile
```
