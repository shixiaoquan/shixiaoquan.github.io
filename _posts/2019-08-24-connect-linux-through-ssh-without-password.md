---
layout: post
title:  "使用 SSH 免密登录 Linux 服务器"
date:   2019-08-24 09:28
categories: OPS
---


```bash

```

### 在本地生成公钥和私钥

 在本地的 ~/.ssh/ 目录下,生成公钥和私钥

```bash
ssh-keygen -t rsa -C  'your email@domain.com'

-t 指定密钥类型，默认即 rsa ，可以省略
-C 设置注释文字，比如你的邮箱，可以省略
```

示例:(我用的老余的服务器)

```bash
🙈: ssh-keygen -t rsa -C 1010080000@qq.com
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/edmond/.ssh/id_rsa): id_rsa_lao_yu_server
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in id_rsa_lao_yu_server.
Your public key has been saved in id_rsa_lao_yu_server.pub.
The key fingerprint is:
SHA256:Cqkr7ze0sfgHdtCcEXnD/S+CuVoA/PEFMKTgRkQs/g8 1010083274@qq.com
The key's randomart image is:
+---[RSA 2048]----+
| +=  .==..       |
|.o.o .o.+..      |
|..o +o.+ ...     |
| o  .++o .  .    |
|  . o.o So   .   |
|   E=..oo . . .  |
|  .+o*. .. . .   |
|. ..=....        |
| ++o.o..         |
+----[SHA256]-----+
```

### 复制公钥到服务器

id_rsa 和 id_rsa.pub 分别是私钥和公钥, 我们打开 带后缀 .pub 的文件

```bash
vim id_rsa.pub
```

将内容追加到服务器的 `~/.shh/authorized_keys` 文件中.

### 配置本地的 ssh 配置文件

如果只连接一台服务器,也没有其他的需求,例如连接 GitHub 之类的, 直接就可以使用了;
如果需要配置多台服务器,就需要在 `~/.shh/` 先创建一个 `config` 文件, 用于配置不同的服务器

```bash
touch ~/.ssh/config
```

```bash
Host            alias            #自定义别名
HostName        hostname         #替换为你的ssh服务器
Port            port             #ssh服务器端口，默认为22
User            user             #ssh服务器用户名
IdentityFile    ~/.ssh/id_rsa    #第一个步骤生成的公钥文件对应的私钥文件
```

### 利用别名就可以开始装逼了

```bash
ssh laoyu
```

```bash
Last login: Sat Aug 24 09:24:24 2019 from 180.107.200.19
```

这样就成功了

### 保持长连接, 防止超时断线

在本机 `/etc/ssh/ssh_config` 中加入 `ServerAliveInterval 60`

添加后效果如下:

```bash
# Host *
ServerAliveInterval 60
#   ForwardAgent no
#   ForwardX11 no
#   PasswordAuthentication yes
#   HostbasedAuthentication no
#   GSSAPIAuthentication no
#   GSSAPIDelegateCredentials no
#   BatchMode no
#   CheckHostIP yes
#   AddressFamily any
#   ConnectTimeout 0
#   StrictHostKeyChecking ask
#   IdentityFile ~/.ssh/id_rsa
#   IdentityFile ~/.ssh/id_dsa
#   IdentityFile ~/.ssh/id_ecdsa
#   IdentityFile ~/.ssh/id_ed25519
```

`ServerAliveInterval 60` 的作用是每隔60秒系统会发送一个空数据包,从而保持与服务器的连接, 防止超时断线
