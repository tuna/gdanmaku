#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import signal
import json
import argparse
import threading
import requests
from settings import load_config
from app import GDanmakuApp

from danmaku_ui import Danmaku
from gi.repository import Gtk, GLib, GObject


class Main(object):

    def __init__(self, server=None):
        self.server = server
        self.app = GDanmakuApp(self)
        self.thread_sub = None
        self.enabled = True
        self.options = load_config()
        self.live_danmakus = {}

    def _subscribe_danmaku(self, server):
        print("subscribing from server: {}".format(server))
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
                    GLib.idle_add(self.new_danmaku, dm_opts)

    def new_danmaku(self, dm_opts):
        if not self.enabled:
            return

        for opt in dm_opts:
            try:
                dm = Danmaku(**opt)
                dm.connect('delete-event', self.on_danmaku_delete)
            except Exception as e:
                print(e)
                continue

            self.live_danmakus[id(dm)] = dm

    def on_danmaku_delete(self, dm, event):
        self.live_danmakus.pop(id(dm))

    def toggle_danmaku(self):
        self.enabled = not self.enabled
        if not self.enabled:
            for _, dm in self.live_danmakus.iteritems():
                dm.hide()
                dm._clean_exit()

    def run(self):
        GObject.threads_init()
        dm_server = self.server or self.options["http_stream_server"]
        thread_sub = threading.Thread(
            target=self._subscribe_danmaku, args=(dm_server, ))
        thread_sub.daemon = True
        thread_sub.start()
        self.thread_sub = thread_sub

        Gtk.main()


def main():
    options = load_config()

    parser = argparse.ArgumentParser(prog="gdanmaku")
    parser.add_argument(
        "--server",
        type=str,
        default=options["http_stream_server"],
        help="danmaku stream server"
    )

    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)

    main_app = Main(args.server)
    main_app.run()


if __name__ == '__main__':
    main()

# vim: ts=4 sw=4 sts=4 expandtab
