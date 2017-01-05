#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import dill as pickle
import daemon

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



def register(obj, f_name=None):
    if not f_name:
        f_name == obj.__name__
    atexit.register(freeze(obj, f_name))


def freeze(obj, f_name):
    pickle.Pickler(open(f_name, 'wb'), pickle.HIGHEST_PROTOCOL).dump(obj)

def melt(f_name):
    return pickle.loads(open(f_name, 'rb').read())
