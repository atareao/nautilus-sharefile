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

import requests
import sys
from flask import Flask, request, send_from_directory


def stop_server(port):
    try:
        requests.get('https://localhost:{}/shutdown'.format(port),
                     verify=False)
    except Exception:
        pass


def start_server(port, seed, path, filename):

    app = Flask(__name__)

    # http://flask.pocoo.org/snippets/67/
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.route("/shutdown")
    def shutdown():
        shutdown_server()
        return "OK", 200

    @app.route('/<random>')
    def send(random):
        if random == seed:
            return send_from_directory(path, filename)
        return 'KO', 404

    app.run('0.0.0.0', port, debug=True, ssl_context='adhoc')


if __name__ == '__main__':
    if len(sys.argv) > 4:
        port = sys.argv[1]
        key = sys.argv[2]
        path = sys.argv[3]
        filename = sys.argv[4]
        start_server(port, key, path, filename)
    exit(0)
