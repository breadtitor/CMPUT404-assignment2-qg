#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle,guo qiaoxi， https://github.com/tywtyw2002, and https://github.com/treedust
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
import urllib.parse
#no change
def help():
    print("httpclient.py [GET/POST] [URL]\n")
#no change
class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
#no change
class HTTPClient(object):
    #def get_host_port(self,url):
#no change
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None
#need change
    def get_code(self, data):
        return data.split()[1]
       
        #return None
#need change
    def get_headers(self,data):
        header_end = data.index("\r\n\r\n") + 4
        return data[:header_end]
    
        #return None
#need change
    def get_body(self, data):
        header_end = data.index("\r\n\r\n") + 4
        return data[header_end:]
        #return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        #no change
    def close(self):
        self.socket.close()

    # read everything from the socket
    #no change
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')
#need change
    def GET(self, url, args=None):
        parsed_url = urllib.parse.urlparse(url)
        code = 500
        body = ""
        host_name = parsed_url.hostname
        port_num = parsed_url.port
        scheme = parsed_url.scheme

        if not port_num:
            if scheme == "http":
                port_num = 80
            elif scheme == "https":
                port_num = 443
        self.connect(host_name, port_num)

        path = parsed_url.path if parsed_url.path else '/'
        
        request = f'GET {path} HTTP/1.1\r\nHost: {host_name}\r\nAccept-Charset: UTF-8\r\nConnection:close\r\n\r\n'
        self.sendall(request)

        response = self.recvall(self.socket)

        code = int(self.get_code(response))
        body = self.get_body(response)
        self.close()

        return HTTPResponse(code, body)
    
#need change
  
    def POST(self, url, args=None):
        parsed_url = urllib.parse.urlparse(url)
        code = 500
        body = ""
        host_name = parsed_url.hostname
        port_num = parsed_url.port
        scheme = parsed_url.scheme

        if not port_num:
            if scheme == "http":
                port_num = 80
            elif scheme == "https":
                port_num = 443
        self.connect(host_name, port_num)

        path = parsed_url.path if parsed_url.path else '/'
        request = f'POST {path} HTTP/1.1\r\nHost: {host_name}\r\nAccept-Charset: UTF-8\r\nConnection:close\r\n'

        if not args:
            request = 'POST ' + path + ' HTTP/1.1\r\nHost: ' + host_name + '\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: ' + str(0) + '\r\nConnection: close\r\n\r\n' + ''
            print("no args")
          
            
        else:
            addargs = urllib.parse.urlencode(args)
            request = 'POST ' + path + ' HTTP/1.1\r\nHost: ' + host_name + '\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: ' + str(len(addargs)) + '\r\nConnection: close\r\n\r\n' + addargs
        # if args:
        #     request += f'Content-Length: {len(args)}\r\n\r\n{args}'
        # else:
        #     request += '\r\n'
        print(request)        
        self.sendall(request)

        response = self.recvall(self.socket)
        code = int(self.get_code(response))
        body = self.get_body(response)
        print(response)
        self.close()

        return HTTPResponse(code, body)
#nochange
    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    #no change
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
