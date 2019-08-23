---
layout: post
title:  "Linux Ubuntu Install Java、MySQL"
date:   2019-08-23 20:34
categories: OPS
---

安装 Java 分为安装 JRE 和 JDK, JRE 是 Java Runtime Environment, JDK 是 Java Develop Environment

### 检查 Java 是否安装

```bash
java -version
```

出现如下结果,表示 Java 未安装

```bash
Command 'java' not found, but can be installed with:

sudo apt install default-jre
sudo apt install openjdk-11-jre-headless
sudo apt install openjdk-8-jre-headless
```

出现类似如下信息,表示已经安装

```bash
openjdk version "11.0.4" 2019-07-16
OpenJDK Runtime Environment (build 11.0.4+11-post-Ubuntu-1ubuntu218.04.3)
OpenJDK 64-Bit Server VM (build 11.0.4+11-post-Ubuntu-1ubuntu218.04.3, mixed mode, sharing)
```

### 安装 JRE

```bash
sudo apt install default-jre
```

### 安装 JDK

```bash
sudo apt install default-jdk
```

### 安装 MySQL

```bash
sudo apt install mysql-server
```

安装完毕后, 检查 MySQL 状态

```bash
systemctl status service
```

```bash
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2019-08-23 12:50:35 UTC; 1min 2s ago
 Main PID: 9167 (mysqld)
    Tasks: 27 (limit: 1152)
   CGroup: /system.slice/mysql.service
           └─9167 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid

Aug 23 12:50:34 ip-172-31-43-249 systemd[1]: Starting MySQL Community Server...
Aug 23 12:50:35 ip-172-31-43-249 systemd[1]: Started MySQL Community Server.
```

已经启动

使用 root 用户登录,初始密码为空,直接按回车键就行

```bash
sudo mysql -u root -p

Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.27-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.
```

设置 root 账户权限和密码

```bash
GRANT ALL PRIVILEGES ON *.* TO root@localhost IDENTIFIED BY "MySQL123";
```

其中root@localhos，localhost就是本地访问，配置成%就是所有主机都可连接；

第二个'123456'为你给新增权限用户设置的密码，%代表所有主机，也可以是具体的ip；
