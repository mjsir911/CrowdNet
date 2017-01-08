#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')
import net
import cortex
import socket
import time
import test
import http.server

__appname__     = ""
__author__      = "Marco Sirabella"
__copyright__   = ""
__credits__     = ["Marco Sirabella"]  # Authors and bug reporters
__license__     = "GPL"
__version__     = "1.0"
__maintainers__ = "Marco Sirabella"
__email__       = "msirabel@gmail.com"
__status__      = "Prototype"  # "Prototype", "Development" or "Production"
__module__      = ""


class Server():

    def __init__(self, obj=None, address=(socket.gethostbyname(socket.gethostname()), 37598), phonebook={('sirabella.org', 6702)}):
    #def __init__(self, port):
        # Server settings
        self.phonebook = {(socket.gethostbyname(addr), port) for addr, port in phonebook} # who woulda thought
        if address[0] == 'localhost' or address[0] == '127.0.0.1':
            self.address = address
        else:
            pub_ip = self.get('/https://github.com/mjsir911/CrowdNet', ('ip.42.pl', 80))
            self.address = pub_ip, address[1]
        try:
            self.phonebook.remove(self.address)
        except KeyError:
            pass

        def junk(s):
            self._obj = s.data
            #print('i "set" it')

        def add_phone(s):
            self.phonebook.add((s.client_address[0], s.data))
            print('adding peer ', s.client_address)

        self._obj = obj
        self.Request.add_post_response(['phonebook'], add_phone)
        self.Request.add_post_response(['phonebook', 'remove'], lambda s: self.phonebook.remove(s.data))
        self.Request.add_post_response(['phonebook', 'add'], lambda s: self.equalize(True))
        self.Request.add_post_response(['dill', 'set'], junk)

        self.Request.add_get_response(['dill'], lambda s: cortex.introspect(self._obj))
        self.Request.add_get_response(['phonebook'], lambda s: cortex.introspect(self.phonebook))

        self.httpd = http.server.HTTPServer(self.address, self.Request)
        self.httpd.request_queue_size = 100
        self.serve()
        self.equalize()

    @property
    def obj(self):
        #print('recursive2?')
        return self._obj

    @obj.setter
    def obj(self, obj):
        if obj != self._obj:
            print('recursive?')
            self._obj = obj
            self.mass_post('dill/set', obj)
        else:
            print('no feedback pls')

    def equalize(self, recursive=False):
        self.order
        for peer in list(self.phonebook):
            try:
                data = self.get('dill', peer)
                #data = None
            except ConnectionError as e:
                badpeer = peer
                print('removing {} from phonebook due to {}'.format(badpeer, e))
                self.phonebook.remove(badpeer)
                self.mass_post('phonebook/remove', badpeer)

                continue
            #print('{} data from {}'.format(data, peer))
            if data:
                self.obj = data
            else:
                pass
                #print('{} has no network'.format(peer))
            phonebook = self.get('phonebook', peer)
            self.post('phonebook', peer, self.address[1])
            if not recursive:
                for phone in phonebook:
                    if phone != self.address:
                        # if new address, tell the rest there is a new address
                        #self.mass_post('phonebook/add', None)
                        self.phonebook.add(phone)
        return

    @classmethod
    def get(cls, path, address):
        conn = http.client.HTTPConnection(*address)
        conn.connect()
        conn.request("GET", "/{}".format(path))
        print('getting response from {} at path {}'.format(address, path))
        response = conn.getresponse()
        data = response.read()
        try:
            data = cortex.extrospect(data)
        except:
            data = data.decode()
        return data

    @classmethod
    def post(cls, path, address, data):
        conn = http.client.HTTPConnection(*address)
        conn.connect()
        #print('posting to ', address)
        conn.request("POST", "/{}".format(path), cortex.introspect(data))
        print('posting response from {} at path {}'.format(address, path))
        response = conn.getresponse()
        data = response.read()
        #return cortex.introspect(data)
        return

    def mass_post(self, path, data):
        for peer in list(self.phonebook):
            #test.time.sleep(10)
            #print('posting data to peer ', peer, ' at path ', path)
            self.post(path, peer, data)

    @property
    def order(self):
        combined = lambda ip, port: int(''.join(bin(int(x)+256)[3:] for x in ip.split('.')) + format(port, '016b'), 2)
        all_addr = list(self.phonebook) + [self.address]
        order = sorted(combined(*addr) for addr in all_addr)
        own = order.index(combined(*self.address))
        self.place = own
        return order

    @test.threaded
    def serve(self):
        self.httpd.serve_forever()

    @test.threaded
    def loop(self):
        time.sleep(1)
        while not self.obj:
            self.equalize()
            time.sleep(0.1)


        old = None
        while True:
            if old != self.phonebook:
                self.equalize()
                print('network changed')
            old = set(self.phonebook)
            time.sleep(1)


    class Request(http.server.BaseHTTPRequestHandler):

        def log_message(self, *args, **kwargs):
            """just to override"""
            pass

        g_responses = []
        @classmethod
        def add_get_response(cls, path, func):
            cls.g_responses.append((path, func))

        # GET
        def do_GET(self):
            # Send response status code
            #print('am i freezin up everything?', self.path)
            self.send_response(200)

            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()

            #self.parent_server.phonebook.add(self.client_address)

            path = self.path.split('/')[1:]
            for response in self.g_responses:
                rpath, rfunc = response
                if path == rpath:
                    msg = rfunc(self)
                    #print('doing get function ', rfunc, ' to path ', path)
                    self.wfile.write(msg)
                    return
            print(path, self.g_responses)
            return

            # Write content as utf-8 data
            return

        def do_POST(self):
            #print('am i freezin up everything?', self.path)
            self.data = cortex.extrospect(self.rfile.read(int(self.headers["Content-Length"])))
            self.send_response(200)
            self.send_header("Content-Length", '0')
            self.end_headers()
            self.wfile.write(b'')
            path = self.path.split('/')[1:]
            #print(self.data)
            for response in self.p_responses:
                rpath, rfunc = response
                #print(path, rpath)
                if path == rpath:
                    rfunc(self)
                    #print('doing post function ', rfunc, ' to path ', path)
                    return
            print('unknown path: ', path, type(path[0]), path[0])
            print(self.p_responses)
            return
            """
            if path[0] == 'phonebook':
                if path[1] == 'remove':
                    p.phonebook.remove(data)
                else:
                    p.phonebook.add((self.client_address[0], data))
                    """

        p_responses = []
        @classmethod
        def add_post_response(cls, path, func):
            cls.p_responses.append((path, func))
