#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import net

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

def to_bitlist(num, wordlen=4):
    return tuple(int(n) for n in format(num, '0{}b'.format(wordlen)))
def bitlist_to_num(bitlist):
    return int(''.join(str(num) for num in bitlist), 2)

import functools
def bitmath(func):
    @functools.wraps(func)
    def wrapper(b):
        num = bitlist_to_num(b)
        result = func(num)
        return to_bitlist(result)

#@bitmath
def division(bl):
    numlen = len(bl) // 2
    numerator = bitlist_to_num(bl[:numlen])
    denominator = bitlist_to_num(bl[numlen:])
    return to_bitlist(numerator // denominator)

import itertools
def func2list(func):
    inputs = {}
    for input in itertools.product(('1', '0'), repeat=8):
        input = tuple(int(i) for i in input)
        try:
            inputs[input] = func(input)
        except:
            pass
    return inputs

def division(nums):
    numerator = nums[0]
    denominator = nums[1]
    return numerator // denominator

def func2list(func, r=16):
    inputs = {}
    for input in itertools.product(range(16), repeat=2):
        try:
            inputs[input] = (func(input),)
        except Exception as e:
            pass
    return inputs

def randomcull(inputs):
    culled = []
    for k in tuple(inputs.keys()):
        if random.random() < 0.1:
            culled.append(k)
            del inputs[k]
    return inputs, culled

class MathNet(net.DFFNet):
    @property
    def inputs(self):
        onenum = len(self._inputs) // 2
        a = bitlist_to_num(int(input.out) for input in self._inputs[:onenum])
        b = bitlist_to_num(int(input.out) for input in self._inputs[onenum:])
        return a, b
    @inputs.setter
    def inputs(self, values):
        a = values[0]
        b = values[1]
        a = to_bitlist(a)
        b = to_bitlist(b)
        values = a + b
        for input, value in zip(self._inputs, values):
            input.input = value

    @property
    def outputs(self):
        return bitlist_to_num(round(output.out) for output in self._outputs)
    @outputs.setter
    def outputs(self, values):
        values = to_bitlist(values[0])
        for output, value in zip(self._outputs, values):
            output.target = value
