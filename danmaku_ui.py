#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from random import randint
import cairo
from gi.repository import Gtk, GObject
from threading import Lock

color_styles = {
    "white": ((1, 1, 1), (0, 0, 0), ),
    "blue": ((20/255.0, 95/255.0, 198/255.0), (1, 1, 1), ),
    "lightblue": ((100/255.0, 172/255.0, 239/255.0), (0, 0, 0), ),
    "cyan": ((0, 1, 1), (0, 0, 0), ),
    "red": ((231/255.0, 34/255.0, 0), (1, 1, 1), ),
    "yellow": ((1, 221/255.0, 0), (0, 0, 0), ),
    "green": ((4/255.0, 202/255.0, 0), (0, 0, 0), ),
}


class Danmaku(Gtk.Window):
    _lock = Lock()
    count = 0
    bottom_count = 0
    top_count = 0

    def __init__(self, text=u"我来组成弹幕", style="white", position="fly"):
        super(Danmaku, self).__init__(
            type=Gtk.WindowType.POPUP, title="Danmaku")
        # super(Danmaku, self).__init__(title="Danmaku")
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        # self.set_decorated(False)
        # self.set_size_request(500, 40)
        # self.set_size_request(370, 240)

        self.style = style
        self.position = position

        with Danmaku._lock:
            Danmaku.count += 1
            if self.position == "bottom":
                Danmaku.bottom_count += 1
            elif self.position == "top":
                Danmaku.top_count += 1

            print(self.count)

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            self.set_visual(self.visual)

        self.set_app_paintable(True)

        # self.connect("destroy", Gtk.main_quit)

        self.connect("draw", self.clear_background)
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.draw_text)
        self.add(darea)

        self.x = self.screen.width()
        self.y = randint(0, self.screen.height())
        self.text = text

        self.show_all()

    def clear_background(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def draw_text(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        font_color, border_color = color_styles.get(
            self.style,
            color_styles["white"]
        )

        cr.set_source_rgb(*font_color)
        cr.select_font_face("WenQuanYi Micro Hei",
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(24)
        cr.move_to(20, 30)
        cr.show_text(self.text)
        cr.set_source_rgb(*border_color)
        cr.move_to(20, 30)
        cr.set_line_width(0.5)
        cr.text_path(self.text)
        cr.stroke()

        GObject.timeout_add(10, self.fly)

    def fly(self):
        self.move(self.x, self.y)
        self.x -= 30
        if self.x < -400:
            self.destroy()
            with Danmaku._lock:
                Danmaku.count -= 1
            if self.position == "bottom":
                Danmaku.bottom_count -= 1
            elif self.position == "top":
                Danmaku.top_count -= 1

        GObject.timeout_add(30, self.fly)


if __name__ == "__main__":

    Danmaku("我爱bilibili")
    Danmaku("Test", style="darkblue")
    Gtk.main()

# vim: ts=4 sw=4 sts=4 expandtab
