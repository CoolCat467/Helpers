#!/usr/bin/env python3
# Program that sorts lists with text using RadixLSD
#
# Copywrite Cat Inc, All rights reserved.
# Programmed by Samuel Davenport, member of Cat Inc.
#
# DISCLAIMER:
# Additinal programs used in this program
# may contain code or code based off other code
# not owned by Cat Inc.

# RadixLSD written by Mohit Kumra
from RadixLSD import *

def RadixText(data):
    global read
    #Sorts text with RadixLSD
    tosort = []
    for i in range(len(data)):
        tosort.append(maths.mkplain(data[i]))
    tmp = ['']
    for i in range(26):
        tmp.append(chr(i + 65).lower())
    tmp.append("'")
    for i in range(10):
        tmp.append(i)
    tmp.append('')
    read = tuple(tmp)
    for i in tosort:
        tmp = []
        for ii in str(i).lower():
            try:
                dtmp = str(read.index(ii))
            except ValueError:
                dtmp = str(len(read)-1)
            if int(len(list(dtmp))%2) != 0:
                dtmp = str('0' + dtmp)
            tmp.append(dtmp)
        tosort[tuple(tosort).index(i)] = int(''.join(tmp))
    sort = RadixLSD(tosort)
    for i in range(len(sort)):
        tmp = len(list(str(sort[i])))
        if bool(tmp % 2):
            sort[i] = str('0' + str(sort[i]))
        else:
            sort[i] = str(sort[i])
    for i in sort:
        tmp = []
        for ii in range(0, int(len(list(i))-1/2), 2):
            tmp.append(read[int(i[ii] + i[ii+1])])
        sort[tuple(sort).index(i)] = str(''.join(tmp))
    return sort
