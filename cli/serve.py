from http.server import HTTPServer, SimpleHTTPRequestHandler

from .base import cli


@cli.command()
def serve():
    class BuildHTTPRequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="build", **kwargs)

    print("Local server running on http://localhost:8000")
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, BuildHTTPRequestHandler)
    httpd.serve_forever()
