#!/usr/bin/python3
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
    gi.require_version('GObject', '2.0')
    gi.require_version('Nautilus', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Nautilus as FileManager
import sys
import os
import locale
import gettext
try:
    sys.path.insert(1, '/usr/share/nautilus-python/extensions/sharefile/')
    from sharedialog import ShareDialog
except Exception as e:
    print(e)
    exit(-1)


APP = '$APP$'
ICON = '$APP$'
VERSION = '$VERSION$'
LANGDIR = os.path.join('usr', 'share', 'locale-langpack')

current_locale, encoding = locale.getdefaultlocale()
language = gettext.translation(APP, LANGDIR, [current_locale])
language.install()
try:
    _ = language.gettext
except Exception as exception:
    _ = str


class ShareFileMenuProvider(GObject.GObject, FileManager.MenuProvider):
    """
    Implements the 'Share File' extension to the File Manager\
    right-click menu
    """

    def __init__(self):
        """
        File Manager crashes if a plugin doesn't implement the __init__\
        method
        """
        GObject.GObject.__init__(self)

    def process(self, widget, afile, window):
        port = '9999'
        seed = 'download'
        shareDialog = ShareDialog(port, seed, afile, _('Share file'))
        shareDialog.run()

    def get_file_items(self, window, sel_items):
        """
        Adds the 'Share File' menu item to the File Manager\
        right-click menu, connects its 'activate' signal to the 'run'\
        method passing the selected File
        """
        if len(sel_items) == 1 and not sel_items[0].is_directory():
            afile = sel_items[0].get_location().get_path()
            top_menuitem = FileManager.MenuItem(
                name='ShareFileMenuProvider::Gtk-sharefile-top',
                label=_('Share file'),
                tip=_('Share file with a QR'))
            top_menuitem.connect('activate',
                                 self.process,
                                 afile,
                                 window)
            return top_menuitem,
        return
