#!/usr/bin/env python3
# Program that Converts Numbers into Word Numbers and Vise-Versa
#
# Copywrite Cat Inc, All rights reserved.
# Programmed by Samuel Davenport, member of Cat Inc.
#
# DISCLAIMER:
# Additinal programs used in this program
# may contain code or code based off other code
# not owned by Cat Inc.

NAME = 'NumberProcessing'
__version__ = '0.0.0'

full = {'zero' : '0', 'one' : '1', 'two' : '2', 'three' : '3', 'four' : '4',
        'five' : '5', 'six' : '6', 'seven' : '7', 'eight' : '8',
        'nine' : '9', 'ten' : '10', 'eleven' : '11', 'twelve' : '12',
        'thirteen' : '13', 'fourteen' : '14', 'fifteen' : '15',
        'sixteen' : '16', 'seventeen' : '17', 'eighteen' : '18',
        'nineteen' : '19', 'twenty' : '20', 'thirty' : '30',
        'fourty' : '40', 'fifty' : '50', 'sixty' : '60',
        'seventy' : '70', 'eighty' : '80', 'ninety' : '90',
        'hundred' : '100', 'thousand' : '1000', 'million' : '1000000',
        'billion' : '1000000000', 'trillion' : '1000000000000'}

single = {'one' : '1', 'two' : '2', 'three' : '3', 'four' : '4',
          'five' : '5', 'six' : '6', 'seven' : '7', 'eight' : '8',
          'nine' : '9'}

def wordnum(data):
    #input is str
    cur = ['trillion']
    tmp = list(str(data).split(' '))
    cur.extend(tmp)
    places = ('trillion', 'billion', 'million', 'thousand')
    lastplace = len(cur)
    tmp = []
    for i in range(len(cur)):
        if cur[int(i)] in places or int(i) == (len(cur)-1):
            toapp = list(cur[lastplace:int(i)+1])
            tmp.append(toapp)
            lastplace = int(i)+1
    del tmp[0]
    cur = tmp
    places = []
    for lst in cur:
        dtmp = []
        i = 0
        while True:
            dtmp.append(int(full[lst[i]]))
            i += 1
            if i >= len(lst):
                break
        tmp = []
        for i in range(len(dtmp)):
            if dtmp[i] == 100:
                tmp.append(int(dtmp[i-1] * dtmp[i]))
                tmp.append(int('-'+str(dtmp[i-1])))
            else:
                tmp.append(int(dtmp[i]))
        dtmp = []
        nums = []
        for i in range(len(tmp)):
            if tmp[i] in (1000, 1000000, 1000000000, 1000000000000):
                num = 0
                for ii in nums:
                    num = num + int(ii)
                dtmp.append(int(num * tmp[i]))
            elif i == len(tmp)-1:
                num = 0
                for ii in nums:
                    num = num + int(ii)
                dtmp.append(int(num + tmp[i]))
            else:
                nums.append(int(tmp[i]))
        num = 0
        for newnum in dtmp:
            num = int(num + int(newnum))
        places.append(num)
    num = 0
    for place in places:
        num = num + int(place)
    return num

def numword(data):
    #input is int
    trillions = ['100000000000000', '1000000000000']
    billions  = ['100000000000',    '1000000000']
    millions  = ['100000000',       '1000000']
    thousands = ['100000',          '1000']
    hundreds  = ['100',             '1']
    allplaces = []
    allplaces.extend(trillions)
    allplaces.extend(billions)
    allplaces.extend(millions)
    allplaces.extend(thousands)
    allplaces.extend(hundreds)
    typelist = ('trillion', 'billion', 'million', 'thousand', '', '')
    read = ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9))
    cur = int(data)
    tmp = []
    lst = list(single.keys())#words list
    for i in range(5):
        for ii in range(2):
            if not cur == 0:
                dtmp = (cur / int(allplaces[read[i][ii]]))#divide and get float
                if int(dtmp) >= 1:#did divide into place?
                    lst = list(full.keys())#words list
                    if str(int(dtmp)) in list(full.values()):
                        idx = int(tuple(full.values()).index(str(int(dtmp))))#index pos
                        tmp.append(lst[idx])#remember tens and one pos
                    else:
                        pos = int(int(dtmp) - (int(dtmp) % 10))
                        if str(pos) in list(full.values()):
                            idx = int(tuple(full.values()).index(str(int(pos))))
                            pos = lst[idx]
                            if pos != 'zero':
                                tmp.append(pos)
                        
                        pos = int(int(dtmp) % 10)
                        if str(pos) in list(full.values()):
                            idx = int(tuple(full.values()).index(str(int(pos))))
                            pos = lst[idx]
                            if pos != 'zero':
                                tmp.append(pos)
                    if ii == 0:
                        tmp.append('hundred')
                    else:
                        tmp.append(typelist[i])
                    cur = int(cur - (int(allplaces[read[i][ii]])) * int(dtmp))#decrease num accordingly
    cur = tmp
    cur = []
    for i in tmp:#add spaces so it looks nice
        cur.append(i+' ')
    tmp = list(str(''.join(cur)))
    del tmp[len(tmp)-1]
    if (''.join(''.join(tmp).split('trillion billion million thousand hundred '))) in tuple(single.values()):
        tmp = ['error']
    tmp = list(str(''.join(tmp)))
    toret = str(''.join(tmp[0:len(tmp)-1]))
    return toret

def process(data):
    try:
        if not str(data).isalnum() and not str(data).isdigit():
            use = str(data)
            mode = 0
        elif str(data).isdigit():
            use = int(data)
            mode = 1
        else:
            mode = 2
        if mode in (0, 1):
            if bool(mode):
                toret = numword(use)
            else:
                toret = wordnum(use)
        else:
            toret = 'error'
    except BaseException:
        toret = 'error'
    return toret
