#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import abc

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

class Axon():
    def __init__(self,  iNeuron, oNeuron, weight=None):
        self.iNeuron = iNeuron
        self.oNeuron = oNeuron
        self.bind()
        if weight:
            self.weight = weight
        else:
            self.weight = random.random()

    @property
    def value(self):
        return self.weight * self.iNeuron.out

    @property
    def error(self):
        return self.oNeuron.derivative * self.weight

    def backprop(self, eta):
        delta_error = self.oNeuron.derivative * self.iNeuron.out
        self.new_weight = self.weight - eta * delta_error
        return self.new_weight

    def lock(self):
        self.weight = self.new_weight
        self.oNeuron._done = False
        self.iNeuron._done = False

    def unbind(self):
        self.iNeuron._oAxon.remove(self)
        self.oNeuron._iAxon.remove(self)
    def bind(self):
        self.iNeuron._oAxon.append(self)
        self.oNeuron._iAxon.append(self)

import math
class Neuron():
    def __init__(self, operator=sum):
        self.op = operator
        self._iAxon = []
        self._oAxon = []
        self._done = False

    @pLock
    def net(self):
        return self.op(i.value for i in self._iAxon)

    @pLock
    def out(self):
        return 1 / (1 + math.exp(-self.net))

    @pLock
    def net_derivative(self):
        return sum(axon.error for axon in self._oAxon)

    @pLock
    def partial_derivative(self):
        return self.out * (1 - self.out)

    @pLock
    def derivative(self):
        return self.partial_derivative * self.net_derivative

    def f_connect(self, other, weight=None):
        return Axon(self, other, weight)

    def back_pass(self, eta=0.5):
        for a in self._oAxon:
            a.backprop(eta)

    def lock(self):
        for a in self._oAxon:
            a.lock()


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


    @property
    def error(self):
        return 0.5 * (self.target - self.out) ** 2

import itertools
import numpy
class NNet(metaclass=abc.ABCMeta):
    def __init__(self, eta=0, dataset=None):
        self.eta = eta
        self.dataset = dataset
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

    @property
    def neurons(self):
        return [self._inputs + sum(self._hiddens, []) + self._outputs]

    def back_pass(self):
        try:
            for axon in self.axons:
                axon.backprop(self.eta)
        finally:
            for axon in self.axons:
                axon.lock()

    def train(self, epoch, dataset=None, verbose=True):
        if not dataset:
            dataset = self.dataset
        age = 0
        try:
            while age < epoch:
                datum = tuple(dataset.items())[
                        random.randint(0, len(dataset) - 1)]
                self.inputs  = datum[0]
                self.outputs = datum[1]
                self.back_pass()
                age += 1
                if verbose:
                    print('epoch is {}'.format(age), end='\r')
        except KeyboardInterrupt:
            self.back_pass()
        finally:
            if verbose:
                print()

    def error(self, accuracy, dataset=None):
        if not dataset:
            dataset = self.dataset
        error = 0
        for _ in range(accuracy):
            #self.train(1, dataset, False)
            datum = tuple(dataset.items())[
                    random.randint(0, len(dataset) - 1)]
            self.inputs  = datum[0]
            self.outputs = datum[1]
            error += sum(output.error for output in self._outputs)
        return error / accuracy

class DFFNet(NNet):
    """
    Deep fried forward neural network
      >>> z = DFFNet(2, [2], 1)
    """
    def __init__(self, input_neurons, hidden_neurons, output_neurons, eta=1,
            dataset=None):
        super().__init__(eta, dataset=dataset)

        self._inputs  = [      Input()  for _ in range(input_neurons)]
        self._hiddens = [[Neuron() for _ in range(i)] for i in hidden_neurons]
        self._outputs = [      Output() for _ in range(output_neurons)]
        self._neurons  = [self._inputs] + self._hiddens + [self._outputs]
        self.weave()

    def weave(self):
        for one, next in zip(self._neurons, self._neurons[1:]):
            for iNeuron, oNeuron in itertools.product(one, next):
                self.axons.append(Axon(iNeuron, oNeuron))

    @staticmethod
    def x_layers(outlayer, inlayer):
        for oNeuron in inlayer:
            for iNeuron in outlayer:
                oNeuron.f_connect(iNeuron)






if __name__ == '__main__':
    import doctest
    doctest.testmod()
