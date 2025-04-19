import http.server
import socketserver
import os

PORT = 9000
FILE = "client.py"

class InviteHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == f"/{FILE}":
            with open(FILE, 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/x-python")
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_error(404)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("0.0.0.0", PORT), InviteHandler) as httpd:
    print(f"[INVITE SERVER] Hosting {FILE} on port {PORT}")
    print(f"Share this command: python3 <(curl -s http://YOUR.IP.ADDRESS:{PORT}/{FILE})")
    httpd.serve_forever()
