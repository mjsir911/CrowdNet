#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#lol

import socketserver
import socket
import time
import struct
import http2p
import net
import test
import cortex
import random

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

class Hi(http2p.Server):
    def __init__(self, *args, **kwargs):

        self.a_queue = []

        super().__init__(*args, **kwargs)

    #@test.threaded

class RIP(http2p.Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_age = 0
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP = socketserver.UDPServer(self.address, self.UDPHandler)
        self.serve_udp()

        def got_data(s):
            #print('got queue: ', s.data)
            self.obj.axons = s.data
        self.UDPHandler.add_udp_response(['train', 'got'], got_data)

        def process_data(s):
            #print('got dataset: ', s.data)
            self.process(s.data)
        self.UDPHandler.add_udp_response(['train', 'start'], process_data)


    def process(self, dataset):
        #print('training with ', dataset)
        processed = self.obj.train(dataset, (self.place, len(self.order)))
        self.obj.axons = processed
        #print('sending processed queue: ', processed)
        #http2p.test.time.sleep(random.random() + 1 / 10)
        self.mass_udp('train/got', processed)

    def train(self, dataset):
        #print('sending start for', dataset)
        self.mass_udp('train/start', dataset)
        self.process(dataset)

    def function_train(self, func, epoch):
        avg = 0
        self.obj.func = func
        #argcount = func.__code__.co_argcount
        argcount = len(self.obj.inputs) # bad practs
        #assert argcount == len(self.inputs), 'need different amount of inputs'
        try:
            age = 0
            while age < epoch:
                if self.obj.error(0.1) > 0.95:
                    print('accuracy above 0.95 in {} epochs, breaking'.format(self.total_age))
                    break
                startTime = time.time() * 1000
                old_axons = self.obj.axons
                v_inputs  = [self.obj.random() for x in range(argcount)]
                #print('epoch is :', age, end="\r", flush=True)
                try:
                    v_outputs = func(*v_inputs)
                except Exception as e:
                    print(e)
                    continue
                v_outputs = self.obj.make_iter(v_outputs)
                self.train([v_inputs, v_outputs])
                #while old_axons == self.obj.axons and self.UDPHandler.bad == False:
                    #pass
                    #print(self.UDPHandler.bad)
                if self.UDPHandler.bad == True:
                    print('oh no')
                    self.UDPHandler.bad == False
                    continue
                endTime = time.time() * 1000
                age += 1
                avg = (avg * age + (endTime - startTime)) / (age + 1)
                print('avg is :', avg / len(self.obj.axons), end="\r", flush=True)
            print('training complete')
        except KeyboardInterrupt:
            print()
            print('wow rude')
        self.total_age += age

    def udp_client(self, path, msg, addr):
        path = cortex.introspect(path.split('/'))
        sep = chr(30).encode()
        msg = cortex.introspect(msg)
        full = path + sep + msg
        self.udp_sock.sendto(full, addr)

    def mass_udp(self, path, data):
        #print('hi')
        for peer in self.phonebook:
            #print('sending {} to {}'.format(path, peer))
            self.udp_client(path, data, peer)


    @test.threaded
    def serve_udp(self):
        print('spooling up servers')
        self.UDP.serve_forever()

    class UDPHandler(socketserver.BaseRequestHandler):
        bad = False
        """
        This class works similar to the TCP handler class, except that
        self.request consists of a pair of data and client socket, and since
        there is no connection the client address must be given explicitly
        when sending data back via sendto().
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            #print('udp connecion!')

        def handle(self):
            #data = self.request[0].strip()
            #socket = self.request[1]
            data = self.request[0]
            data = data.split(chr(30).encode())
            try:
                path = cortex.extrospect(data[0])
                self.data = cortex.extrospect(data[1])
            except struct.error:
                #print('bad thing')
                self.data = [False]
                self.bad = True
            #print(path, data)
            for response in self.responses:
                rpath, rfunc = response
                #print(path, rpath)
                if path == rpath:
                    rfunc(self)
                    #print('doing post function ', rfunc, ' to path ', path)
                    return
            print('unknown path: ', path, type(path[0]), path[0])
            print(self.responses)
            return
            #print("{} wrote:".format(self.client_address[0]))
            #print(data)
            #print(type(self.request))
            #(print(str(self.request))
            #print(cortex.extrospect(self.request[0]))
            #socket.sendto(data.uper(), self.client_address)

        responses = []
        @classmethod
        def add_udp_response(cls, path, func):
            cls.responses.append((path, func))
