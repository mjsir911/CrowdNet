#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import math

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

def sig(x):
    return 1 / (1 + math.e ** -x)

def unsig(x):
    return math.log(x / (1 - x))

def error(ideal, actual):
    return (1/2) * (ideal - actual) ** 2

def node_delta(ideal, actual):
    return -(ideal - actual) * actual * (1 - actual)
    #return -(ideal - actual) * actual * (1 - out)

class Neuron():
    def __init__(self, inputs, operation):
        self.terminals = inputs
        for axon in self.terminals:
            axon.connect(self)
        self.operation = operation
        self.axons = []
        self.target = None
        self.bias = 0

    @property
    def value(self):
        terminals = (input.value for input in self.terminals)
        x = next(terminals)
        while True:
            try:
                x = self.operation(x, next(terminals))
            except StopIteration:
                break
        return sig(x)

    @value.setter
    def value(self, value):
        try:
            self.terminals = [self.Dud(value)]
        except AttributeError:
            raise

    @property
    def net_derivative(self):
        net = 0
        for axon in self.axons:
            #net += axon.connection.net_derivative * axon.weight
            net += axon.connection.inverse * axon.weight
        if not self.axons:
        #if not net: # does same thing
            #net = -(self.target - self.value) * self.value * (1 - self.value)
            #net = -(self.target - self.value) * self.value * (1 - self.value)

            #print('net : ', net)
            # gotta make this happen
            net = -(self.target - self.value)
        return net

    @property
    def inverse(self):
        return self.net_derivative * self.value * (1 - self.value)
        # doesnt work
        #pass


    def Axon(self, *args):
        new = self._Axon(self, *args)
        self.axons.append(new)
        return new

    class _Axon():
        def __init__(self, parent, weight=0):
            if weight:
                self.weight = weight
                #print('setting weight to {}'.format(weight))
            else:
                #print('setting random weight')
                self.weight = 2 * random.random() - 1
            self.parent = parent
            self.new_weight = None
            self.connection = None

        def connect(self, connection):
            assert not self.connection
            self.connection = connection

        @property
        def value(self):
            return self.parent.value * self.weight

        def backprop(self, alpha):
            #output_error_derivative = -(self.connection.target - self.connection.value)
            output_error_derivative = self.connection.net_derivative
            #print('a : ', output_error_derivative)
            output_sig_der = self.connection.value * ( 1 - self.connection.value)
            #print('b : ', output_sig_der)
            weight_derivative = 1 * self.parent.value * self.weight ** (1 - 1) + 0 + 0
            #print('c : ', weight_derivative)
            delta_error = output_error_derivative * output_sig_der * weight_derivative
            #delta_error = self.connection.net_derivative * output_sig_der * weight_derivative
            #print(delta_error)
            self.new_weight = self.weight - alpha * delta_error

        def lock(self):
            self.weight = self.new_weight

class Input(Neuron):
    def __init__(self, input=0.5):
        super().__init__([self.Dud(input)], lambda a: a)

    class Dud():
        def __init__(self, value=0):
            self.value = unsig(value)
        def connect(self, nah):
            pass


class Net():
    def __init__(self, alpha=0.5, hidden_neurons=[1]):
        self.alpha = alpha
        self._inputs = [Input() for x in range(5)]

        self.hiddens = [Neuron([self._inputs[0].Axon(), self._inputs[1].Axon(0.3)], lambda a, b: a + b) for x in range(1)]

        self._outputs = [
                Neuron([neuron.Axon() for neuron in self.hiddens], lambda a, b: a + b),
                #Neuron([self.hiddens[0].Axon(0.5), self.hiddens[1].Axon(0.55), constant2.Axon(1)], lambda a, b: a + b),
                ]

        self.neurons = self.hiddens + self._outputs


    def train(self, dataset):
        """ [[inputs], [outputs]] """
        self.inputs = dataset[0]
        self.ideal  = dataset[1]
        ideal = iter(dataset[1])

        for output in self._outputs:
            output.target = next(ideal)
        for neuron in self.neurons:
        #for neuron in self._outputs:
            for axon in neuron.terminals:
                axon.backprop(self.alpha)

        [[axon.lock() for axon in neuron.terminals] for neuron in self.neurons] # no lock for now

    def mass_train(self, dataset, epoch):
        for age in range(int(epoch)):
            for datum in dataset:
                self.train(datum)
            print('epoch is: ', age)

    @property
    def inputs(self):
        return [neuron.value for neuron in self._inputs]

    @inputs.setter
    def inputs(self, values):
        values = iter(values)
        for neuron in self._inputs:
            neuron.value = abs(1e-15 - next(values))

    @property
    def outputs(self):
        return [neuron.value for neuron in self._outputs]
