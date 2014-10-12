#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import Gtk
from danmaku_ui import Danmaku


class DBusObject(dbus.service.Object):

    @dbus.service.method("moe.tuna.danmaku.Service", in_signature='s', out_signature='s')
    def new_danmaku(self, content):
        Danmaku(content)
        return "Welcome!"

    @dbus.service.method("moe.tuna.danmaku.Service", in_signature='', out_signature='s')
    def exit(self):
        Gtk.main_quit()
        return "Bye!"


if __name__ == '__main__':

    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("moe.tuna.danmaku", session_bus)
    _object = DBusObject(session_bus, "/Danmaku")
    Gtk.main()
    # app.run()

# vim: ts=4 sw=4 sts=4 expandtab
