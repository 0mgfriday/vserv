#!/usr/bin/env python3

# https://github.com/python/cpython/blob/3.12/Lib/http/server.py

import argparse
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from functools import partial

class SimpleHandler(BaseHTTPRequestHandler):
    def __init__(self, timeout, redirect_location, redirect_sc, redirect_endpoint, *args, **kwargs):
        self.timeout = timeout
        self.redirect_location = redirect_location
        self.redirect_sc = redirect_sc
        self.redirect_endpoint = redirect_endpoint
        super().__init__(*args, **kwargs)

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(self.timeout)

    def version_string(self):
        """Value of Server response header"""
        return ''

    def respond(self):
        if self.redirect_location != '' and (self.redirect_endpoint == '' or self.path.startswith('/' + self.redirect_endpoint)):
            self.send_response(self.redirect_sc)
            self.send_header('Location', self.redirect_location)
        else:
            self.send_response(200)
        self.end_headers()

    def do_GET(self):
       self.respond()

    def do_HEAD(self):
       self.respond()
    
    def do_POST(self):
       self.respond()

    def do_PUT(self):
       self.respond()
    
    def do_PATCH(self):
       self.respond()

    def do_DELETE(self):
       self.respond()

    def do_OPTIONS(self):
       self.respond()

    def log_message(self, format, *args):
        print('\033[92mRequest from: ' + self.client_address[0] + ' - ' + self.log_date_time_string() + '\033[0m')
        print(self.requestline)
        print(str(self.headers))
        if ('Content-Length' in self.headers):
            content_length = int(self.headers['Content-Length'])
            if (content_length > 0):
                if (content_length > 1048576):
                    content_length = 1048576
            try:
                print(self.rfile.read(content_length).decode('utf-8'))
            except OSError:
                print('\033[93mInfo: Request timed out\033[0m')


parser = argparse.ArgumentParser(
    prog='vserv',
    description='Simple web server that logs request details',
    epilog='https://github.com/0mgfriday/vserv')

parser.add_argument('-p', '--port', required=True, help='Port to listen on')
parser.add_argument('-t', '--timeout',type=int, default=5, help='Timeout for requests')
parser.add_argument('-rl', '--redirectlocation', default='', help='Redirect request to the specified URL')
parser.add_argument('-rs', '--redirectstatuscode', type=int, choices=[301,302,303,307,308], default=302, help='Status code to use for redirects')
parser.add_argument('-re', '--redirectendpoint', default='', help='Endpoint to server redirects from. Default is all. Example: test/redir')
args = parser.parse_args()

handler = partial(
    SimpleHandler,
    args.timeout,
    args.redirectlocation,
    args.redirectstatuscode,
    args.redirectendpoint)

with HTTPServer(("", int(args.port)), handler) as httpd:
    print('\033[94mServing on port ' + args.port + '\033[0m\n')
    if args.redirectendpoint != '':
        print('\033[94mServing redirects on /' + args.redirectendpoint + '\033[0m\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)