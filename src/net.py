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
        return self.oNeuron.net_derivative * self.weight

    def backprop(self, eta):
        delta_error = self.oNeuron.net_derivative * self.iNeuron.out
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
        return sum(axon.error for axon in self._oAxon) * self.out * (1 -
                self.out)

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
        return -(self.target - self.out) * self.out * (1 - self.out)

    @property
    def error(self):
        return (self.target - self.out) ** 2 / 2

import itertools
import numpy
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

    @property
    def neurons(self):
        return tuple(self._inputs + sum(self._hiddens, ()) + self._outputs)

    def back_pass(self):
        try:
            for neuron in self.neurons:
                neuron.back_pass(self.eta)
        finally:
            for neuron in self.neurons:
                neuron.lock()

    def train(self, epoch, dataset=None, verbose=True):
        if not dataset:
            dataset = self.dataset
        age = 0
        try:
            while age < epoch:
                datum = dataset[random.randint(0, len(dataset) - 1)]
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
            datum = dataset[random.randint(0, len(dataset) - 1)]
            self.inputs  = datum[0]
            self.outputs = datum[1]
            error += sum(output.error for output in self._outputs)
        return error / accuracy

class DFFNet(NNet):
    """
    Deep fried forward neural network
      >>> z = DFFNet(2, [2], 1)
    """
    def __init__(self, input_neurons, hidden_neurons, output_neurons, eta=1):
        super().__init__(eta)

        self._inputs  = tuple(      Input()  for _ in range(input_neurons))
        self._hiddens = tuple(tuple(Neuron() for _ in range(i)) for i in hidden_neurons)
        self._outputs = tuple(      Output() for _ in range(output_neurons))
        self._neurons  = (self._inputs,) + self._hiddens + (self._outputs,)
        for one, next in zip(self._neurons, self._neurons[1:]):
            for iNeuron, oNeuron in itertools.product(one, next):
                self.axons.append(Axon(iNeuron, oNeuron))

    @staticmethod
    def x_layers(outlayer, inlayer):
        for oNeuron in inlayer:
            for iNeuron in outlayer:
                oNeuron.f_connect(iNeuron)



class ITest(DFFNet):
    """
      >>> z = ITest()
      >>> print(z.inputs)
      [0.05, 0.1]
      >>> print([o.target for o in z._outputs])
      [0.01, 0.99]
      >>> print([a.weight for a in z.axons])
      [0.15, 0.2, 0.25, 0.3, 0.4, 0.45, 0.5, 0.55]
      >>> z.back_pass()
      >>> print([a.weight for a in z.axons])
      [0.1497807161327628, 0.19956143226552567, 0.24975114363236958, 0.29950228726473915, 0.35891647971788465, 0.4086661860762334, 0.5113012702387375, 0.5613701211079891]




    """
    def __init__(self):
        super().__init__(2, [2], 2, 0.5)

        self._inputs[0].input = 0.05
        self._inputs[1].input = 0.10

        self._hiddens = ((Neuron(), Neuron()),)

        self._outputs = (Output(), Output())
        self._outputs[0].target = 0.01
        self._outputs[1].target = 0.99

        self._neurons  = (self._inputs,) + self._hiddens + (self._outputs,)

        b1 = Static(1)
        i1, i2 = self._inputs
        h1, h2 = self._hiddens[0]
        o1, o2 = self._outputs


        self.axons = []
        self.axons.append(i1.f_connect(h1))
        self.axons[0].weight = 0.15
        self.axons.append(i2.f_connect(h1))
        self.axons[1].weight = 0.20
        self.axons.append(i1.f_connect(h2))
        self.axons[2].weight = 0.25
        self.axons.append(i2.f_connect(h2))
        self.axons[3].weight = 0.30

        b1.f_connect(h1, 0.35)
        b1.f_connect(h2, 0.35)

        self.axons.append(h1.f_connect(o1, 0.40))
        self.axons.append(h2.f_connect(o1, 0.45))
        self.axons.append(h1.f_connect(o2, 0.50))
        self.axons.append(h2.f_connect(o2, 0.55))

        b1.f_connect(o1, 0.60)
        b1.f_connect(o2, 0.60)



if __name__ == '__main__':
    import doctest
    z = ITest()
    doctest.testmod()
