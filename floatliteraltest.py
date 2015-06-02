import ast

from floatliteral import *

def test():
    print(type(1.2))
    def uses_float():
        return 1.2
    print(type(uses_float.__code__.co_consts[-1]))
    d = decimal.Decimal(1.2)
    print(repr(d))

