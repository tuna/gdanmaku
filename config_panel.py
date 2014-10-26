#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from gi.repository import Gtk, Pango
from settings import load_config, save_config


class ConfigPanel(Gtk.Window):

    def __init__(self):
        super(ConfigPanel, self).__init__(
            type=Gtk.WindowType.TOPLEVEL, title="Danmaku")

        self.options = load_config()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                       spacing=10, margin=10)
        self.add(vbox)

        # Stream Server
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       spacing=10, margin=10)
        server_label = Gtk.Label("Server:")
        hbox.pack_start(server_label, False, True, 0)

        server_entry = Gtk.Entry()
        server_entry.set_text(self.options["http_stream_server"])
        server_entry.connect("changed", self.on_server_changed)

        hbox.pack_start(server_entry, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        # Font Selection
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       spacing=10, margin=10)
        font_label = Gtk.Label("Font:")
        hbox.pack_start(font_label, False, True, 0)

        font_button = Gtk.FontButton(
            font_name=u"{} {}".format(self.options['font_family'],
                                      self.options['font_size']))

        font_button.connect("font-set", self.on_font_select)
        hbox.pack_start(font_button, False, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        # Speed Scale
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       spacing=10, margin=10)
        speed_label = Gtk.Label("Speed:")
        hbox.pack_start(speed_label, False, True, 0)

        speed_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=Gtk.Adjustment(
                self.options['speed_scale'], 0.5, 2.0, 0.01, 0, 0)
        )
        speed_scale.connect("change-value", self.on_speed_select)
        hbox.pack_start(speed_scale, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

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

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_server_changed(self, widget):
        self.options['http_stream_server'] = widget.get_text()

    def on_font_select(self, widget):
        fontname = widget.get_font_name()
        font_family = Pango.font_description_from_string(fontname).get_family()
        font_size = widget.get_font_size() / 1000
        self.options['font_family'] = font_family
        self.options['font_size'] = font_size

    def on_speed_select(self, widget, scroll, value):
        self.options['speed_scale'] = int(value * 100) / 100.0

    def on_confirm_button(self, widget):
        save_config(self.options)
        Gtk.main_quit()

if __name__ == "__main__":
    cp = ConfigPanel()
    Gtk.main()

# vim: ts=4 sw=4 sts=4 expandtab
