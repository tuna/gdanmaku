#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import signal
import json
import argparse
import threading
import requests

from settings import load_config
from app import GDanmakuApp
from server_selection import ServerSelectionWindow
from danmaku_ui import Danmaku
from gi.repository import Gtk, GLib, GObject


class Main(object):

    def __init__(self, server=None):
        self.server = server
        server_selection = ServerSelectionWindow(self.server)
        server_selection.connect('server-selected', self.on_server_selected)
        self.app = GDanmakuApp(self)
        self.thread_sub = None
        self.enabled = True
        self.options = load_config()
        self.live_danmakus = {}

    def _subscribe_danmaku(self, server, channel, password):
        print("subscribing from server: {}, channel: {}".format(server, channel))
        uri = self.options["http_stream_uri"].format(cname=channel)
        if uri.starswith("/") and server.endswith("/"):
            server = server[:-1]
        url = server + uri

        while 1:
            try:
                res = requests.get(
                    url, headers={"X-GDANMAKU-AUTH-KEY": password})
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

    def on_server_selected(self, widget, server, channel, password):
        thread_sub = threading.Thread(
            target=self._subscribe_danmaku, args=(server, channel, password))
        thread_sub.daemon = True
        thread_sub.start()
        self.thread_sub = thread_sub

    def run(self):
        GObject.threads_init()
        Gtk.main()


def app_config():
    from config_panel import ConfigPanel
    from gi.repository import Gtk
    ConfigPanel()
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

    parser.add_argument(
        '--config',
        action="store_true",
        help="run configuration window"
    )

    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)

    if args.config:
        app_config()
    else:
        main_app = Main(args.server)
        main_app.run()


if __name__ == '__main__':
    main()

# vim: ts=4 sw=4 sts=4 expandtab
