#!/usr/bin/env python2

import sys
import SimpleHTTPServer
import SocketServer
class TramServerRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    # TODO
    def do_GET(self):
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    # TODO
    def do_POST(self):
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_POST(self)

Handler = TramServerRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)

server.serve_forever()