#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Figure out the order functions should be in so
# that chaining inputs and outputs and given a starting
# input and final output, we can know the correct order.

# Programmed by CoolCat467

__title__ = 'Function machine chain solver'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import math
import itertools
from typing import Union
from functools import cache, lru_cache

import sys
info = sys.version_info
if info.major < 3:
    raise RuntimeError('Must be at least Python 3!')
if info.minor < 9:
    raise RuntimeError('Must be at least Python 3.9!')
del info, sys

class func:
    "Function object. Needs name and function object"
    def __init__(self, name:str, function) -> None:
        "Remember name and function to use."
        self.name = name
        self.func = function
        return
    
    def __repr__(self) -> str:
        return f'Function "{self.name}"'
    
    @lru_cache()
    def get(self, x):
        "Return result of function with input x."
        # Use lru cache decorator for preformance help.
        # one of the only good times to use it now that I think about it.
        return self.func(x)
    pass

def find_function_order(functions:tuple, start:float, end:float) -> Union[tuple, None]:
    """Return either a list of the order functions should be used in to get end
    from start chained in order, or None because it's not possible."""
    # Ensure start and end are floats. Breaks from division if not, as 0 != 0.0
    start = float(start)
    end = float(end)
    # Get dictionary of functions, with their names as keys.
    fdict = {f.name:f for f in functions}
    def solve_single(totry:list[str], inp:float) -> Union[float, None]:
        """MODIFIES "totry" IN PLACE!!!
        Try totry backwords with inp as last function's input.
        Returns either result float or None because of errors."""
        # Get name of function to try next by pop
        fname = totry.pop()
        # Try to get result from function(input)
        try:
            res = fdict[fname].get(inp)
        except:
            # If it fails, return None.
            #ValueError or ZeroDivisionError or OverflowError
            return None
        # Otherwise,
        if not totry:
            # If none left to try, return final result.
            return res
        # Return result of next one on.
        # solved by recursion.
        return solve_single(totry, res)
    # Get all possible orders of chaining functions
    options = set(itertools.permutations(fdict.keys()))
    # For each possible order,
    for option in options:
        # Figure out final result after chaining
        # output of last to input of next
        # Very important, makes list object copy of it
        # because it changes it in place.
        o = solve_single(list(option), start)
        # If it errored out in some way or another, keep going.
        if o is None:
            continue
        # Otherwise, if it's the same as what we're looking for,
        if o == end:
            # Return function order reversed because
            # solve single reads things backwards.
            return tuple(reversed(option))
    return

class solver:
    "Solver object."
    def __init__(self):
        self.funcs = {}
        return
    
    def __repr__(self):
        return "<Function Solver>"
    
    def add_func(self, func):
        "Add function to solver."
        self.funcs[func.name] = func
        return
    
    def solve(self, start_input:float, final_output:float) -> Union[tuple, None]:
        # Ensure start and end are floats. Breaks from division if not, as 0 != 0.0
        start = float(start_input)
        end = float(final_output)
        # Get dictionary of functions, with their names as keys.
        def solve_single(totry:list[str], inp:float) -> Union[float, None]:
            """MODIFIES "totry" IN PLACE!!!
            Try totry backwords with inp as last function's input.
            Returns either result float or None because of errors."""
            # Get name of function to try next by pop
            fname = totry.pop()
            # Try to get result from function(input)
            try:
                res = self.funcs[fname].get(inp)
            except:
                # If it fails, return None.
                #ValueError or ZeroDivisionError or OverflowError
                return None
            # Otherwise,
            if not totry:
                # If none left to try, return final result.
                return res
            # Return result of next one on.
            # solved by recursion.
            return solve_single(totry, res)
        # Get all possible orders of chaining functions
        options = set(itertools.permutations(self.funcs.keys()))
        # For each possible order,
        for option in options:
            # Figure out final result after chaining
            # output of last to input of next
            # Very important, makes list object copy of it
            # because it changes it in place.
            o = solve_single(list(option), start)
            # If it errored out in some way or another, keep going.
            if o is None:
                continue
            # Otherwise, if it's the same as what we're looking for,
            if o == end:
                # Return function order reversed because
                # solve single reads things backwards.
                return tuple(reversed(option))
        return None
    
    @cache
    def get_func(self) -> func:
        "Get function class to use."
        class function(func):
            def __init__(salf, *args, **kwargs):
                super().__init__(*args, **kwargs)
                salf.solver = self
                self.add_func(salf)
                return
            def __repr__(salf):
                rep = super().__repr__()
                return f'<{str(self)}-wrapped {rep}>'
            pass
        return function
    pass

def run():
    print()
    # Mr cat solves function chains for us! Much waw!
    mrcat = solver()
    fu = mrcat.get_func()
    # Define functions here.
    u = fu('u', lambda x: x - x ** 2)
    v = fu('v', lambda x: -(x**3) + x)
    w = fu('w', lambda x: math.sqrt(3 + 2 * x))
    y = fu('y', lambda x: 36 / (x - 1))
    z = fu('z', lambda x: 2 ** (-x) - 4)
##    f = fu('f', lambda x: math.sqrt(x + 3))
##    g = fu('g', lambda x: -((x-2)/3))
##    h = fu('h', lambda x: 3 ** (x-4) + 1)
##    k = fu('k', lambda x: 2 * abs(x + 4) - 3)
    s, e = 73, -3540
    result = mrcat.solve(s, e)
    print(result)
    return

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
