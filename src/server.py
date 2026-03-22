from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import shutil
from urllib.parse import unquote, urlparse
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Server is running.\n")

    def do_PUT(self) -> None:
        decoded = unquote(self.path)
        normalized = decoded.replace("\\", "/")

        local_path = normalized.lstrip("/")          
        directory = os.path.dirname(local_path)   
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        with open(local_path, "wb") as f:
            f.write(data)

        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"File saved.\n")
    
    def do_DELETE(self):
        folder = self.path.strip("/")
        if os.path.isdir(folder):
            shutil.rmtree(folder)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Folder deleted.\n")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 5500
    server_name = "localhost"
    with open('config.json', 'r') as file_descriptor:
        data = json.load(file_descriptor)
        server_url = data.get("destinationUrl")
        parsed = urlparse(server_url)
        PORT = parsed.port
        server_name = parsed.hostname

    server = HTTPServer((server_name, PORT), Handler)
    print(f"Server running on port {PORT}")
    server.serve_forever()
