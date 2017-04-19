#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


"""thanks to this guy for helping teach about backpropogation with complex maths"""
"""https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/"""

class Axon():
    def __init__(self,  iNeuron, oNeuron, weight=None):
        iNeuron._oAxon.append(self)
        oNeuron._iAxon.append(self)
        self.neurons = (iNeuron, oNeuron)
        if weight:
            self.weight = weight
        else:
            self.weight = 0.5

    @property
    def value(self):
        return self.weight * self.neurons[0].out

import functools
def pLock(func):
    @functools.wraps(func)
    def wrapper(self):
        if not hasattr(self, '_lock'):
            self._lock = {}
        elif not isinstance(self._lock, dict):
            raise

        if self._done and self._lock.get(func.__name, False):
            return self._lock[func.__name__]
        else:
            r = func(self)
            self._lock[func.__name__] = r
            return r
    return wrapper

op = sum

import math
class Neuron():
    def __init__(self, value=None):
        self._iAxon = []
        self._oAxon = []
        self._done = False
        if value:
            self._value = value
        else:
            self._value = None

    @property
    def net(self):
        return op(i.value for i in self._iAxon)

    @property
    def out(self):
        if self._value:
            return self._value
        else:
            return 1 / (1 + math.exp(-self.net))


class Input(Neuron):
    def __init__(self, value=None):
        super().__init__(value)

class Output(Neuron):
    def __init__(self, target=None):
        super().__init__()
        if target:
            self._target = target
        else:
            self._target = 0

    @property
    def target(self):
        return self._target
    @target.setter
    def target(self, value):
        self._done = False
        self._target = value

    @property
    @pLock
    def net_derivative(self):
        print('doin')
        self._done = True
        return -(self.target - self.value)

import itertools
class DFFNet():
    """
    Deep feed forward neural network
      >>> z = DFFNet(2, [2], 1)
    """
    def __init__(self, input_neurons, hidden_neurons, output_neurons, eta=1):
        self.eta = eta

        self._inputs  = tuple(      Input()  for _ in range(input_neurons))
        self._hiddens = tuple(tuple(Neuron() for _ in range(i)) for i in hidden_neurons)
        self._outputs = tuple(      Output() for _ in range(output_neurons))
        self.neurons  = (self._inputs,) + self._hiddens + (self._outputs,)
        self.axons = []
        for one, next in zip(self.neurons, self.neurons[1:]):
            for iNeuron, oNeuron in itertools.product(one, next):
                self.axons.append(Axon(iNeuron, oNeuron))
        print(self.axons)
        #print(self.neurons)

class ITest():
    def __init__(self):
        self._inputs = (Input(0.05), Input(0.10), Neuron(1))
        self._hiddens = (Neuron(), Neuron(), Neuron(1))
        self._outputs = (Output(0.01), Output(0.99))
        self.axons = []
        i1, i2 = self._inputs[:2]
        h1, h2 = self._hiddens[:2]
        o1, o2 = self._outputs
        s1, s2 = self._inputs[2], self._hiddens[2]

        self.axons.append(Axon(i1, h1, 0.15))
        self.axons.append(Axon(i2, h1, 0.20))
        self.axons.append(Axon(i1, h2, 0.25))
        self.axons.append(Axon(i2, h2, 0.30))

        self.axons.append(Axon(s1, h1, 0.35))
        self.axons.append(Axon(s1, h2, 0.35))

        self.axons.append(Axon(h1, o1, 0.40))
        self.axons.append(Axon(h2, o1, 0.45))
        self.axons.append(Axon(h1, o2, 0.50))
        self.axons.append(Axon(h2, o2, 0.55))

        self.axons.append(Axon(s2, o1, 0.60))
        self.axons.append(Axon(s2, o2, 0.60))

if __name__ == '__main__':
    import doctest
    z = ITest()
    #doctest.testmod()
