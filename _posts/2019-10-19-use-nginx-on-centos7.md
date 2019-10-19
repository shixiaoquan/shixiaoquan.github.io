---
layout: post
title:  "Nginx 在 ContOS7 上的使用"
date:   2019-10-19 18:21
categories: OPS
---

Nginx 读作 engine x， 是一个免费的、开源的、高性能的 HTTP 和反向代理服务，主要负责负载一些访问量比较大的站点。

Nginx 可以作为一个独立的 Web 服务，也可以用来给 Apache 或是其他的 Web 服务做反向代理。

相比于 Apache，Nginx 可以处理更多的并发连接，而且每个连接的内存占用的非常小。

## 安装

yum 库中没有 nginx 的安装包,但是 epel 中有,所以我们先安装  epel

下面所有操作都默认使用 root 账户操作

### 安装 epel

```bash
yum -y install epel-release
```

### 安装 nginx

```bash
yum -y install nginx
```

### nginx 常用操作

#### 设置开机启动

```bash
systemctl enable nginx
```

#### 关闭开机启动

```bash
systemctl disable nginx
```

#### 启动 nginx

```bahs
systemctl start nginx
```

#### 停止 nginx

```bahs
systemctl stop nginx
```

#### 重启 nginx

```bahs
systemctl restart nginx
```

#### 修改 nginx 配置后，重新加载

```bahs
systemctl reload nginx
```

#### 检查 nginx 的运行状态

```bash
systemctl status nginx
```

然后会输出类似如下内容:

```bash
nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; vendor preset: disabled)
   Active: active (running) since Sat 2019-10-19 18:30:38 CST; 9s ago
  Process: 19120 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
  Process: 19118 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
  Process: 19116 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
 Main PID: 19122 (nginx)
   CGroup: /system.slice/nginx.service
           ├─19122 nginx: master process /usr/sbin/nginx
           └─19123 nginx: worker process
```

### 打开相应的服务器端口

如果你的服务器开启了防火墙，则需要同时打开 80（HTTP）和 443（HTTPS）端口

通过下面的命令来打开这两个端口:

```bash
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --reload
```

### 验证 nginx 是否成功启动

打开 <http://服务器IP,> 如果显示默认的 nginx 欢迎页, 表示已经启动成功

![nginx 欢迎页](/assets/img/nginx_welcome_page.png)

### nginx 配置文件和最佳实践

* 通过以上方式安装的 Nginx，所有相关的配置文件都在 /etc/nginx/ 目录中。
* Nginx 的主配置文件是 /etc/nginx/nginx.conf。
为了使 Nginx 配置更易于维护，建议为每个服务（域名）创建一个单独的配置文件。
* 每一个独立的 Nginx 服务配置文件都必须以 .conf 结尾，并存储在 /etc/nginx/conf.d 目录中。您可以根据需求，创建任意多个独立的配置文件。
* 独立的配置文件，建议遵循以下命名约定，比如你的域名是 kaifazhinan.com，那么你的配置文件的应该是这样的 /etc/nginx/conf.d/kaifazhinan.com.conf，如果你在一个服务器中部署多个服务，当然你也可以在文件名中加上 Nginx 转发的端口号，比如 kaifazhinan.com.3000.conf，这样做看起来会更加友好。
如果你的配置中有很多重复的代码，那么建议你创建一个 /etc/nginx/snippets 文件夹，在这里面存放所有会被复用的代码块，然后在各个需要用到的 Nginx 的配置文件中引用进去，这样可以更方便管理和修改。
* Nginx 日志文件（access.log 和 error.log ）位于 /var/log/nginx/ 目录中。建议为每个独立的服务配置不同的访问权限和错误日志文件，这样查找错误时，会更加方便快捷。
* 你可以将要部署的代码文件，存储在任何你想的位置，但是一般推荐存放在下列位置中的其中一个：

  * /home/<user_name>/<site_name>
  * /var/www/<site_name>
  * /var/www/html/<site_name>
  * /opt/<site_name>
  * /usr/share/nginx/html
  