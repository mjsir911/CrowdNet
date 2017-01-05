#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../src')
import net
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

base = 4

def mad(func):
    def wrapper(*args, **kwargs):
        first = int(''.join(str(round(n)) for n in args[:base]), 2)
        last = int(''.join(str(round(n)) for n in args[base:]), 2)
        input_bin = [int(z) for z in list(format(func(first, last), '0{}b'.format(base)))]
        return input_bin
    return wrapper

add = mad(lambda a, b: a + b)
sub = mad(lambda f, l: f - l)
mul = mad(lambda a, b: a * b)
div = mad(lambda d, n: d // n)

simple = 0
inverse = 1
add_op = (0, 0)
sub_op = (0, 1)
mul_op = (1, 0)
div_op = (1, 1)

"""
def math(*args):
    op = args[:2]
    args = args[2:]
    if op[1] == simple:
        if op[1] != inverse:

    else:
        if op[1] != inverse:
            """


divfull = cortex.melt('dills/division')
print('accuracy currently at', str(int(divfull.error(0.9) * 100)), '%')
print('do functions.division(n, d) to try out division!')

#divfull.function_train(div, 1e6)

def division(n, d):
    n = [int(num) for num in list(format(n, '0{}b'.format(base)))]
    d = [int(num) for num in list(format(d, '0{}b'.format(base)))]
    divfull.inputs = n + d
    o = int(''.join([str(round(num)) for num in divfull.outputs]), 2)
    return o

xnor = lambda a, b: int(a == b)

def main():
    while True:
        numerator   = int(input('numerator: '))
        denominator = int(input('denomerator: '))
        ans = division(numerator, denominator)
        print(ans)
        if ans != numerator // denominator:
            print('actual answer is: ', numerator // denominator)

if __name__ == '__main__':
    main()
