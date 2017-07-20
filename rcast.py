#!/usr/bin/env python

import urllib, urllib2, os, sys, thread, base64, signal, socket, SimpleHTTPServer, SocketServer

def signal_handler(signal, frame):
        print('You pressed Ctrl+C, stopping. Casting may continue for some time.')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ip = 'raspberrypi.local:2020'

tocast = sys.argv[1]
subtitle_file_name, sub_tocast = [None, None]

try:
    sub_tocast = sys.argv[2]
    if not os.path.isfile(sub_tocast):
        print "Sub not found!"
        sys.exit(0)
    else:
        subtitle_file_name = os.path.split(sub_tocast)[1]
except Exception:
    pass

print "-----------------------------"
print "Casting "+tocast
print "-----------------------------"

if not os.path.isfile(tocast):
    print "File not found!"
    sys.exit(0)

print "Do not close this program while playing the file"
print "Press Ctrl+C to stop"
print "-----------------------------"

path = os.path.split(tocast)[0]

os.chdir(path)

filename = os.path.split(tocast)[1]

PORT = 8080

class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = MyTCPServer(("", PORT), Handler)

thread.start_new_thread( httpd.serve_forever, ())



encoded_string = urllib.quote_plus("http://localhost:8080/"+filename)

full_url = "http://"+ip+"/stream?url="+encoded_string

if subtitle_file_name != None:
    full_url += "&subtitles=" + urllib.quote_plus(
        "http://localhost:8080/" + subtitle_file_name)

print "Calling "+full_url

urllib2.urlopen(full_url).read()

# We don't want to quit directly, pause until Ctrl+C
signal.pause()
