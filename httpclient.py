#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
    	host = url.hostname
    	port = url.port
    	if port == None:
    		port = 80
    	path = url.path
    	if url.params != "":
    		path = path + ';' + url.params
    	elif url.query != "":
    		path = path + '?' + url.query
    	elif url.fragment != "":
    		path = path + '#' + url.fragment
    	return host,port,path

    def connect(self, host, port):
        # use sockets!
        Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        Socket.connect((host,port))
        return Socket

    def get_code(self, data):
    	code = int(data.split()[1])
        return code

    def get_headers(self,data):
    	header = data.split("\r\n\r\n")[0]
        return header

    def get_body(self, data):
    	body = data.split("\r\n\r\n")[1]
        return body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        host,port,path = self.get_host_port(urlparse(url))
        sock = self.connect(host,port)
        sock.sendall("GET " + path + " HTTP/1.1\r\n" + "Host: " + host + "\r\n\r\n")
        response = self.recvall(sock)
        code = self.get_code(response)
        body = self.get_body(response)
        #print code + "\n" + body
        print response
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host,port,path = self.get_host_port(urlparse(url))
        sock = self.connect(host,port)
        #sock.sendall
        arg_length = str(0)
        argrument = ""
        if args != None:
        	argrument = urllib.urlencode(args)
        	arg_length = str(len(argrument))
        #arg_length = len(args)
        request = "POST " + path + " HTTP/1.1\r\nHost: " + host + "\r\nContent-Type: application/x-www-form-urlencoded; charset=utf-8\r\n"
        request += "Content-Length: " + arg_length + "\r\n\r\n" + argrument
        sock.sendall(request)
        response = self.recvall(sock)
        print response
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
