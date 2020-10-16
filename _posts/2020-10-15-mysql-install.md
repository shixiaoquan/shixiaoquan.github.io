---
layout: post
title:  "基于CentOS，安装MySql"
date:   2020-10-15 14:41
categories: DB
---

先记住几个命令
* mysqld is the server executable (one of them)   #服务执行工具    
* mysql is the command line client  # 客户端工具   查询用
* mysqladmin is a maintainance or administrative utility  # 运维和管理工具

## 安装MySQL

### 下载安装包，然后使用 yum 安装

在 Centos7 系统下使用 yum 命令安装 MySQL，需要注意的是 CentOS 7 版本中 MySQL数据库已从默认的程序列表中移除，所以在安装前我们需要先去官网下载 Yum 资源包，下载地址为：<https://dev.mysql.com/downloads/repo/yum/>

```
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum update
yum install mysql-server
```

### 权限设置
```
chown mysql:mysql -R /var/lib/mysql
```

### 初始化 MySQL
```
mysqld --initialize
```

### 启动 MySQL

```
systemctl start mysqld
```

### 查看MySQL运行状态
```
systemctl status mysqld
```

## 验证 MySQL 的安装
```
[root@host]# mysqladmin --version
```
linux上该命令将输出以下结果，该结果基于你的系统信息：
```
mysqladmin  Ver 8.42 Distrib 5.6.49, for Linux on x86_64
```

## 使用 MySQL Client(Mysql客户端) 执行简单的SQL命令
你可以在 MySQL Client(Mysql客户端) 使用 mysql 命令连接到 MySQL 服务器上，默认情况下 MySQL 服务器的登录密码为空，所以本实例不需要输入密码。

命令如下：
```
[root@host]# mysql
```
以上命令执行后会输出 mysql>提示符，这说明你已经成功连接到Mysql服务器上，你可以在 mysql> 提示符执行SQL命令：
```
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
3 rows in set (0.01 sec)
```

## Mysql安装后需要做的
Mysql安装成功后，默认的root用户密码为空，你可以使用以下命令来创建root用户的密码：
```
[root@host]# mysqladmin -u root password "new_password";
```
现在你可以通过以下命令来连接到Mysql服务器：
```
[root@host]# mysql -u root -p
Enter password:*******
```
**注意：** 在输入密码时，密码是不会显示了，你正确输入即可。



