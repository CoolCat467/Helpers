#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Fast Fourier Transform

"Fast Fourier Transform"

# Programmed by CoolCat467

__title__ = 'Fast Fourier Transform'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

#https://www.youtube.com/watch?v=h7apO7q16V0

import cmath

def FFT(points):
    "Fast Fourier Transform"
    # P - [p0, p1, ..., pn-1] coeff rep
    n = len(points) # n is a power of 2
    if n == 1:
        return points
    w = cmath.exp(complex(2 * cmath.pi, 1) / n)
    
    p_even, p_odd = [], []
    for idx, val in enumerate(points):
        if idx % 2:
            p_odd.append(val)
        else:
            p_even.append(val)
    y_e, y_o = FFT(p_even), FFT(p_odd)
    
    y = [0]*n
    n_ot = n//2
    for j in range(n_ot):
        odd = w ** j * y_o[j]
        y[j] = y_e[j] + odd
        y[j + n_ot] = y_e[j] - odd
    return y

def IFFT(points):
    "Inverse Fast Fourier Transform"
    # P - [P(w**0), P(w**1), ..., P(w**(n-1))] value rep
    n = len(points) # n is a power of 2
    if n == 1:
        return points
    w = cmath.exp(complex(-2 * cmath.pi, 1) / n)
    
    p_even, p_odd = [], []
    for idx, val in enumerate(points):
        if idx % 2:
            p_odd.append(val)
        else:
            p_even.append(val)
    y_e, y_o = IFFT(p_even), IFFT(p_odd)
    
    y = [0]*n
    n_ot = n//2
    for j in range(n_ot):
        odd = w ** j * y_o[j]
        y[j] = y_e[j] + odd
        y[j + n_ot] = y_e[j] - odd
    return [v/n for v in y]

def run():
    pass





if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
