#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of nautilus-sharefile
#
# Copyright (c) 2020 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import os
import socket
from myqr import create_qr
from server import stop_server
from plumbum import local, BG

SIZE = 300
_ = str


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class ShareDialog(Gtk.Dialog):

    def __init__(self, port, seed, filename, title, parent=None, icon=None):
        Gtk.Dialog.__init__(self, title, parent)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        self.set_resizable(False)
        if icon:
            self.set_icon_name(icon)
        self.connect('destroy', self.close)
        self.connect('realize', self.on_realize)
        self._port = port
        self._seed = seed
        self._filename = filename
        ip = get_ip()
        self._url = 'https://{}:{}/{}'.format(ip, self._port, self._seed)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        vbox.set_border_width(5)

        self.image = Gtk.Image()
        self.image.set_size_request(SIZE, SIZE)
        self.get_content_area().add(self.image)

        hb = Gtk.HeaderBar()
        self.set_titlebar(hb)
        hb.set_title(title)
        hb.set_subtitle(self._url)

        button_close = Gtk.Button.new_with_mnemonic(_('Close'))
        button_close.set_halign(Gtk.Align.START)
        button_close.connect('clicked', self.close)
        button_close.get_style_context().add_class(
            Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        hb.pack_end(button_close)

        self.show_all()
        self.render()

        GLib.idle_add(self.start_server)

    def start_server(self):
        python3 = local['python3']
        exec = '/usr/share/nautilus-python/extensions/sharefile/server.py'
        path, filename = os.path.split(self._filename)
        python3[exec, self._port, self._seed, path, filename] & BG

    def render(self):
        pixbuf = create_qr(self._url)
        rectangle = self.image.get_allocation()
        if rectangle.width == 1 or rectangle.height == 1:
            width = SIZE
            height = SIZE
        else:
            width = rectangle.width
            height = rectangle.height
        scale_w = width / pixbuf.get_width() * 100
        scale_h = height / pixbuf.get_height() * 100
        if scale_w > scale_h:
            self.scale = scale_h
        else:
            self.scale = scale_w
        w = int(pixbuf.get_width() * self.scale / 100)
        h = int(pixbuf.get_height() * self.scale / 100)
        pixbuf = pixbuf.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def on_realize(self, *_):
        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        monitor_width = monitor.get_geometry().width / scale
        monitor_height = monitor.get_geometry().height / scale
        width = self.get_preferred_width()[0]
        height = self.get_preferred_height()[0]
        self.move((monitor_width - width)/2, (monitor_height - height)/2)

    def close(self, *args):
        stop_server(self._port)
        self.destroy()


if __name__ == '__main__':
    shareDialog = ShareDialog('9999', 'kaka', '/tmp/sample.jpg', 'Test')
    shareDialog.run()
