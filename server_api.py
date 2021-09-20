import http.server
import socketserver
from database import *


def addClient(post_data):
    post_data_json = json.loads(post_data)
    db = Database("user.db")

    if post_data_json["class_name"] not in db.db:
        db.close()
        return "404"

    db.add_entry(post_data_json["class_name"], post_data_json["token"])
    db.close()
    return "200"


def getFile(path):
    filename = "www/" + "/".join(path.split("/")[2:])
    print(filename)
    try:
        with open(filename, "rb") as r:
            file_data = r.read()

        return file_data

    except FileNotFoundError:
        pass

    return b"[404]"


class MyServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(getFile(self.path))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        status_code = addClient(post_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(status_code.encode("utf-8"))


def main(port):
    with socketserver.TCPServer(("", port), MyServer) as httpd:
        print("serving at port", port)
        httpd.serve_forever()
