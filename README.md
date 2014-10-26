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

Let's use `ooxx` as a channel name, run

```
./danmaku.py --server=http://dm.tuna.moe/danmaku/stream?c=ooxx
```

or just run `./danmaku.py` and fill server url in the first dialog.

and post on http://dm.tuna.moe/?c=ooxx

### Server Hosted Service

Clone https://github.com/tuna/gdanmaku-server and run `webserver.py` to start a publishing server, 
then run 

```
danmaku.py --server=http://localhost:5000/danmaku/stream
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
