#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="danmaku")
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="subcommand",
        help="sub commands"
    )

    parser_display = subparsers.add_parser('display', help="danmaku display service")
    parser_subscriber = subparsers.add_parser('subscribe', help="subscribe danmaku stream")
    parser_subscriber.add_argument(
        "--server",
        type=str,
        default="http://dm.tuna.moe/danmaku/stream",
        help="danmaku stream server"
    )
    parser_kill = subparsers.add_parser('kill', help="kill danmaku display serverice")

    args = parser.parse_args()

    if args.subcommand == 'display':
        from display_service import danmaku_service
        danmaku_service()
    elif args.subcommand == "kill":
        from dbus_client import interface
        interface.exit()
    elif args.subcommand == "subscribe":
        from webclient import subscribe_danmaku
        subscribe_danmaku(args.server)

    # app.run()

# vim: ts=4 sw=4 sts=4 expandtab
