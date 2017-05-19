#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import svgwrite
from . import net

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

def c2percent(num):
    return '{}%'.format(num)

class Net(svgwrite.Drawing):
    def __init__(self, net, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.net = net
        self.coords = {}

    def drawLayer(self, xPos, n_layers, layer):
        n_neurons = len(layer)
        yspacing = 100 / (1 + n_neurons)
        xspacing = 100 / (1 + n_layers)
        xPos = (xPos + 1) * xspacing
        for i, neuron in enumerate(layer):
            yPos = (i + 1) * yspacing
            self.coords[neuron] = xPos, yPos


    def weaveAxons(self):
        for neuron, coord in self.coords.items():
            for axon in neuron._iAxon:
                try:
                    start = tuple(c2percent(c) for c in self.coords[axon.iNeuron])
                    end   = tuple(c2percent(c) for c in self.coords[axon.oNeuron])
                except KeyError:
                    continue
                self.add(self.line(start, end, stroke='blue', stroke_width=1))

    def drawNet(self):
        n_layers = len(self.net._neurons)
        for i, layer in enumerate(self.net._neurons):
            self.drawLayer(i, n_layers, layer)
        self.weaveAxons()
        for xPos, yPos in self.coords.values():
            self.add(self.circle((c2percent(xPos), c2percent(yPos)), 10))

#z = net.DFFNet(5, [10, 10], 4)
from . import test
z = test.ITest()
svg = Net(z)
svg.drawNet()
svg.save()
