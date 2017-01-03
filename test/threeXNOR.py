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


# doesnt like fractions of values, stick with 0s and 1s
# if two zeros, output 0, 1
# if two ones, output 1, 0
# if three zeros or ones, output 1, 1
pattern = [ [ [1, 1, 1], [1, 1] ], [ [1, 0, 1], [1, 0] ],
            [ [0, 1, 1], [1, 0] ], [ [0, 0, 1], [0, 1] ],

            [ [1, 1, 0], [1, 0] ], [ [1, 0, 0], [0, 1] ],
            [ [0, 1, 0], [0, 1] ], [ [0, 0, 0], [1, 1] ],
            ]


network = net.Net(0.1, 3, [20], 2)
inp = lambda: int(input('a binary value? : '))
try:
    network.mass_train(pattern, int(2e3))
except KeyboardInterrupt:
    print('impatient much?')

while True:
    network.inputs = [inp(), inp(), inp()]
    print(network.outputs)
