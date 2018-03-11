---
title: Android-MediaPlayer---播放音频
date: 2016/3/11 20:46:25
categories: Android
tags:
  - android
  - MediaPlayer
  - 音频
---
# 获取MediaPlayer的实例

## 使用new方法创建

```
MediaPlayer mediaPlayer = new MediaPlayer();
```

## 使用create方法创建
共有5种重载方法
<!--more-->
**方法一：**
```
create(Context context, Uri uri)
```
Parameters
<table border="1">
<tr>
<td>context</td>
<td>the Context to use</td>
</tr>
<tr>
<td>uri</td>
<td>the Uri from which to get the datasource</td>
</tr>
</table>
Uri需要自己构建，可以是SDCard中的音频路径，也可以是网络资源地址
例如：
```
/*SdCard中获取资源*/
String path = Environment.getExternalStorageDirectory().toString() + "/" + "test.amr";
Uri uri = Uri.fromFile(new File( path));
Uri uri = Uri.parse(path);
mediaPlayer = MediaPlayer.create(this, uri);
/*网络资源*/
path = "http://222.92.237.119:11000/UploadFiles/company_1/2016-11-16/0123fbc7-ee2b-4c2e-88d0-60a1528d1023.aac";
uri = Uri.parse(path);
mediaPlayer = MediaPlayer.create(this, uri);
```
**方法二：**
```
create(Context context, int resid)
```
Parameters
<table border="1">
<tr>
<td>context</td>
<td>the Context to use</td>
</tr>
<tr>
<td>uri</td>
<td>the raw resource id (R.raw.<something>) for the resource to use as the datasource</td>
</tr>
</table>

例如：
```
mediaPlayer = MediaPlayer.create(this, R.raw.test);
```

**方法三四五:**
```
create(Context context, int resid, AudioAttributes audioAttributes, int audioSessionId)
create(Context context, Uri uri, SurfaceHolder holder)
create(Context context, Uri uri, SurfaceHolder holder, AudioAttributes audioAttributes, int audioSessionId)
```
最后两个方法是播放视频的，暂时不管他，第三个不会用不管 >_<

# 设置需要播放的文件
如果使用create方法创建MediaPlayer实例，则不在需要设置数据源，也不需要调用prepare()方法。
现在说的说的是使用new 方法创建的MediaPlayer实例。
需要调用setDataSource方法
 **1. assets中获取资源**
```
try {
	FileDescriptor fileDescriptor = getAssets().openFd("test.mp3").getFileDescriptor();
	mMediaPlayer.reset();
	mMediaPlayer.setDataSource(fileDescriptor);
	mMediaPlayer.prepare();
} catch (IOException e) {
	e.printStackTrace();
}
```
 **2. SDCard中获取资源方法1**

```
String path = Environment.getExternalStorageDirectory().toString() + "/" + "test.amr";
        Uri uri = Uri.fromFile(new File(path));
        try {
            mMediaPlayer.reset();
            mMediaPlayer.setDataSource(AudioPlayActivity2.this,uri);
            mMediaPlayer.prepare();
        } catch (IOException e) {
            e.printStackTrace();
        }
```

 **3. SDCard中获取资源方法2**

```
String path = Environment.getExternalStorageDirectory().toString() + "/" + "test.amr";
        Uri uri = Uri.parse(path);
        try {
            mMediaPlayer.reset();
            mMediaPlayer.setDataSource(AudioPlayActivity2.this,uri);
            mMediaPlayer.prepare();
        } catch (IOException e) {
            e.printStackTrace();
        }
```

 **4. SDCard中获取资源方法3**

```
String path = Environment.getExternalStorageDirectory().toString() + "/" + "test.amr";
        try {
            mMediaPlayer.reset();
            mMediaPlayer.setDataSource(path);
            mMediaPlayer.prepare();
        } catch (IOException e) {
            e.printStackTrace();
        }
```

 **5. 网络资源1**

```
String path = "http://222.92.237.119:11000/UploadFiles/company_1/2016-11-16/0123fbc7-ee2b-4c2e-88d0-60a1528d1023.aac";
        try {
            mMediaPlayer.reset();
            mMediaPlayer.setDataSource(path);
            mMediaPlayer.prepare();
        } catch (IOException e) {
            e.printStackTrace();
        }
```

 **6. 网络资源2**

```
String path = "http://222.92.237.119:11000/UploadFiles/company_1/2016-11-16/0123fbc7-ee2b-4c2e-88d0-60a1528d1023.aac";
        Uri uri = Uri.parse(path);
        try {
            mMediaPlayer.reset();
            mMediaPlayer.setDataSource(AudioPlayActivity2.this,uri);
            mMediaPlayer.prepare();
        } catch (IOException e) {
            e.printStackTrace();
        }
```

# 对播放器的主要控制
<table>
<tr>
<td>prepare()</td>
<td>提供了同步方式设置播放器进入prepare状态，需要注意的是，如果MediaPlayer实例是由create方法创建的，那么第一次启动播放前不需要再调用prepare（）了，因为create方法里已经调用过了</td>
</tr>
<tr>
<td>prepareAsync() </td>
<td>提供了异步方式设置播放器进入prepare状态</td>
</tr>
<tr>
<td>start()</td>
<td>启动文件播放的方法</td>
</tr>
<tr>
<td>pause()</td>
<td>暂停</td>
</tr>
<tr>
<td>stop()</td>
<td>结束</td>
</tr>
<tr>
<td>seekTo()</td>
<td>定位方法，可以让播放器从指定的位置开始播放，需要注意的是该方法是个异步方法，也就是说该方法返回时并不意味着定位完成，尤其是播放的网络文件，真正定位完成时会触发OnSeekComplete.onSeekComplete()，如果需要是可以调用setOnSeekCompleteListener(OnSeekCompleteListener)设置监听器来处理的</td>
</tr>
<tr>
<td>release()</td>
<td>可以释放播放器占用的资源，一旦确定不再使用播放器时应当尽早调用它释放资源</td>
</tr>
<tr>
<td>reset()</td>
<td>可以使播放器从Error状态中恢复过来，重新会到Idle状态</td>
</tr>
</table>

# 设置播放器的监听事件
常用的两种是setOnCompletionListener(MediaPlayer.OnCompletionListener listener)和
setOnErrorListener(MediaPlayer.OnErrorListener listener)
例如：

```
mMediaPlayer.setOnCompletionListener(new
	MediaPlayer.OnCompletionListener() {
    @Override
    public void onCompletion(MediaPlayer mp) {
		mp.release();
    }
});
mMediaPlayer.setOnErrorListener(new
	MediaPlayer.OnErrorListener() {
	@Override
	public boolean onError(MediaPlayer mp, int what, int extra) {
		mp.release();
		return false;
	}
});
```
