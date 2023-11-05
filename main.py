from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
import json
from datetime import datetime
from threading import Thread

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('front-init/index.html')
        elif pr_url.path == '/message':
            self.send_html_file('front-init/message.html')
        else:
            self.send_html_file('front-init/error.html', 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        if 'username' in message_data and 'message' in message_data:
            message = {
                "username": message_data['username'][0],
                "message": message_data['message'][0]
            }
            self.send_message_to_socket_server(message)
            self.send_html_file('front-init/index.html', 303)
        else:
            self.send_html_file('front-init/error.html', 400)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_message_to_socket_server(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message['timestamp'] = str(datetime.now())
        message_json = json.dumps(message).encode('utf-8')
        sock.sendto(message_json, ('localhost', 5000))

def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    http_thread = Thread(target=run)
    http_thread.start()
    http_thread.join()
