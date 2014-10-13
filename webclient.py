#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import requests
import json
from dbus_client import interface


def subscribe_danmaku(server="http://localhost:5000/danmaku/stream"):
    while 1:
        res = requests.get(server)
        if res.status_code == 200 and res.text:
            for opt in json.loads(res.text):
                interface.new_danmaku(json.dumps(opt))

# vim: ts=4 sw=4 sts=4 expandtab
