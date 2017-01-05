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

div = lambda a, b, c, d, e, f, g, h: [int(z) for z in list(format(int(int(str(round(a)) + str(round(b)) + str(round(c)) + str(round(d)), 2) / int(str(round(e)) + str(round(f)) + str(round(g)) + str(round(h)), 2)), '04b'))]

divfull = net.Net(0.1, 8, [6], 4)

divfull.function_train(div, 1e6)

def division(n, d):
    n = [int(num) for num in list(format(n, '04b'))]
    d = [int(num) for num in list(format(d, '04b'))]
    divfull.inputs = n + d
    o = int(''.join([str(round(num)) for num in divfull.outputs]), 2)
    return o

xnor = lambda a, b: int(a == b)
