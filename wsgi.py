import time

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from wsgiref.simple_server import make_server

from prometheus_client.exposition import generate_latest, CONTENT_TYPE_LATEST
from prometheus_toolbox.expose import get_registry
from prometheus_toolbox.expose.helpers import create_wsgi_app

ENCODING = 'utf-8'


class MyServer(ThreadingHTTPServer):

    application = None
    daemon_threads = False

    def get_app(self):
        return self.application

    def set_app(self,application):
        self.application = application


class MyRequestHandler(BaseHTTPRequestHandler):
    """Very simple request handler. Only supports GET.
    """

    def do_GET(self):  # pylint: disable=invalid-name
        """Respond after seconds given in path.
        """
        if self.path[1:] == "metrics":
            registry = get_registry()
            params = parse_qs(urlparse(self.path).query)
            if 'name[]' in params:
                registry = registry.restricted_registry(params['name[]'])
            try:
                output = generate_latest(registry)
            except:
                self.send_error(500, 'error generating metric output')
                raise
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(output)
        else:
            try:
                seconds = float(self.path[1:])
            except ValueError:
                seconds = 0.0
            if seconds < 0:
                seconds = 0.0
            text = "Waited for {:4.2f} seconds.\nThat's all.\n"
            msg = text.format(seconds).encode(ENCODING)
            time.sleep(seconds)
            self.send_response(200)
            self.send_header("Content-type", 'text/plain; charset=utf-8')
            self.send_header("Content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)


def run(server_class=MyServer,
        handler_class=MyRequestHandler,
        port=5000):
    """Run the simple server on given port.
    """
    demo_app = create_wsgi_app()
    with make_server(
            '', port, demo_app,
            server_class=server_class,
            handler_class=handler_class
    ) as httpd:
        sa = httpd.socket.getsockname()
        print("Serving HTTP on", sa[0], "port", sa[1], "...")
        httpd.serve_forever()  # serve one request, then exit


if __name__ == '__main__':
    run()
