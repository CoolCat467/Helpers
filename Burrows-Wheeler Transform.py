#!/usr/bin/env python3
# Burrows-Wheeler Transform
# -*- coding: utf-8 -*-

# Programmed by CoolCat467

from functools import wraps

__title__ = 'Burrows-Wheeler Transform'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

def transform(string, end='$'):
    """Return Burrows-Wheeler transform of string."""
    if end in string:
        raise EOFError('Multiple end characters exist!')
    string += end
    return ''.join((i[-1] for i in sorted((string[i:]+string[:i] for i in range(len(string))))))

def reverseTransform(string, end='$'):
    """Return inverse Burrows-Wheeler transform of string."""
    if not end in string:
        raise EOFError(f'End character {end} not found in string!')
    s = len(string)
    table = [''] * s
    for i in range(s):
        table = sorted(''.join(i) for i in zip(string, table))
    return [r for r in table if r.endswith(end)][0][:-1]

def compress(string):
    """Compress a string by replacing duplicated characters right next to eachother with the duplicated character plus count of repeats."""
    cchr = ''
    count = 0
    data = []
    def add_char(current, num):
        if current.isdigit():
            current = chr(ord(current)+128)
        if num <= 2:
            return current*num
        return f'{num}{current}'
    for char in string:
        if char == cchr:
            count += 1
        else:
            # Replace digits with different unicode characters.
            data.append(add_char(cchr, count))
            cchr = char
            count = 1
    data.append(add_char(cchr, count))
    return ''.join(data)

def decompress(string):
    """Decompress strings with duplicated characters next to eachother."""
    def isConvNum(char):
        uni = ord(char)
        return uni >= 176 and uni <= 185
    data = ''
    count = '1'
    lastDigit = False
    for char in string:
        if char.isdigit() and not isConvNum(char):
            if lastDigit:
                count += char
            else:
                count = char
        else:
            # Undo digit replace from compression
            if isConvNum(char):
                char = chr(ord(char)-128)
            # Add char * count to data
            data += char * int(count)
            count = '1'
        lastDigit = char.isdigit()
    return data

def transformer(func, end='$'):
    """Decorator that returns the Burrows-Wheeler transform of the output of a function."""
    @wraps(func)
    def transformer_wrapper(*args, **kwargs):
        """Transformer wrapper."""
        return transform(func(*args, **kwargs), end)
    return transformer_wrapper

def transformer_defend(end='$'):
    """Return transformer decorator with a custom EOF character."""
    @wraps(transformer)
    def transformer_defend_wrapper(func):
        return transformer(func, end)
    return transformer_defend_wrapper

def compresser(func):
    """Decorator that compresses the output of a transformed function."""
    @wraps(func)
    def compresser_wrapper(*args, **kwargs):
        """Compresser wrapper."""
        return compress(func(*args, **kwargs))
    return compresser_wrapper

def decompresser(func):
    """Decorator that decompresses the output of a compressed function."""
    @wraps(func)
    def decompresser_wrapper(*args, **kwargs):
        """Decompresser wrapper."""
        return decompress(func(*args, **kwargs))
    return decompresser_wrapper

def reverse_transformer(func, end='$'):
    """Decorator that returns the reverse Burrows-Wheeler transform of the output of a function."""
    @wraps(func)
    def reverse_transformer_wrapper(*args, **kwargs):
        """Reverse transformer wrapper."""
        return reverseTransform(func(*args, **kwargs), end)
    return reverse_transformer_wrapper

def reverse_transformer_defend(end='$'):
    """Return reverse transformer decorator with a custom EOF character."""
    @wraps(transformer)
    def reverse_transformer_defend_wrapper(func):
        return reverse_transformer(func, end)
    return reverse_transformer_defend_wrapper

### Examples of usage ###

def send_data_to_socket(string, socket, EOFchar='K'):
    @compresser
    @transformer_defend(EOFchar)
    def compress_data(string):
        return string
    compressed = compress_data(string)
    print(repr(compressed))
##    socket.send(compressed)

@reverse_transformer_defend('K')
@decompresser
def recieve_data_from_socket(socket, buffer_size=1024):
    return socket
##    return socket.recive(buffer_size)
