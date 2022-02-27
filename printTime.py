#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Print Time

# Programmed by CoolCat467

__title__ = 'Print Time'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0


def splitTime(seconds: int) -> list:
    "Split time into decades, years, months, weeks, days, hours, minutes, and seconds."
    seconds = int(seconds)
    def modTime(sec: int, num: int) -> tuple[int, int]:
        "Return number of times sec divides equally by number, then remainder."
        smod = sec % num
        return int((sec - smod) // num), smod
    ##values = (1, 60, 60, 24, 7, 365/12/7, 12, 10, 10, 10, 1000, 10, 10, 5)
    ##mults = {0:values[0]}
    ##for i in range(len(values)):
    ##    mults[i+1] = round(mults[i] * values[i])
    ##divs = list(reversed(mults.values()))[:-1]
    divs = (15768000000000000,
            3153600000000000,
            315360000000000,
            31536000000000,
            31536000000,
            3153600000,
            315360000,
            31536000,
            2628000,
            604800,
            86400,
            3600,
            60,
            1)
    ret = []
    for num in divs:
        t, seconds = modTime(seconds, num)
        ret.append(t)
    return ret

def combine_end(data: Iterable, final: str='and') -> str:
    "Join values of text, and have final with the last one properly."
    data = list(data)
    if len(data) >= 2:
        data[-1] = final+' ' + data[-1]
    if len(data) > 2:
        return ', '.join(data)
    return ' '.join(data)

def get_elapsed(seconds: int, singleTitleAllowed: bool=False) -> str:
    "Returns time using the output of splitTime."
    times = ('eons', 'eras', 'epochs', 'ages', 'millenniums',
             'centuries', 'decades', 'years', 'months', 'weeks',
             'days', 'hours', 'minutes', 'seconds')
    single = [i[:-1] for i in times]
    single[5] = 'century'
    split = splitTime(seconds)
    zipidxvalues = [(i, v) for i, v in enumerate(split) if v]
    if singleTitleAllowed:
        if len(zipidxvalues) == 1:
            index, value = zipidxvalues[0]
            if value == 1:
                return 'a '+single[index]
    data = []
    for index, value in zipidxvalues:
        title = single[index] if abs(value) < 2 else times[index]
        data.append(str(value)+' '+title)
    return combine_end(data)

def get_time_of_day(hour: int) -> str:
    "Figure out and return what time of day it is."
    if hour > 4 and hour < 12:
        return 'Morning'
    elif hour > 11 and hour < 19:
        # "It is usually from 12 PM to 6 PM,
        # but during winter it may be from 12 PM to 4 PM
        # and during summer it may be from 12 PM to 8 PM."
        return 'Afternoon'
    elif hour > 18 and hour < 22:
        return 'Evening'
    ##elif hour > 21 or hour < 4:
    return 'Night'


def run():
    pass





if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
