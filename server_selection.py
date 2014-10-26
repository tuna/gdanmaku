#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from gi.repository import Gtk, GObject
from settings import load_config, save_config


class ServerSelectionWindow(Gtk.Window):

    __gsignals__ = {
        "server-selected": (GObject.SIGNAL_RUN_FIRST, None, (str, ))
    }

    def __init__(self, server, is_main=False):
        super(ServerSelectionWindow, self).__init__(
            type=Gtk.WindowType.TOPLEVEL, title="Danmaku")

        self.options = load_config()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                       spacing=0, margin=10)
        self.add(vbox)

        # Stream Server
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       spacing=10, margin=10)
        server_label = Gtk.Label("Server:")
        hbox.pack_start(server_label, False, True, 0)

        server_entry = Gtk.Entry()
        server_entry.set_width_chars(30)
        server_entry.set_text(server)
        hbox.pack_start(server_entry, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        self.server_entry = server_entry

        # check
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       spacing=10, margin=10)
        save_default_btn = Gtk.CheckButton.new_with_label("Save as default")
        hbox.pack_end(save_default_btn, False, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        self.save_default_btn = save_default_btn

        # Buttons
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       spacing=20, margin=10)
        cancel_button = Gtk.Button("Cancel")
        cancel_button.connect("clicked", Gtk.main_quit)
        hbox.pack_start(cancel_button, True, True, 0)

        ok_button = Gtk.Button("OK")
        ok_button.connect("clicked", self.on_confirm_button)
        hbox.pack_start(ok_button, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        if is_main:
            self.connect("delete-event", Gtk.main_quit)

        self.show_all()

    def on_confirm_button(self, widget):
        server = self.server_entry.get_text()
        if self.save_default_btn.get_active():
            options = load_config()
            options["http_stream_server"] = server
            save_config(options)

        self.emit("server-selected", server)
        self.close()


if __name__ == "__main__":
    options = load_config()
    sel_win = ServerSelectionWindow(options["http_stream_server"], is_main=True)
    Gtk.main()
# vim: ts=4 sw=4 sts=4 expandtab
