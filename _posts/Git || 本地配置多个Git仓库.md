---
title: 本地配置多个Git仓库
date: 2016/7/13 20:46:25
categories: Git
tags:
  - git
  - 配置
  - 多个仓库
---
工作用到公司的git repo，自己在github、coding有自己的repo，但是是在同一台笔记本上连接
一个ssh证书对应一个仓库，在做相应的配置即可
以公司、GitHub、Coding三个repo为例
<!--more-->
## 创建三份ssh证书
1、根据每个repo用到的email生成ssh证书
` ssh-keygen -t rsa -b 4096 -C "your_email@example.com" `
2、根据不同的repo进行命名，后面需要给每个repo配置证书
`Enter a file in which to save the key (/Users/you/.ssh/id_rsa): [XXXXXX（每个repo对应的ssh名称）]`
3、输入密码，一般都是直接回车，每次都是免密
`Enter passphrase (empty for no passphrase): [Type a passphrase]`
`Enter same passphrase again: [Type passphrase again]`
重复3次，生成3个ssh证书
分别为： id_rsa_work 、id_rsa_github、id_rsa_coding
位于`～/.ssh` 目录下（以Mac为例）
## 配置repo相应的ssh证书
在`~/.ssh` 目录下新建 config文件 `touch ~/config`
填写内容如下
```
#dhms
host git-server
user shiquan
hostname lan.work.cloud
port 29418
identityfile ~/.ssh/id_rsa_work
KexAlgorithms XXXXXXXXXXXXXXXXXX

#github
Host github.com
User shixiaoquan
HostName github.com
IdentityFile ~/.ssh/id_rsa_github

#coding
Host git.coding.net
User shixioaquan
HostName git.coding.net
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa_coding
```
**原理分析**（本段摘自[here](http://www.jianshu.com/p/04e9a885c5c8)）
 1.   ssh 客户端是通过类似 git@github.com:githubUserName/repName.git 的地址来识别使用本地的哪个私钥的，地址中的 User 是@前面的git， Host 是@后面的github.com。
 2.  如果所有账号的 User 和 Host 都为 git 和 github.com，那么就只能使用一个私钥。所以要对User 和 Host 进行配置，让每个账号使用自己的 Host，每个 Host 的域名做 CNAME 解析到 github.com，如上面配置中的Host second.github.com。
 3.  配置了别名之后，新的地址就是git@second.github.com:githubUserName/repName.git（在添加远程仓库时使用）。
这样 ssh 在连接时就可以区别不同的账号了。

## 填写ssh证书内容到相应的repo
将`~/.ssh` 目录下的 id_rsa_work.pub 、id_rsa_github.pub、id_rsa_coding.pub中的内容填写到相应的repo的ssh配置中

## 完活儿






