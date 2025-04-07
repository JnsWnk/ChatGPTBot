from http.server import BaseHTTPRequestHandler, HTTPServer

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

def run_health_server():
    server = HTTPServer(('0.0.0.0', 10000), HealthHandler)
    server.serve_forever()