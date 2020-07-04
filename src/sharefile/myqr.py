#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of GQRCode
#
# Copyright (c) 2012-2019 Lorenzo Carbonell Cerezo <a.k.a. atareao>
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

from mylibs import theqrmodule
from mylibs.draw import image2pixbuf

# Positional parameters
#   words: str
#
# Optional parameters
#   version: int, from 1 to 40
#   level: str, just one of ('L','M','Q','H')
#   picutre: str, a filename of a image
#   colorized: bool
#   constrast: float
#   brightness: float
#   save_name: str, the output filename like 'example.png'
#   save_dir: str, the output directory
#
# See [https://github.com/sylnsfar/qrcode] for more details!


def create_qr(words, version=1, level='H', colorized=False, contrast=1.0,
              brightness=1.0):
    supported_chars = r"0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñop\
qrstuvwxyz ··,.:;+-*/\~!@#$%^&`'=<>[]()?_{}|"

    # check every parameter
    if not isinstance(words, str) or\
            any(i not in supported_chars for i in words):
        raise ValueError(
            'Wrong words! Make sure the characters are supported!')
    if not isinstance(version, int) or version not in range(1, 41):
        raise ValueError(
            'Wrong version! Please choose a int-type value from 1 to 40!')
    if not isinstance(level, str) or len(level) > 1 or level not in 'LMQH':
        raise ValueError(
            "Wrong level! Please choose a level from {'L','M','Q','H'}!")
    try:
        ver, pilimage = theqrmodule.get_qrcode_pilimage(version, level, words)
        return image2pixbuf(pilimage)
    except Exception as e:
        print(e)
    return None
