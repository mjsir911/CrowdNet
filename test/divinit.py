#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
sys.path.insert(0, '../src')
import net
import test
import cortex

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

parser = argparse.ArgumentParser(description='Setup a neural network over a computer network')

parser.add_argument('file', metavar='FILE', type=str,
        default='divfull.net',
        help='File to save neural network')

parser.add_argument('-e', '--eta', metavar='ETA', type=float,
        default=0.3,
        help='Learning rate of network')

parser.add_argument('-b', '--base', metavar='BASE', type=int,
        default=8,
        help='Base at which neural network can process')

args = parser.parse_args()

base = args.base
eta = args.eta
f_name = args.file

@test.mad(base)
def division(n, d):
    return n // d

obj = net.Net(eta, base * 2, [int(base * 1.5)], base, func=division)
cortex.freeze(obj, f_name)
