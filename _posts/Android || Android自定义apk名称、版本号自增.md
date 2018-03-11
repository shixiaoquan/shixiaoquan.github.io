---
title: Android自定义apk名称、版本号自增
date: 2016/3/11 20:46:25
categories: Android
tags:
  - android
  - apk名称
  - apk版本号
---
### 自定义apk名称
默认情况下，gradle会打包一个app-release.apk文件，但是在实际应用中没啥用，gradle支持根据需求自定义apk文件名称
设置应用名称在module根目录的build.gradle文件中的这个位置

```
applicationVariants.all { variant ->
        variant.outputs.each { output ->
            ......
            //setting apk name to what you want
            output.outputFile = new File(output.outputFile.parent, "luffy" + "-v" +
                    defaultConfig.versionName + "-" + defaultConfig.versionCode + ".apk");
        }
    }
```
<!--more-->
**如上的代码会第一次打包会生成一个 luffy-v1.0-1.apk的文件**

apk文件的名称是由new File(P1, P2),这个对象的P2参数决定的，上面的例子中，配置了 luffy+ versionName+versionCode，得到相应的文件名

还可以根据你的需求添加其他的信息，比如时间

```
// 获取当前系统时间
def releaseTime() {    return new Date().format("yyyy-MM-dd", TimeZone.getTimeZone("UTC"))
}
// 获取程序名称
def getProductName(){    return "gradlesample"}
```
在

```
android{
	......
}
```
标签外，定义函数获取时间和项目名称，用于命名

```

// 获取当前系统时间
def releaseTime() { return new Date().format("yyyy-MM-dd", TimeZone.getTimeZone("UTC")) }
// 获取程序名称
def getProductName(){    return "gradlesample"}
android {
	......

    // applicationVariants are e.g. debug, release
    applicationVariants.all { variant ->
        variant.outputs.each { output ->
        .....
            //setting apk name to what you want
            output.outputFile = new File(output.outputFile.parent, defaultConfig.applicationId + "-" + buildType.name + "-v" +
                    defaultConfig.versionName + "-" + defaultConfig.versionCode + releaseTime() + "-" + getProductName() + "-" + ".apk");
        }
    }
}
```
得到com.gradlesample-release-v1.0-**32017-09-12-gradlesample**-.apk,加上了时间和项目名称
### 版本号自增

 **1、 在module的根目录下新建version.properties文件**

内容：`VERSION_CODE=1`

**2、 获取本次打包应该使用的版本号**

```

/**
 * auto increase apk versioncode,and return versioncode
 * @return
 */
def getVersionCode() {
    def versionFile = file('version.properties')
    if (versionFile.canRead()) {
        def Properties versionProps = new Properties()
        versionProps.load(new FileInputStream(versionFile))
        def versionCode = versionProps['VERSION_CODE'].toInteger()
        def runTasks = gradle.startParameter.taskNames        //仅在assembleRelease任务是增加版本号
        if ('assembleRelease' in runTasks) {
            versionProps['VERSION_CODE'] = (++versionCode).toString()
            versionProps.store(versionFile.newWriter(), null)
        }
        return versionCode
    } else {
        throw new GradleException("Could not find version.properties!")
    }
}
```
原理就是，每次打包时去 version.properties文件中去读取记录下的versionCode，然后在原来的基础上+1，并覆盖原来的记录，然后返回+1后的versionCode
**3、 设置defaultConfig中的versionCode**

```

    def currentVersionCode = getVersionCode()

    defaultConfig {
	    ......
        versionCode currentVersionCode
        ......
    }
```
