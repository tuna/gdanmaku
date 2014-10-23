#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import signal
import json
import argparse
import threading
import requests


def app_main(dm_server):

    from danmaku_ui import Danmaku
    from gi.repository import Gtk, GLib, GObject

    def new_danmaku(dm_opts):
        for opt in dm_opts:
            try:
                Danmaku(**opt)
            except:
                continue

    def subscribe_danmaku(server="http://dm.tuna.moe/danmaku/stream"):
        while 1:
            try:
                res = requests.get(server)
            except requests.exceptions.ConnectionError:
                continue
            if res.status_code == 200 and res.text:
                try:
                    dm_opts = json.loads(res.text)
                except:
                    continue
                else:
                    GLib.idle_add(new_danmaku, dm_opts)

    GObject.threads_init()

    thread_sub = threading.Thread(
        target=subscribe_danmaku, args=(dm_server, ))
    thread_sub.daemon = True
    thread_sub.start()

    Gtk.main()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="gdanmaku")
    parser.add_argument(
        "--server",
        type=str,
        default="http://dm.tuna.moe/danmaku/stream",
        help="danmaku stream server"
    )

    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)

    app_main(args.server)


# vim: ts=4 sw=4 sts=4 expandtab
