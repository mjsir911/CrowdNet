#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import test
import time
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
    return math.log(x / (1 - x)) # this might break everything
    #return math.log(x / abs(1 - x)) # this might break everything

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
            self.terminals = [Dud(value)]
        except AttributeError:
            raise

    @property
    def net_derivative(self):
        net = 0
        for axon in self.axons:
            #net += axon.dendrite.net_derivative * axon.weight
            net += axon.dendrite.inverse * axon.weight
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
        new = _Axon(self, *args)
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
        self.new_weight = 2 * random.random() - 1
        self.dendrite = None

    def connect(self, dendrite):
        assert not self.dendrite
        self.dendrite = dendrite

    @property
    def value(self):
        #print(self.weight)
        #print(self.weight)
        return self.parent.value * self.weight

    #@test.multipro
    def backprop(self, eta):
        output_error_derivative = self.dendrite.net_derivative
        output_sig_der = self.dendrite.value * ( 1 - self.dendrite.value)
        weight_derivative = 1 * self.parent.value * self.weight ** (1 - 1) + 0 + 0
        delta_error = output_error_derivative * output_sig_der * weight_derivative
        self.new_weight = self.weight - eta * delta_error
        return self.new_weight

    def lock(self):
        self.weight = self.new_weight
        if type(self.weight) is not type(float()):
            #print(self.new_weight)
            pass

class Input(Neuron):
    def __init__(self, input=0.5):
        super().__init__([Dud(input)], lambda a: a)

class Dud():
    def __init__(self, value=0):
        self.value = unsig(value)
        #self.value = value
    def connect(self, nah):
        pass


class Net():
    def __init__(self, eta, input_neurons, hidden_neurons, output_neurons, is_discrete=False, func=None):
        chain = []
        self.sleep = 0
        self.func = func
        self.is_discrete=is_discrete
        self.eta = eta
        self._inputs = [Input() for x in range(input_neurons)]
        chain.append(self._inputs)

        for layer in range(len(hidden_neurons)):
            self.hiddens = [Neuron([neuron.Axon() for neuron in chain[layer]], lambda a, b: a + b) for x in range(hidden_neurons[layer])]
            chain.append(self.hiddens)
        if not hidden_neurons:
            self.hiddens = []


        self._outputs = [
                Neuron([neuron.Axon() for neuron in chain[-1]], lambda a, b: a + b)
                for x in range(output_neurons)
                ]

        chain.append(self._outputs)
        #print(chain)

        self.t_neurons = self.hiddens + self._outputs
        self.neurons = self._inputs + self.t_neurons
        self._axons = [axon for neuron in self.neurons for axon in neuron.axons]

        self.a_queue = [False] * len(self._axons)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return False
        if self.inputs != other.inputs:
            return False
        if self.outputs != other.outputs:
            return False
        if self.axons != other.axons:
            return False

        return True

    @property
    def inputs(self):
        return [neuron.value for neuron in self._inputs]

    @inputs.setter
    def inputs(self, values):
        values = self.make_iter(values)
        assert len(values) == len(self._inputs), 'not correct amount of inputs, provided {} inputs, need {} inputs'.format(len(values), len(self._inputs))
        values = iter(values)
        for neuron in self._inputs:
            #neuron.value = abs(1e-15 - next(values))
            if not self.is_discrete:
                neuron.value = self.extreme(next(values))
            else:
                neuron.value =  self.unint(next(values))
        time.sleep(self.sleep / 100)

    @property
    def outputs(self):
        return [neuron.value for neuron in self._outputs]

    @property
    def axons(self):
        return [axon.weight for axon in self._axons]

    @axons.setter
    def axons(self, data):
        self.a_queue = test.truey([data] + [self.a_queue])
        if all(self.a_queue):
            #print('full of trueys')
            #print('locking in data')
            for weight, axon in zip(self.a_queue, self._axons):
                axon.weight = weight
            self.a_queue = [False] * len(self._axons)

    def train(self, dataset, repeat=(0, 1)):
        """ [[inputs], [outputs]] """
        self.inputs = dataset[0]
        self.ideal  = dataset[1]
        ideal = iter(dataset[1])

        for output in self._outputs:
            output.target = next(ideal)

        """
        if not axon_range:
            axon_range = (0, len(self._axons))
        """

        # here i want p2p
        data = [False] * len(self._axons)
        for index, axon in zip(range(repeat[0], len(self._axons), repeat[1]), self._axons[repeat[0]::repeat[1]]):
                data[index] = axon.backprop(self.eta)
        return data

    def mass_train(self, dataset, epoch):
        try:
            for age in range(int(epoch)):
                datum = dataset[random.randint(0, len(dataset) - 1)]
                print('epoch is :', age, end="\r", flush=True)
                self.axons = self.train(datum)
            print()
        except KeyboardInterrupt:
            print()
            print('wow rude')

    @test.timeme
    def function_train(self, epoch, func=None):
        if func:
            if self.func:
                self.func = func
            else:
                print('set a function')
                assert False
                raise
        else:
            func = self.func
        self.func = func
        #argcount = func.__code__.co_argcount
        argcount = len(self.inputs) # bad practs
        #assert argcount == len(self.inputs), 'need different amount of inputs'
        try:
            for age in range(int(epoch)):
                v_inputs  = [self.random() for x in range(argcount)]
                print('epoch is :', age, end="\r", flush=True)
                try:
                    v_outputs = func(*v_inputs)
                except Exception as e:
                    print(e)
                    continue
                v_outputs = self.make_iter(v_outputs)
                #print('input = {}, output = {}'.format(v_inputs, v_outputs))
                many = 1
                for offset in range(0, many):
                    self.axons = self.train([v_inputs, v_outputs], (offset, many))
            print('training complete')
        except KeyboardInterrupt:
            print()
            print('wow rude')

    def error(self, accuracy, func=None, dataset=None, exact=True):
        if dataset:
            pass
        elif func:
            pass
        else:
            func = self.func
        accuracy_repeat = unsig((accuracy) / 2 + 0.5) * 1e3
        ate = []
        for x in range(int(accuracy_repeat)):
            if func:
                self.inputs  = [self.random() for x in range(len(self._inputs))]
                try:
                    should = [self.extreme(num) for num in self.make_iter(func(*self.inputs))]
                except:
                    continue
                actual = self.outputs
            elif dataset:
                datum = dataset[random.randint(0, len(dataset) - 1)]
                self.inputs = datum[0]
                should = datum[1]
                actual = self.outputs


            #print(actual)
            #print(should)
            assert len(actual) == len(should), 'len is {} when should be {}'.format(len(actual), len(should))
            v = []
            # should i average the error of all the inputs or get the error of the combined inputs
            #a = int(''.cjoin(str(round(n)) for n in actual), 2)
            #s = int(''.join(str(round(n)) for n in should), 2)
            if exact:
                a = [self.extreme(num) for num in actual]
                s = [self.extreme(num) for num in should]
                if a == s:
                    ate.append(1)
                else:
                    ate.append(0)
            else:
                for a, s in zip(actual, should):
                    v.append(abs(a - s) / a)
                    v.append(abs(a - s))

                ate.append(sum(v) / len(v))

        return(sum(ate)/len(ate))

    @classmethod
    def make_iter(cls, obj):
        try:
            iter(obj)
        except TypeError:
            obj = [obj]

        return obj

    @classmethod
    def extreme(cls, value):
        return cls.unint(round(value))
        #return value

    @classmethod
    def unint(cls, value):
        return abs(1e-15 - value)

    def random(self):
        if self.is_discrete:
            return random.random()
        else:
            return round(random.random())


# Some patterns

# doesnt like fractions of values, stick with 0s and 1s
# if two zeros, output 0, 1
# if two ones, output 1, 0
# if three zeros or ones, output 1, 1
t   = [ [ [1, 1, 1], [1, 1] ], [ [1, 0, 1], [1, 0] ],
        [ [0, 1, 1], [1, 0] ], [ [0, 0, 1], [0, 1] ],
      ]

t  += [ [ [1, 1, 0], [1, 0] ], [ [1, 0, 0], [0, 1] ],
        [ [0, 1, 0], [0, 1] ], [ [0, 0, 0], [1, 1] ],
      ]
