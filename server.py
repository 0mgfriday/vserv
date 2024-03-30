#!/usr/bin/env python3

# https://github.com/python/cpython/blob/3.12/Lib/http/server.py

import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(5)

    def version_string(self):
        """Value of Server response header"""
        return ''

    def do_GET(self):
       self.send_response(200)
       self.end_headers()

    def do_HEAD(self):
       self.send_response(200)
       self.end_headers()
    
    def do_POST(self):
       self.send_response(200)
       self.end_headers()

    def do_PUT(self):
       self.send_response(200)
       self.end_headers()
    
    def do_PATCH(self):
       self.send_response(200)
       self.end_headers()

    def do_DELETE(self):
       self.send_response(200)
       self.end_headers()

    def do_OPTIONS(self):
       self.send_response(200)
       self.end_headers()

    def log_message(self, format, *args):
        print('Request from: ' + self.client_address[0] + ' - ' + self.log_date_time_string())
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
                print('Info: Request timed out')
        
if len(sys.argv)-1 != 1:
    print("""
Usage: {} <port_number>
    """.format(sys.argv[0]))
    sys.exit()

with HTTPServer(("", int(sys.argv[1])), SimpleHandler) as httpd:
    print('Serving on port ' + sys.argv[1] + '\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)