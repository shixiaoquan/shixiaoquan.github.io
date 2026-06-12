---
layout: post
title:  "使用 nodemon 替代 node 进行开发"
date:   2019-10-20 17:40
categories: OPS
---

## 安装

可以安装在全局,也可以安装在项目里面,放在 devDependences 里面就行了

```bash
npm install nodemon -g
```

或

```bash
npm install nodemon --dev
```

## 最佳实践,用过的配置文件

```json
{
  "verbose": true,
  "debug": true,
  "exec": "ts-node src/server.ts",
  "ignore": [
    "node_modules",
    "./test",
    "**/*.d.ts",
    "*.test.ts",
    "*.spec.ts",
    "fixtures/*",
    "test/**/*",
    "docs/*"
  ],
  "events": {
    "restart": "rs"
  },
  "watch": [
    "./src"
  ],
  "env": {
    "NODE_ENV": "development",
    "PORT": "3000"
  },
  "ext": "ts",
  "inspect": true
}
```
