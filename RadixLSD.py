#!/bin/env python3
# Python program for implementation of Radix Sort
# Programmed by Mohit Kumra from https://www.geeksforgeeks.org/radix-sort/
# Modified by Samuel Davenport

__version__ = '0.1.0'

def countingSort(sort, exp):
    # A function to do counting sort of sort[] according to
    # the digit represented by exp.
    # written by Mohit Kumra
    arr = list(sort)
    n = len(arr)
    output = [0] * (n)
    count = [0] * (10)
    for i in range(0, n):
        index = (arr[i]/exp)
        count[int((index)%10)] += 1
    
    for i in range(1,10):
        count[i] += count[i-1]
    
    i = n-1
    while i>=0:
        index = (arr[i]/exp)
        output[count[int((index)%10)] - 1] = arr[i]
        count[int((index)%10)] -= 1
        i -= 1
    
    i = 0
    for i in range(0,len(arr)):
        arr[i] = output[i]
    return arr

def RadixLSD(data):
    # Method to do Radix Sort
    # written by Mohit Kumra
    sort = data
    origmax = max(sort)
    exp = 1
    while origmax/exp > 0:
        sort = countingSort(sort,exp)
        exp *= 10
    return sort
