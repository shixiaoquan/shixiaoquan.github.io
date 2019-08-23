---
layout: post
title:  "MySql Learning Record"
date:   2019-08-22 23:41
categories: DB
---

## Login with root

```bash
mysql -u root -p
```

输入默认密码]

## Add User

### 创建一个未授权的用户

* 连接数据库

```bash
🙈: mysql -u root -p
Enter password:*******
mysql> use mysql;
Database changed
```

* 创建一个未授权的用户

```bash
mysql> CREATE USER 'test'@'localhost' IDENTIFIED BY 'test123';
Query OK, 0 rows affected (0.08 sec)
```

* 给用户授权

用户权限有很多, 例如 SELECT，INSERT，UPDATE等，如果授予用户所有权限,则使用 ALL, 如下

```bash
mysql> GRANT ALL ON litemall.* TO 'test'@'localhost';
Query OK, 0 rows affected (0.09 sec)
```

注意:

1. 授权之后需要用户重连MySQL，才能获取相应的权限。
2. 用以上命令授权的用户不能给其它用户授权，如果想让该用户可以授权，用以下命令:

```bash
GRANT privileges ON databasename.tablename TO 'username'@'host' WITH GRANT OPTION;
```

### 设置与更改用户密码

* 如果是 root 用户

```bash
SET PASSWORD FOR 'test'@'localhost' = PASSWORD('test1234');
```

* 如果是当前用户

```bash
SET PASSWORD = PASSWORD("test1234");
```

示例

```bash
SET PASSWORD FOR 'test'@'localhost' = PASSWORD("test1234");
```

### 撤销用户权限

```bash
REVOKE privilegexxx ON databasenamexxx.tablenamexxx FROM 'test'@'localhost';
```

示例

```bash
REVOKE SELECT ON *.* FROM 'test'@'localhost';
```

![好图镇楼](/assets/img/nice_draw.jpg)
