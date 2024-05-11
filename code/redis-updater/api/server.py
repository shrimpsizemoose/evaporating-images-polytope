import http.server
import socketserver
import io
import os
import sys
import subprocess

from api.update_redis import update_coords_in_redis


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = os.getenv('REDIS_URL')
        if self.path in ('/', '/full'):
            evaporate = self.path != '/full'
            update_coords_in_redis(url, evaporate=evaporate)

            # Send an HTTP response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Thank you! Refresh this page to uncover more pixels")
        else:
            super().do_GET()


def main(server_class=http.server.HTTPServer, handler_class=Handler):
    PORT = int(os.getenv('PORT'))
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on 0.0.0.0 port {PORT}...')
    httpd.serve_forever()
