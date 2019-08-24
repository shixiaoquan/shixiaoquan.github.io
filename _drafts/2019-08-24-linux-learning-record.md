---
layout: post
title:  "Linux Learning Record"
date:   2019-08-22 23:41
categories: DB
---

### 查看 Linux 版本信息

* `uname -a`

```bash
[root@VM_0_6_centos ~]# uname -a
Linux VM_0_6_centos 3.10.0-514.26.2.el7.x86_64 #1 SMP Tue Jul 4 15:04:05 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
```

* `cat /proc/version`

```bash
[root@VM_0_6_centos ~]# cat /proc/version
Linux version 3.10.0-514.26.2.el7.x86_64 (builder@kbuilder.dev.centos.org) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-11) (GCC) ) #1 SMP Tue Jul 4 15:04:05 UTC 2017
```

### centos 检查是否安装了 MySQL

一.验证mysql是否安装

1. whereis mysql：如果安装了mysql就会显示mysql安装的地址
2. which mysql:查看文件的运行地址
3. chkconfig --list mysqld：没有安装则显示在mysqld服务中读取信息时出错,没有那个文件或目录
4. service mysqld start ：没有安装则显示未被识别的服务
5. rpm -e mysql：没有安装则显示未被安装
6. yum list installed mysql* 安装前看是否安装过mysql

![好图镇楼](/assets/img/nice_draw.jpg)
