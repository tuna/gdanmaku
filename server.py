#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import dbus
from flask import Flask, request, render_template


bus = dbus.SessionBus()
proxy = bus.get_object('moe.tuna.danmaku', '/Danmaku')
interface = dbus.Interface(proxy, 'moe.tuna.danmaku.Service')

app = Flask("Danmaku")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/danmaku/", methods=["POST"])
def publish_danmaku():
    if request.json:
        content = request.json["content"]
    else:
        content = request.form["content"]

    interface.new_danmaku(content)
    return "OK"


@app.route("/", methods=["DELETE"])
def stop_service():
    interface.exit()
    return "Exited!"


if __name__ == "__main__":
    app.run(debug=True)


# vim: ts=4 sw=4 sts=4 expandtab
