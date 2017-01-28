#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from candle_light import CandleLight
import SocketServer
import json
import logging

logger = logging.getLogger('phue')

candles = {'living room': CandleLight('192.168.1.120', 'LR'),
            'office': CandleLight('192.168.1.120', 'Office'),
            'kitchen': CandleLight('192.168.1.120', 'Kitchen')
          }

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.candles = CandleLight('192.168.1.120', 'Office')

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        print data
        action = data['action']
        room = data['room']
        candle_lights = candles[room.lower().replace('the','').strip()]
        if action == 'start':
            candle_lights.start_flicker()
        elif action == 'stop':
            candle_lights.stop_flicker()
        self._set_headers()
        
def run(server_class=HTTPServer, handler_class=S, port=48464):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()