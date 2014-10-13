#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import json
from flask import Flask, request, render_template
import gevent
from gevent.wsgi import WSGIServer

app = Flask("Danmaku")

new_danmaku = gevent.event.Event()
danmaku_list = []


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/danmaku/stream", methods=["GET"])
def danmaku_stream():
    global danmaku_list
    if new_danmaku.wait(timeout=5):

        r = json.dumps(danmaku_list)
        danmaku_list = []
        new_danmaku.clear()
        return r
    else:
        return json.dumps(danmaku_list)


@app.route("/danmaku/", methods=["POST"])
def publish_danmaku():
    if request.json:
        danmaku = {
            "text": request.json["content"],
            "style": request.json.get("color", "white"),
            "position": request.json.get("position", "fly")
        }
    else:
        danmaku = {
            "text": request.form["content"],
            "style": request.form.get("style", "white"),
            "position": request.form.get("position", "fly")
        }

    # interface.new_danmaku(content)
    danmaku_list.append(danmaku)
    new_danmaku.set()
    return "OK"


if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()


# vim: ts=4 sw=4 sts=4 expandtab
