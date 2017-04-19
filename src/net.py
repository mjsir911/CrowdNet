#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


"""thanks to this guy for helping teach about backpropogation with complex maths"""
"""https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/"""

import functools
def pLock(func):
    @property
    @functools.wraps(func)
    def wrapper(self):
        if not hasattr(self, '_lock'):
            self._lock = {}
        elif not isinstance(self._lock, dict):
            raise

        if self._done and self._lock.get(func.__name__, False):
            return self._lock[func.__name__]
        else:
            r = func(self)
            self._lock[func.__name__] = r
            return r
    return wrapper

"""
def pLock(func):
    @property
    @functools.wraps(func)
    def wrapper(self):
        return func(self)
    return wrapper
    """

class Axon():
    def __init__(self,  iNeuron, oNeuron, weight=None):
        iNeuron._oAxon.append(self)
        oNeuron._iAxon.append(self)
        self.iNeuron = iNeuron
        self.oNeuron = oNeuron
        self.neurons = (iNeuron, oNeuron)
        if weight:
            self.weight = weight
        else:
            self.weight = random.random()

    @property
    def value(self):
        return self.weight * self.iNeuron.out

    @property
    def error(self):
        return self.oNeuron.partial_derivative * self.oNeuron.net_derivative \
                * self.weight

    def backprop(self, eta):
        delta_error = self.oNeuron.partial_derivative * \
        self.oNeuron.net_derivative * self.iNeuron.out
        self.new_weight = self.weight - eta * delta_error
        #print(self.new_weight)

    def lock(self):
        self.weight = self.new_weight
        self.oNeuron._done = False
        self.iNeuron._done = False


op = sum

import math
class Neuron():
    def __init__(self):
        self._iAxon = []
        self._oAxon = []
        self._done = False

    @pLock
    def net(self):
        return op(i.value for i in self._iAxon)

    @pLock
    def out(self):
        return 1 / (1 + math.exp(-self.net))

    @pLock
    def net_derivative(self):
        return sum(axon.error for axon in self._oAxon)

    @pLock
    def partial_derivative(self):
        return self.out * (1 - self.out)

class Static(Neuron):
    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    def out(self):
        return self._value

class Input(Neuron):
    def __init__(self):
        super().__init__()
        self._value = 0

    @property
    def out(self):
        return self._value

    @out.setter
    def input(self, value):
        self._value = value

class Output(Neuron):
    def __init__(self):
        super().__init__()
        self._target = 0

    @property
    def target(self):
        return self._target
    @target.setter
    def target(self, value):
        self._done = False
        self._target = value

    @pLock
    def net_derivative(self):
        self._done = True
        return -(self.target - self.out)

import itertools
class NNet():
    def __init__(self, eta=0):
        self.eta = eta
        self.axons = []

    @property
    def inputs(self):
        return [input.out for input in self._inputs]
    @inputs.setter
    def inputs(self, values):
        for input, value in zip(self._inputs, values):
            input.input = value

    @property
    def outputs(self):
        return [output.out for output in self._outputs]
    @outputs.setter
    def outputs(self, values):
        for output, value in zip(self._outputs, values):
            output.target = value

    def back_pass(self):
        for axon in self.axons:
            axon.backprop(self.eta)
        for axon in self.axons:
            axon.lock()

    def train(self, dataset, epoch):
        age = 0
        while age < epoch:
            datum = dataset[random.randint(0, len(dataset) - 1)]
            self.inputs  = datum[0]
            self.outputs = datum[1]
            self.back_pass()
            age += 1
            print('epoch is {}'.format(age), end='\r')

class DFFNet(NNet):
    """
    Deep feed forward neural network
      >>> z = DFFNet(2, [2], 1)
    """
    def __init__(self, input_neurons, hidden_neurons, output_neurons, eta=1):
        super().__init__(eta)

        self._inputs  = tuple(      Input()  for _ in range(input_neurons))
        self._hiddens = tuple(tuple(Neuron() for _ in range(i)) for i in hidden_neurons)
        self._outputs = tuple(      Output() for _ in range(output_neurons))
        self.neurons  = (self._inputs,) + self._hiddens + (self._outputs,)
        for one, next in zip(self.neurons, self.neurons[1:]):
            for iNeuron, oNeuron in itertools.product(one, next):
                self.axons.append(Axon(iNeuron, oNeuron))

class ITest(NNet):
    def __init__(self):
        super().__init__(0.5)

        self._inputs = (Input(), Input(), Static(1))
        self._inputs[0].input = 0.05
        self._inputs[1].input = 0.10

        self._hiddens = ((Neuron(), Neuron(), Static(1)),)

        self._outputs = (Output(), Output())
        self._outputs[0].target = 0.01
        self._outputs[1].target = 0.99

        self.neurons  = (self._inputs,) + self._hiddens + (self._outputs,)

        i1, i2 = self._inputs[:2]
        h1, h2 = self._hiddens[0][:2]
        o1, o2 = self._outputs
        s1, s2 = self._inputs[2], self._hiddens[0][2]



        self.axons.append(Axon(i1, h1, 0.15))
        self.axons.append(Axon(i2, h1, 0.20))
        self.axons.append(Axon(i1, h2, 0.25))
        self.axons.append(Axon(i2, h2, 0.30))

        Axon(s1, h1, 0.35)
        Axon(s1, h2, 0.35)

        self.axons.append(Axon(h1, o1, 0.40))
        self.axons.append(Axon(h2, o1, 0.45))
        self.axons.append(Axon(h1, o2, 0.50))
        self.axons.append(Axon(h2, o2, 0.55))

        Axon(s2, o1, 0.60)
        Axon(s2, o2, 0.60)



if __name__ == '__main__':
    import doctest
    z = ITest()
    #doctest.testmod()
