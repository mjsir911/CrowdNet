#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

gates = {
        'not': {
            (0,): (1,),
            (1,): (0,),
            },
        'and': {
            (0, 0): (0,),
            (0, 1): (0,),
            (1, 0): (0,),
            (1, 1): (1,),
            },
        'or': {
            (0, 0): (0,),
            (0, 1): (1,),
            (1, 0): (1,),
            (1, 1): (1,),
            },
        'xor': {
            (0, 0): (0,),
            (0, 1): (1,),
            (1, 0): (1,),
            (1, 1): (0,),
            },
        'nand': {
            (0, 0): (1,),
            (0, 1): (1,),
            (1, 0): (1,),
            (1, 1): (0,),
            },
        'nor': {
            (0, 0): (1,),
            (0, 1): (0,),
            (1, 0): (0,),
            (1, 1): (0,),
            },
        'xnor': {
            (0, 0): (1,),
            (0, 1): (0,),
            (1, 0): (0,),
            (1, 1): (1,),
            },
        }



xnorNN = net.DFFNet(2, [5], 1)
xnorNN.dataset = gates['xnor']
