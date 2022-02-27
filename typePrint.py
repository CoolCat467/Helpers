#!/usr/bin/env python3
# Typewriter Print. Prints stuff like a typewriter, one character at a time.
# -*- coding: utf-8 -*-

# Programmed by CoolCat467

__title__ = 'Typewriter Print'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import time, sys

REGULAR = sys.stdout
ERROR = sys.stderr

def typrint(iterable, totalTime=None, delay=0.1, regulate_delay=True, file=REGULAR) -> None:
    """Function that prints an iterable one position at a time with a delay betwen each character If totalTime is given, delay is ignored."""
    start = time.time()
    if totalTime:
        delay = totalTime/len(iterable)
    for char, index in zip(iter(iterable), range(len(iterable))):
        print(char, end='', file=file)
        if regulate_delay:
            time.sleep(max(0, (index * delay) - (time.time() - start)))
        else:
            time.sleep(delay)
    print('\n', end='', file=file)

def run():
    start = time.time()
    print()
    typrint('Cats are best!', 2, file=ERROR)
    typrint('Hellos to the future!\n'*5, 5)

if __name__ == '__main__':
    typrint(f'{__title__} v{__version__}\nProgrammed by {__author__}.', 2)
    run()
