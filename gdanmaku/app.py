#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from gi.repository import Gtk
from config_panel import ConfigPanel
from danmaku_ui import Danmaku
import os

ICON_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "images")

ICON_ENABLED = os.path.join(ICON_DIR, "statusicon.png")
ICON_DISABLED = os.path.join(ICON_DIR, "statusicon_disabled.png")


class GDanmakuApp(object):

    def __init__(self, parent=None):
        self.parent = parent

        self.icon = Gtk.StatusIcon.new_from_file(ICON_ENABLED)
        self.icon.connect("activate", self.on_left_click)
        self.icon.connect("popup-menu", self.on_right_click)

        self.enabled = True

        self.menu = Gtk.Menu()

        self.toggle_item = Gtk.MenuItem("Disable")
        self.toggle_item.connect("activate", self.toggle_danmaku)
        self.menu.append(self.toggle_item)

        self.pref_item = Gtk.MenuItem("Preferences")
        self.pref_item.connect("activate", self.show_config_panel)
        self.menu.append(self.pref_item)

        self.exit_item = Gtk.MenuItem("Exit")
        self.exit_item.connect("activate", Gtk.main_quit)
        self.menu.append(self.exit_item)

        self.menu.show_all()

    def on_left_click(self, event):
        self.toggle_danmaku(None)

    def on_right_click(self, icon, ev_btn, ev_time):
        def pos(menu, aicon):
            return (Gtk.StatusIcon.position_menu(menu, aicon))

        self.menu.popup(None, None, pos, icon, ev_btn, ev_time)

    def toggle_danmaku(self, widget):
        self.parent.toggle_danmaku()
        if self.enabled:
            self.toggle_item.set_label("Enable")
            self.icon.set_from_file(ICON_DISABLED)
            self.enabled = False
        else:
            self.toggle_item.set_label("Disable")
            self.icon.set_from_file(ICON_ENABLED)
            self.enabled = True

    def show_config_panel(self, widget):
        cp = ConfigPanel(is_main=False)
        cp.connect('config-saved', Danmaku.reload_config)


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    d = GDanmakuApp()
    Gtk.main()

# vim: ts=4 sw=4 sts=4 expandtab
