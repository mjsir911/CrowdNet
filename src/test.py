#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import multiprocessing
import collections

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
        if result:
            return result, time_took
        else:
            return time_took

    return wrapper

@timemeavg
def benchmark():
    x = 0
    while x < 1e6:
        x += 1

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


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    """http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks"""
    for i in range(0, len(l), n):
        yield l[i:i + n]



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


def mad(base=4):
    def decorator(func):
        def wrapper(binary):
            first = int(''.join(str(round(n)) for n in binary[:base]), 2)
            last = int(''.join(str(round(n)) for n in binary[base:]), 2)
            input_bin = [int(z) for z in list(format(func(first, last), '0{}b'.format(base)))]
            return input_bin
        return wrapper
    return decorator


#this is a mess
class bitarray(list):
    def __init__(self, iterable=None):
        #super().__init__(bytes)
        super().__init__()
        if iterable:
            for item in iterable:
                self.append(item)

    def __repr__(self):
        return 'bitarray({})'.format(self)

    def __str__(self):
        x = '0b'
        for bit in self:
            x += str(bit)
        return x

    def __setitem__(self, index, value):
        super().__setitem__(index, self._value_bin(value))

    @classmethod
    def _value_bin(cls, value):
        if isinstance(value, int):
            if 0 <= value <= 1:
                return value
            else:
                raise ValueError('bit must be in range(0, 1)')
        else:
            raise ValueError('an integer is required')

    def _binary(func):
        def wrapper(self, value):
            bin = self._value_bin(value)
            return func(self, bin)
        return wrapper

    @classmethod
    def _iterable_bin(cls, iterable):
        buffer = []
        for value in iterable:
            buffer.append(cls._value_bin(value))
        return buffer

    def _iterator(func):
        def wrapper(self, object):
            iterable = self._iterable_bin(object)
            return func(self, iterable)
        return wrapper



    @_binary
    def append(self, value):
        super().append(value)

    @_iterator
    def extend(self, iterable):
        super().extend(iterable)

    def insert(self, index, value):
        super().insert(index, self._value_bin(value))


    def _math(func):
        def wrapper(self, object):
            return type(self)(func(self, object))
        return wrapper

    @_math
    @_iterator
    def __add__(self, obj):
        return super().__add__(obj)
    @_math
    @_iterator
    def __radd__(self, obj):
        return super().__radd__(obj)

    @_iterator
    def __iadd__(self, obj):
        return super().__iadd__(obj)

    @_math
    def __mul__(self, obj):
        return super().__mul__(obj)
    @_math
    def __rmul__(self, obj):
        return super().__rmul__(obj)
    def __imul__(self, obj):
        return super().__imul__(obj)

    def convert_to_base(self, base):
        converted = []
        for i in range(0, len(self), base):
            thing = ''
            for j in range(0, base):
                thing += (str(self[j + i]))
            converted.append(int(thing, 2))
        return converted
