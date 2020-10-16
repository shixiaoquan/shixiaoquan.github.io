---
layout: post
title:  "基于 CentOS，MySql 的管理"
date:   2020-10-15 15:41
categories: DB
---

## 启动及关闭 MySQL 服务器

首先，我们需要通过以下命令来检查MySQL服务器是否启动：
```
ps -ef | grep mysqld
```
如果MySql已经启动，以上命令将输出mysql进程列表， 如果mysql未启动，你可以使用以下命令来启动mysql服务器:
```
root@host# cd /usr/bin
./mysqld_safe &
```
如果你想关闭目前运行的 MySQL 服务器, 你可以执行以下命令:
```
root@host# cd /usr/bin
./mysqladmin -u root -p shutdown
Enter password: ******
```

## MySQL 用户设置
### 先登录数据库
```
root@host# mysql -u root -p
Enter password:*******
mysql> use mysql;
Database changed
```
### 创建用户
- 创建用户 ls
```
mysql> create user ls identified by 'ls123123';
Query OK, 0 rows affected (0.00 sec)
```
ls是用户名；%表示所有 IP 都可访问；ls123123 是密码
- 给用户授权
```
mysql> grant all privileges on *.* to ls@'%' identified by 'ls123123';
Query OK, 0 rows affected (0.00 sec)
```

- 释放
```
mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```

### 删除用户
```
drop user zhangsan@'%';
```
drop user命令会删除用户以及对应的权限，执行命令后你会发现mysql.user表和mysql.db表的相应记录都消失了。

### 修改密码
```
update mysql.user set password = password('zhangsannew') where user = 'zhangsan' and host = '%';
flush privileges;
```
### 修改 root 密码
- 用SET PASSWORD命令 
首先登录MySQL。
```
mysql> set password for root@localhost = password('123'); 
```
- 用mysqladmin 
```
mysqladmin -uroot -proot123456 password root123123
```

### 常用命令组
创建用户并授予指定数据库全部权限：适用于Web应用创建MySQL用户
```
create user zhangsan identified by 'zhangsan';
grant all privileges on zhangsanDb.* to zhangsan@'%' identified by 'zhangsan';
flush  privileges;
```
创建了用户zhangsan，并将数据库zhangsanDB的所有权限授予zhangsan。如果要使zhangsan可以从本机登录，那么可以多赋予localhost权限：
```
grant all privileges on zhangsanDb.* to zhangsan@'localhost' identified by 'zhangsan';
```

## /etc/my.cnf 文件配置
一般情况下，你不需要修改该配置文件，该文件默认配置如下：

```
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.6/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

# Recommended in standard MySQL setup
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
```
在配置文件中，你可以指定不同的错误日志文件存放的目录，一般你不需要改动这些配置。

## 管理MySQL的命令
以下列出了使用Mysql数据库过程中常用的命令：
* USE 数据库名 :
选择要操作的Mysql数据库，使用该命令后所有Mysql命令都只针对该数据库。
```
mysql> use RUNOOB;
Database changed
```
* SHOW DATABASES:
列出 MySQL 数据库管理系统的数据库列表。
```
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| RUNOOB             |
| cdcol              |
| mysql              |
| onethink           |
| performance_schema |
| phpmyadmin         |
| test               |
| wecenter           |
| wordpress          |
+--------------------+
10 rows in set (0.02 sec)
```
- SHOW TABLES:
显示指定数据库的所有表，使用该命令前需要使用 use 命令来选择要操作的数据库。
```
mysql> use RUNOOB;
Database changed
mysql> SHOW TABLES;
+------------------+
| Tables_in_runoob |
+------------------+
| employee_tbl     |
| runoob_tbl       |
| tcount_tbl       |
+------------------+
3 rows in set (0.00 sec)
```
* SHOW COLUMNS FROM 数据表:
显示数据表的属性，属性类型，主键信息 ，是否为 NULL，默认值等其他信息。
```
mysql> SHOW COLUMNS FROM runoob_tbl;
+-----------------+--------------+------+-----+---------+-------+
| Field           | Type         | Null | Key | Default | Extra |
+-----------------+--------------+------+-----+---------+-------+
| runoob_id       | int(11)      | NO   | PRI | NULL    |       |
| runoob_title    | varchar(255) | YES  |     | NULL    |       |
| runoob_author   | varchar(255) | YES  |     | NULL    |       |
| submission_date | date         | YES  |     | NULL    |       |
+-----------------+--------------+------+-----+---------+-------+
4 rows in set (0.01 sec)
```
* SHOW INDEX FROM 数据表:显示数据表的详细索引信息，包括PRIMARY KEY（主键）。
```
mysql> SHOW INDEX FROM runoob_tbl;
+------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table      | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| runoob_tbl |          0 | PRIMARY  |            1 | runoob_id   | A         |           2 |     NULL | NULL   |      | BTREE      |         |               |
+------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
1 row in set (0.00 sec)
```
* SHOW TABLE STATUS [FROM db_name] [LIKE 'pattern'] \G:
该命令将输出Mysql数据库管理系统的性能及统计信息。
```
mysql> SHOW TABLE STATUS  FROM RUNOOB;   # 显示数据库 RUNOOB 中所有表的信息

mysql> SHOW TABLE STATUS from RUNOOB LIKE 'runoob%';     # 表名以runoob开头的表的信息
mysql> SHOW TABLE STATUS from RUNOOB LIKE 'runoob%'\G;   # 加上 \G，查询结果按列打印
```
