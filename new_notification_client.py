import http.server
import socketserver
from database import *


def addClient(post_data):
    post_data_json = json.loads(post_data)
    db = Database("user.db")

    if post_data_json not in Database.db.items():
        return 400

    db.add_entry(post_data_json["class_name"], post_data_json["token"])
    db.close()


class MyServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        status_code = addClient(post_data)

        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


if __name__ == "__main__":
    PORT = 18573
    with socketserver.TCPServer(("", PORT), MyServer) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
