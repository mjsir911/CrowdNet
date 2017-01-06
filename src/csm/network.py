#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')
import net
import cortex
import socket
import time
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

def threaded(func):
    """http://code.activestate.com/recipes/576684-simple-threading-decorator/"""
    from threading import Thread
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Thread(target = func, args = args, kwargs = kwargs).start()
    return wrapper


class Server():

    def __init__(self, port, phonebook={('127.0.0.1', 8000)}):
    #def __init__(self, port):
        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        #phonebook = {('127.0.0.1', 8000)}
        self.phonebook = phonebook
        self.address = ('127.0.0.1', port)
        self.weight = []
        try:
            self.phonebook.remove(self.address)
        except KeyError:
            pass
        # eta, inp, [hid], out
        #self.nn = self.NN(1, 1, [1], 1)
        self.nn = None
        self.Request.parent_server = self
        self.httpd = http.server.HTTPServer(self.address, self.Request)
        self.serve()
        self.loop()

    def NN(self, *args, **kwargs):
        nn = self._NN(*args, **kwargs, networked=True)
        try:
            nn.pb = self.phonebook
            nn.addr = self.address
            nn.post = self.post
            #nn.eq = self.equalize
        except Exception as e:
            print(e)
            print('probs not network')
            pass

        return nn

    class _NN(net.Net):
        def train(self, dataset):
            if self.networked:
                for peer in [self.addr] + list(self.pb):
                    self.post('train', peer, dataset)
                    time.sleep(0.1) # I have to do this because it doesnt wait for the rest to be done to continue on to the next one
            super().train(dataset)

    """
    def start(self, dataset):
        assert self.nn
        self.equalize()
        for peer in list(self.phonebook) + [self.address]:
            self.post('train', peer, dataset)
        #self.old_train(dataset)replace this later
        """

    def equalize(self):
        self.order
        for peer in list(self.phonebook):
            try:
                data = self.get('dill', peer)
            except ConnectionError as e:
                badpeer = peer
                print('removing {} from phonebook due to {}'.format(badpeer, e))
                self.phonebook.remove(badpeer)
                for peer in self.phonebook:
                    self.post('phonebook/remove', peer, badpeer)

                continue
            #print('{} data from {}'.format(data, peer))
            if data:
                self.nn = data
            else:
                pass
                #print('{} has no network'.format(peer))
            phonebook = self.get('phonebook', peer)
            self.post('phonebook', peer, self.address[1])
            for phone in phonebook:
                if phone != self.address:
                    self.phonebook.add(phone)
        return

    @classmethod
    def get(cls, path, address):
        conn = http.client.HTTPConnection(*address)
        conn.connect()
        conn.request("GET", "/{}".format(path))
        response = conn.getresponse()
        data = response.read()
        return cortex.extrospect(data)

    @classmethod
    def post(cls, path, address, data):
        conn = http.client.HTTPConnection(*address)
        conn.connect()
        #print('posting to ', address)
        conn.request("POST", "/{}".format(path), cortex.introspect(data))
        response = conn.getresponse()
        data = response.read()
        #return cortex.introspect(data)
        return

    @classmethod
    def truey(cls, l):
        #print(l)
        #l = l[0]
        for i in l:
            if i:
                return i
        #raise Exception('no true values in {}'.format(l))
        print('no true values in {}'.format(l))
        return [False] * len(l)
        return None

    @property
    def order(self):
        combined = lambda ip, port: int(''.join(bin(int(x)+256)[3:] for x in ip.split('.')) + format(port, '016b'), 2)
        all_addr = list(self.phonebook) + [self.address]
        order = sorted(combined(*addr) for addr in all_addr)
        own = order.index(combined(*self.address))
        self.place = own
        return order

    @property
    def datarange(self):
        front = int(len(self.nn._axons) / len(self.order) * self.place)
        back = int(len(self.nn._axons) / len(self.order) * (self.place + 1))
        #return int(len(self.nn._axons) / len(self.order) * self.place) , int(len(self.nn._axons) /  len(self.order) * (self.place + 1))
        return front, back

    @threaded
    def serve(self):
        self.httpd.serve_forever()

    @threaded
    def loop(self):
        time.sleep(1)
        while not self.nn:
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

        # GET
        def do_GET(self):
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()

            #self.parent_server.phonebook.add(self.client_address)

            # Send message back to client
            if self.path == '/dill':
                #print('self.nn = ', self.parent_server.nn)
                msg = cortex.introspect(self.parent_server.nn)
            elif self.path == '/phonebook':
                msg = cortex.introspect(self.parent_server.phonebook)
            else:
                msg = b''
            # Write content as utf-8 data
            self.wfile.write(msg)
            return

        def do_POST(self):
            data = cortex.extrospect(self.rfile.read(int(self.headers["Content-Length"])))
            self.send_response(200)
            self.send_header("Content-Length", '0')
            self.end_headers()
            self.wfile.write(b'')
            p = self.parent_server
            if self.path == '/phonebook':
                p.phonebook.add((self.client_address[0], data))

            elif self.path == '/train':
                self.send_data(data)

            elif self.path == '/data':
                #print('recvd data :', data)
                p.weight.append(data)

                if len(p.weight) == len(p.phonebook) + 1:
                    #print('len of p.weights is', len(p.weight))
                    #print('doing truey to: ', p.weight)
                    p.nn.axons = [m for m in map(p.truey, zip(*p.weight))]
                    #p.weight = []

            elif self.path == '/phonebook/remove':
                p.phonebook.remove(data)

            else:
                print(self.path)
                pass

            return

        @threaded
        def send_data(self, data):
            p = self.parent_server
            x = p.nn.axons
            y = p.place
            l = len(p.order)
            #axon_range = y * 2 , len(x) //  l + y * 2
            #axon_range = int((y / l) * len(x)), (len(x) // l) * y * 2
            #axon_range = len(x) // l * y , len(x) //  l * (y + 1)
            #axon_range = int(len(x) / l * y) , int(len(x) /  l * (y + 1))
            #print('training {} axons with {} data'.format(axon_range, data))
            net = p.nn
            net.a_range = p.datarange
            p.equalize()
            #p.weight = [net.old_train(data, axon_range=p.datarange)]  # MORE EFFICIENT
            p.weight = []
            weight_to_send = [net.old_train(data, axon_range=p.datarange)]
            #print(p.weight)
            #print(p.address)
            for peer in tuple(p.phonebook) + (p.address,):
            #for peer in p.phonebook: # MORE EFFICIENT
                #print('posting data {} to peer {}'.format(weight_to_send, peer))
                p.post('data', peer, weight_to_send[0])
