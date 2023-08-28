import http.server
import socketserver
import flask
PORT = 8000

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Serveur actif sur le port", PORT)
    httpd.serve_forever()