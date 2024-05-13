import http.server
import socketserver
import io
import os
import sys
import subprocess

import redis
from api.update_redis import update_coords_in_redis
from api.conway import read_grid, iter_grid, write_grid


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = os.getenv('REDIS_URL')
        if self.path in ('/', '/full'):
            evaporate = self.path != '/full'
            update_coords_in_redis(
                url,
                evaporate=evaporate,
                num_pixels_each_hit=70,
                max_seconds_pixel_ttl=10,
            )

            # Send an HTTP response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(
                b"<H1>Thank you! &#128640;</H1><p>Refresh to uncover more pixels</p>"
            )
        elif self.path == '/conway-iter':
            r = redis.from_url(url)
            grid = read_grid(r)
            r.flushdb()
            write_grid(r, iter_grid(grid))
            self.send_response(200)
            self.send_header('Content-type', 'text/pain')
            self.end_headers()
            self.wfile.write(b"pew pew")
        elif self.path == '/clear':
            r = redis.from_url(url)
            r.flushdb()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"It was there and now it's gone")
        else:
            super().do_GET()


def main(server_class=http.server.HTTPServer, handler_class=Handler):
    PORT = int(os.getenv('PORT'))
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on 0.0.0.0 port {PORT}...')
    httpd.serve_forever()
