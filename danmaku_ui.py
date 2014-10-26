#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from random import randint
import cairo
from gi.repository import Gtk, GObject
from threading import Lock
from settings import load_config

color_styles = {
    "white": ((1, 1, 1), (0, 0, 0), ),
    "black": ((0, 0, 0), (1, 1, 1), ),
    "blue": ((20/255.0, 95/255.0, 198/255.0), (1, 1, 1), ),
    "lightblue": ((100/255.0, 172/255.0, 239/255.0), (0, 0, 0), ),
    "cyan": ((0, 1, 1), (0, 0, 0), ),
    "red": ((231/255.0, 34/255.0, 0), (1, 1, 1), ),
    "yellow": ((1, 221/255.0, 0), (0, 0, 0), ),
    "green": ((4/255.0, 202/255.0, 0), (0, 0, 0), ),
    "purple": ((0.5, 0, 0.5), (1, 1, 1), ),
}

TEST = False

OPTIONS = load_config()


class Danmaku(Gtk.Window):
    _lock = Lock()
    count = 0
    vertical_slots = None

    _font_family = OPTIONS['font_family']
    _speed_scale = OPTIONS['speed_scale']
    _font_size = OPTIONS['font_size']
    _height = _font_size + 6

    @classmethod
    def reload_config(cls, *args):
        options = load_config()
        cls._font_family = options['font_family']
        cls._speed_scale = options['speed_scale']
        cls._font_size = options['font_size']

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
        self.position_inited = False
        self.quited = False
        self.vslot = None

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            self.set_visual(self.visual)

        with Danmaku._lock:
            Danmaku.count += 1
            if Danmaku.vertical_slots is None:
                Danmaku.vertical_slots = [0] * \
                    ((self.screen.get_height() - 20) / self._height)

        self.set_app_paintable(True)

        # self.connect("destroy", Gtk.main_quit)

        self.connect("draw", self.clear_background)
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.draw_text)
        self.add(darea)

        self.text = text

        self.show_all()

    def init_position(self):
        self.set_opacity(1)
        self.height = self._height
        self.resize(self.width, self.height)

        if self.position == 'fly':
            self.x = self.screen.width()
            self.y = randint(0, self.screen.height()-self._font_size-20)
            self.step = min(len(self.text) * 0.03 + 1.2, 8) * self._speed_scale
            # print self.step
            self.interval = 30

        elif self.position == 'bottom':
            self.x = (self.screen.width() - self.width) / 2
            with Danmaku._lock:
                i = 0
                for i, v in enumerate(Danmaku.vertical_slots[::-1]):
                    if v == 0:
                        Danmaku.vertical_slots[-(i+1)] = 1
                        self.vslot = -(i+1)
                        break
                else:
                    self.set_opacity(0)
                    GObject.timeout_add(1000, self.init_position)
                    return

                self.y = self.screen.height() + self.height * self.vslot - 10
                # print self.text, self.x, self.y

        elif self.position == 'top':
            self.x = (self.screen.width() - self.width) / 2
            with Danmaku._lock:
                i = 0
                for i, v in enumerate(Danmaku.vertical_slots):
                    if v == 0:
                        Danmaku.vertical_slots[i] = 1
                        self.vslot = i
                        break
                else:
                    self.set_opacity(0)
                    GObject.timeout_add(1000, self.init_position)
                    return

                self.y = self.height * self.vslot + 10

        self.move(self.x, self.y)
        self.position_inited = True

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
        cr.select_font_face(self._font_family,
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(self._font_size)
        cr.move_to(0, 25)
        cr.show_text(self.text)
        self.width = cr.get_current_point()[0] + 10

        cr.set_source_rgb(*border_color)
        cr.move_to(0, 25)
        cr.set_line_width(0.5)
        cr.text_path(self.text)
        cr.stroke()

        if not self.position_inited:
            self.init_position()

        if self.position == "fly":
            GObject.timeout_add(10, self.fly)
        else:
            GObject.timeout_add(5000, self._clean_exit)

    def fly(self):
        _x = int(self.x)
        self.x -= self.step
        x_dst = int(self.x)
        if self.x < -self.width:
            if not self.quited:
                self._clean_exit()
        else:
            GObject.timeout_add(self.interval, self.fly)

        if _x != x_dst:
            self.move(x_dst, self.y)

    def _clean_exit(self):
        if self.quited:
            return

        self.quited = True

        with Danmaku._lock:
            Danmaku.count -= 1
            # print(Danmaku.count)
            if self.vslot is not None:
                Danmaku.vertical_slots[self.vslot] = 0

            if TEST:
                if Danmaku.count <= 0:
                    Gtk.main_quit()

        self.close()


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)

    TEST = True
    Danmaku("T")
    Danmaku("Test", style="blue")
    Danmaku("我爱bilibili")
    Danmaku("我爱bilibili还有acfun")
    Danmaku("穹妹是我的")
    Danmaku("括号君我要给你生猴子")
    Danmaku("括号君我要你给我生猴子")
    Danmaku("括号君王尼玛黑雪学姐我要你给我生猴子")
    Danmaku("Test", style="blue", position="top")
    Danmaku("Test", style="green", position="top")
    Danmaku("马云保护协会", style="blue", position="top")
    Danmaku("清华大学TUNA协会", style="purple", position="top")
    Danmaku("Test Bottom 1", style="red", position="bottom")
    Danmaku("Test Bottom 2", style="cyan", position="bottom")
    Gtk.main()

# vim: ts=4 sw=4 sts=4 expandtab
