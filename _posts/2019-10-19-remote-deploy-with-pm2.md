---
layout: post
title:  "使用 pm2 进行远程自动化部署"
date:   2019-10-19 22:46
categories: OPS
---

pm2（process manager）是一个进程管理工具，维护一个进程列表，可以用它来管理你的node进程，负责所有正在运行的进程，并查看node进程的状态，也支持性能监控，负载均衡等功能。

## pm2 的用处

* 监听文件变化，自动重启程序
* 支持性能监控
* 负载均衡
* 程序崩溃自动重启
* 服务器重新启动时自动重新启动
* 自动化部署项目

## 安装

```bash
npm install pm2 -g
```

## 常用命令

### 启动

```bash
pm2 start app.js
```

### 启动进程并指定应用的程序名

```bash
pm2 start app.js --name application1
```

### 集群模式启动

```bash
# -i 表示 number-instances 实例数量
# max 表示 PM2将自动检测可用CPU的数量 可以自己指定数量
pm2 start start.js -i max
```

### 添加进程监视

```bash
# 在文件改变的时候会重新启动程序
pm2 start app.js --name start --watch
```

### 列出所有进程

```bash
pm2 list
pm2 ls # 简写
```

### 删除进程

```bash
# pm2 delete [appname] | id
pm2 delete app  # 指定进程名删除
pm2 delete 0    # 指定进程id删除
pm2 delete all  # 删除所有进程
```

### 查看某个进程的详细情况

```bash
pm2 describe app
```

### 重新启动

```bash
pm2 restart app.js
```

### 查看进程的资源消耗情况

```bash
pm2 monit
```

### 查看进程日志

```bash
pm2 logs app  # 查看该名称进程的日志
pm2 logs all  # 查看所有进程的日志
```

### 设置开机启动

开启启动设置，此处是CentOS系统，其他系统替换最后一个选项（可选项：ubuntu, centos, redhat, gentoo, systemd, darwin, amazon）

```bash
pm2 startup centos
```

然后按照提示需要输入的命令进行输入

最后保存设置

```bash
pm2 save
```

## 远程部署

### 准备工作

* 服务器安装 pm2
* 服务器安装并配置 git, 确保可以从指定的 repo 拉取到最新的代码
* 可以免密登录到服务器(这个不是必须的, 但是实际工作中,必然要设置, 不然每次部署都要输入好几次密码, 会疯掉的)

### pm2 的远程部署配置

详细配置可参考[官方文档-deploy](http://pm2.keymetrics.io/docs/usage/deployment/)
ecosystem.json

```json
{
  "apps": [
    {
      "name": "lottery-api",
      "script": "dist/server.js",
      "env": {
        "COMMON_VARIABLE": "true"
      },
      "env_production": {
        "NODE_ENV": "production"
      }
    }
  ],
  "deploy": {
    "production": {
      "user": "root",
      "host": [
        "xxx.xxx.xxx.xxx"
      ],
      "port": 22,
      "ref": "origin/master",
      "repo": "git@gitee.com:shiquan/lottery-api.git",
      "ssh_options": "StrictHostKeyChecking=no",
      "path": "/root/workspace/lottery/lottery-api",
      "pre-deploy": "git fetch --all ",
      "post-deploy": "npm install && pm2 startOrRestart ecosystem.json --env production",
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

首次部署

```bash
pm2 deploy deploy.yaml production setup
```

部署完成后，既可登陆服务器查看配置的目录下是否从git上拉取了项目

再次部署

```bash
pm2 deploy deploy.yaml production upddate
```

这种操作也适合前端代码部署
