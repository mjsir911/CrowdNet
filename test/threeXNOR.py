#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../src')
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

network = net.Net(1, 3, [10], 2)
inp = lambda: int(input('a binary value? : '))
try:
    network.mass_train(net.t, int(2e3))
except KeyboardInterrupt:
    print('impatient much?')
network.inputs = [inp(), inp(), inp()]
print(network.outputs)
