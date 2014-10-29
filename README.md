# GDanmaku

GDanmaku is a small GTK program to play danmaku on any screen.

## Warning

GDanmaku is still under development, documents might be outdated.

## Run Demo

### Config

run `./danmaku.py --config` to set your preferences.

Make sure you have chosen a font that supports unicode, 
or Chinese characters would be rendered as block.

### Use TUNA Service

First u need to create a channel, go to http://dm.tuna.moe/ and create a channel, 
(let's use `ooxx` as the channel name and `passw0rd` as the password)

then run `./danmaku.py` and fill `http://dm.tuna.moe` to server, 
and your channel name (`ooxx`) and channel password (`passw0rd)`.

then open http://dm.tuna.moe/ and click to your channel page, then post.

### Server Hosted Service

Clone https://github.com/tuna/gdanmaku-server and run `webserver.py` to start a publishing server, 
then run 

```
danmaku.py --server=http://localhost:5000/
```

## Todo

- [ ] More channels to send danmaku
    - [x] dm.tuna.moe
    - [ ] Twitter
    - [ ] Wechat
- [x] User defined configurations
    - [x] font size
    - [x] speed

## Screenshot

![](https://raw.githubusercontent.com/bigeagle/gdanmaku/master/screenshots/danmaku.png)
