#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Program that Converts Numbers into Word Numbers and Vise-Versa

# Programmed by CoolCat467

__title__ = 'numberProcessing'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

FULL = {'zero' : '0', 'one' : '1', 'two' : '2', 'three' : '3', 'four' : '4',
        'five' : '5', 'six' : '6', 'seven' : '7', 'eight' : '8',
        'nine' : '9', 'ten' : '10', 'eleven' : '11', 'twelve' : '12',
        'thirteen' : '13', 'fourteen' : '14', 'fifteen' : '15',
        'sixteen' : '16', 'seventeen' : '17', 'eighteen' : '18',
        'nineteen' : '19', 'twenty' : '20', 'thirty' : '30',
        'fourty' : '40', 'fifty' : '50', 'sixty' : '60',
        'seventy' : '70', 'eighty' : '80', 'ninety' : '90',
        'hundred' : '100', 'thousand' : '1000', 'million' : '1000000',
        'billion' : '1000000000', 'trillion' : '1000000000000'}

SINGLE = {'one' : '1', 'two' : '2', 'three' : '3', 'four' : '4',
          'five' : '5', 'six' : '6', 'seven' : '7', 'eight' : '8',
          'nine' : '9'}

PLACELAYERS = ('trillion', 'billion', 'million', 'thousand')

def text_to_number(data:str) -> int:
    """Return integer representation of a number as words."""
    cur = data.split(' ')
    # get places
    value = 0
    last = 0
    for idx, val in enumerate(cur):
        is_last = idx == len(cur)-1
        if is_last or val in PLACELAYERS:
            values = list(map(lambda x: int(FULL[x]), cur[last:idx+1]))
            if 100 in values:
                hidx = values.index(100)
                values[hidx-1] *= 100
                del values[hidx]
            if not is_last:
                value += sum(values[:-1])*int(FULL[val])
                last = idx+1
    return value + sum(values)

def split_by(value:int, divs:tuple, delzero:bool=False) -> dict:
    "Split value into sections defined by divs."
    value = int(value)
    def mod(val:int, num:int) -> tuple:
        "Return number of times val divides equally by num, then remainder."
        vmod = val % num
        return int((val - vmod) // num), vmod
    ret = {}
    for num in sorted(iter(set(divs)), reverse=True):
        remains, value = mod(value, num)
        if delzero and remains == 0:
            continue
        ret[num] = remains
    return ret

def number_to_text(data: int) -> str:
    """Convert number to string."""
    revfull = {int(v):k for k, v in FULL.items()}
    del revfull[0]
    revsing = {int(v):k for k, v in SINGLE.items()}
    # get parts of full
    split = split_by(data, tuple(revfull.keys()), True)
    text = ''
    # keep track of numbers left to represent
    left = data
    for k, val in split.items():
        left -= val*k
        # If data to represent in this chunk > 100
        if data-left > 100:
            # Get 100s, 10s, and 1s
            kval = split_by(val, (100, 10, 1), True)
            if 100 in kval:
                text += revsing[kval[100]]+' '+revfull[100]+' '
            if 10 in kval:
                text += revfull[kval[10]*10]+' '
            if 1 in kval and left > 10:
                parts = split_by(kval[1], revsing.keys(), True)
                text += ' '.join(revsing[pk] for pk in parts)+' '
        text += revfull[k]+' '
    return text[:-1]#no trailing space

##def number_to_text(data:int) -> str:
##    #input is int
##    trillions = ['100000000000000', '1000000000000']
##    billions  = ['100000000000',    '1000000000']
##    millions  = ['100000000',       '1000000']
##    thousands = ['100000',          '1000']
##    hundreds  = ['100',             '1']
##    allplaces = []
##    allplaces.extend(trillions)
##    allplaces.extend(billions)
##    allplaces.extend(millions)
##    allplaces.extend(thousands)
##    allplaces.extend(hundreds)
##    typelist = ('trillion', 'billion', 'million', 'thousand', '', '')
##    read = ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9))
##    cur = int(data)
##    tmp = []
##    lst = list(SINGLE.keys())#words list
##    for i in range(5):
##        for ii in range(2):
##            if not cur == 0:
##                dtmp = (cur / int(allplaces[read[i][ii]]))#divide and get float
##                if int(dtmp) >= 1:#did divide into place?
##                    lst = list(FULL.keys())#words list
##                    if str(int(dtmp)) in list(FULL.values()):
##                        idx = int(tuple(FULL.values()).index(str(int(dtmp))))#index pos
##                        tmp.append(lst[idx])#remember tens and one pos
##                    else:#if no representation
##                        pos = int(int(dtmp) - (int(dtmp) % 10))
##                        #get position for one less place value
##                        if str(pos) in list(FULL.values()):#
##                            idx = int(tuple(FULL.values()).index(str(int(pos))))
##                            pos = lst[idx]
##                            if pos != 'zero':
##                                tmp.append(pos)
##                        
##                        pos = int(int(dtmp) % 10)
##                        if str(pos) in list(FULL.values()):
##                            idx = int(tuple(FULL.values()).index(str(int(pos))))
##                            pos = lst[idx]
##                            if pos != 'zero':
##                                tmp.append(pos)
##                    if ii == 0:
##                        tmp.append('hundred')
##                    else:
##                        tmp.append(typelist[i])
##                    cur = int(cur - (int(allplaces[read[i][ii]])) * int(dtmp))
##                    #decrease num accordingly
##    cur = tmp
##    cur = []
##    for i in tmp:#add spaces so it looks nice
##        cur.append(i+' ')
##    tmp = list(str(''.join(cur)))
##    del tmp[len(tmp)-1]
# pylint: C0301: Line too long (111/100)
##    if (''.join(''.join(tmp).split('trillion billion million thousand hundred '))) in tuple(SINGLE.values()):
##        tmp = ['error']
##    tmp = list(str(''.join(tmp)))
##    toret = str(''.join(tmp[0:len(tmp)-1]))
##    return toret

def run():
    "Run example."
    valuetext = "five hundred seventy six trillion one hundred "\
                "twenty seven billion four hundred fifty eight "\
                "million seven hundred eighty four thousand three "\
                "hundred thirty two"
    print(valuetext)
    value = text_to_number(valuetext)
    print(value)
    vtext2 = number_to_text(value)
    print(vtext2)
    if valuetext == vtext2:
        print('True')
    else:
        print('False')

if __name__ == '__main__':
    run()
