#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import dbus


bus = dbus.SessionBus()
proxy = bus.get_object('moe.tuna.danmaku', '/Danmaku')
interface = dbus.Interface(proxy, 'moe.tuna.danmaku.Service')

__all__ = ("interface", )

# vim: ts=4 sw=4 sts=4 expandtab
