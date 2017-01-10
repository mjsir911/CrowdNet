#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import multiprocessing

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

def timeme(method):
    def wrapper(*args, **kwargs):
        startTime = time.time() * 1000
        result = method(*args, **kwargs)
        endTime = time.time() * 1000

        print(endTime - startTime, 'ms')
        return result

    return wrapper

def timemeavg(method):
    def wrapper(*args, **kwargs):
        startTime = time.time() * 1000
        result = method(*args, **kwargs)
        endTime = time.time() * 1000

        time_took = endTime - startTime
        #print(endTime - startTime, 'ms')
        return result, time_took

    return wrapper

def multipro(function):
    def wrapper(*args, **kwargs):
        recv, send = multiprocessing.Pipe(False)
        def no(*args, **kwargs):
            args[-1].send(function(*args[:-1], **kwargs))
        args = args + (send,)
        #print(args)
        process = multiprocessing.Process(target=no, args=args, kwargs=kwargs)
        process.start()
        return recv.recv()
    return wrapper

def threaded(func):
    """http://code.activestate.com/recipes/576684-simple-threading-decorator/"""
    from threading import Thread
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        th = Thread(target=func, args=args, kwargs = kwargs)
        th.daemon = True
        return th.start()
    return wrapper

@multipro
def test(x):
    return sig(x)

def pool(funcs):
    p = multiprocessing.Pool()



def truey(l):
#print(l)
#l = l[0]
    new = [False] * len(max(l))
    for num, i in enumerate(zip(*l)):
            for value in i:
                if value:
                    new[num] = value
    return new
#raise Exception('no true values in {}'.format(l))
    print('no true values in {}'.format(l))
