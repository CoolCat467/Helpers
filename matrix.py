#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Matrix Module

"Matrix module"

# Programmed by CoolCat467

__title__ = 'Matrix'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__mer_major__ = 0
__mer_minor__ = 0
__mer_patch__ = 0

import math
from typing import Any, Iterable, Union, Callable
from functools import wraps, reduce

from vector import Vector4

def mmathop(function):
    "Matrix math operator decorator"
    @wraps(function)
    def wrapped_op(self, rhs, *args, **kwargs):
        if hasattr(rhs, '__len__'):
            if len(rhs) == len(self):
                return function(self, rhs, *args, **kwargs)
            raise TypeError('Operand length is not same as own')
        return function(self, [rhs]*len(self), *args, **kwargs)
##        raise AttributeError('Operand has no length attribute')
    return wrapped_op

def mapop(function: Callable) -> Callable:
    "Return new `self` class instance built from application of function on items of self."
    @wraps(function)
    def operator(self):
        return self.__class__(map(function, iter(self)), shape=self.shape)
    return operator

def simpleop(function):
    "Return new `self` class instance built from application of function on items of self and rhs."
    def apply(values):
        return function(*values)
    @wraps(function)
    def operator(self, rhs):
        return self.__class__(map(apply, zip(self, rhs)), shape=self.shape)
    return operator

def onlysquare(function):
    "Return wrapper that only runs function if matrix is square."
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if len(set(self.shape)) == 1:
            return function(self, *args, **kwargs)
        raise TypeError('Matrix is not a square matrix!')
    return wrapper

def combine_end(data: Iterable, final: str='and') -> str:
    "Join values of text, and have final with the last one properly."
    data = list(data)
    if len(data) >= 2:
        data[-1] = final+' ' + data[-1]
    if len(data) > 2:
        return ', '.join(data)
    return ' '.join(data)

def onlytype(*types, names: str=None) -> Callable:
    "Return wrapper that only runs function if all items are instances of types."
    if names is None:
        names = combine_end((t.__name__+'s' for t in types), 'or')
    def wrapper(function) -> Callable:
        @wraps(function)
        def wrapped_func(self: Iterable, *args, **kwargs) -> Any:
            for value in iter(self):
                if not isinstance(value, types):
                    raise TypeError(f'Matrix is not composed entirely of {names}')
            return function(self, *args, **kwargs)
        return wrapped_func
    return wrapper

def onlytypemath(*types, name: str=None) -> Callable:
    "Return wrapper that only runs function if all items are instances of types."
    if name is None:
        name = combine_end((t.__name__+'s' for t in types), 'or')
    def wrapper(function) -> Callable:
        @wraps(function)
        def wrapped_func(self: Iterable, rhs: Iterable, *args, **kwargs) -> Any:
            for value in iter(self):
                if not isinstance(value, types):
                    raise TypeError(f'Matrix is not composed entirely of {name}')
            for value in iter(rhs):
                if not isinstance(value, types):
                    raise TypeError(f'Operand is not composed entirely of {name}')
            return function(self, rhs, *args, **kwargs)
        return wrapped_func
    return wrapper

def boolop(combine: str='all') -> Callable:
    "Return matrix boolian simple operator. Combine can by ('any', 'all')"
    if not combine in {'any', 'all'}:
        raise ValueError("Combine must be either 'any' or 'all'!")
    def wrapper(function) -> Callable[[Iterable, Iterable], bool]:
        "Matrix boolian operator decorator"
        def apply(values: Iterable) -> bool:
            return function(*values)
        if combine == 'any':
            def operator(self, rhs) -> bool:
                return any(map(apply, zip(self, rhs)))
        else:
            def operator(self, rhs) -> bool:
                return all(map(apply, zip(self, rhs)))
        return wraps(function)(operator)
    return wrapper

multiply = lambda x,y:x*y

class Matrix:
    "Matrix Class"
    __slots__ = ('__m','__shape')
    def __init__(self, data, shape: tuple, dtype: type=tuple):
        self.__shape = shape
        items = reduce(multiply, self.__shape)
        data = list(data)
        if len(data) != items:
            data = sum(data, [])
        if len(data) != items:
            size = 'x'.join(map(str, self.shape))
            raise ValueError(f'Unequal number of elements for {size} matrix!')
        self.__m = dtype(data)
    
    def __repr__(self) -> str:
        elem = [len(s) for s in map(str, self.elements)]
        leng = min(8, math.ceil(sum(elem)/len(elem)))
        elem = [len(str(round(e, leng))) for e in self.elements]
        leng = min(8, math.ceil(sum(elem)/len(elem)))
        rows = ['  ['+', '.join(str(round(r, leng))[:leng].rjust(leng) for r in row)+']' for row in self.rows()]
        args = '[\n'+',\n'.join(rows)+'\n]'+', '+str(self.shape)
        return f'{self.__class__.__name__}({args})'
    
    @property
    def shape(self) -> tuple:
        "Shape of this Matrix"
        return self.__shape
    
    @property
    def elements(self):
        "Unwrapped elements of this matrix"
        return self.__m
    
    @property
    def T(self) -> 'Matrix':# pylint: disable=invalid-name
        "Transpose of this matrix"
        return self.transpose()
    
    def rows(self):
        "Return rows of this matrix"
        rows = []
        for ridx in range(self.shape[0]):
            rows.append(self.elements[ridx*self.shape[1]:(ridx+1)*self.shape[1]])
        return rows
    
    def __len__(self):
        return len(self.__m)
    
    def __iter__(self):
        return iter(self.__m)
    
    def __get_active_indices(self, index) -> Union[int, list[int]]:
        "Return either list of indices or single indice to act apon for given index."
        data = list(range(len(self)))
        shape = list(self.shape)
        all_reg = True
        last_dim = 1
        for part in index:
##            print(part)
            next_dim = shape.pop()
            slicelen = reduce(multiply, shape, 1)
            if not isinstance(part, slice):
##                print(f'{part=}')
                if all_reg:
                    part = slice(part*slicelen, (part+1)*slicelen)
                elif self.shape[1] == 1:
                    part = slice(None, None, last_dim)
                else:
                    part = slice(part, None, last_dim)
                
##                print(f'new {part=}\n')
            else:
                all_reg = False
                start, stop, step = part.indices(len(self))
                part = slice(start*next_dim, stop*next_dim, step)
            data = data[part]
            last_dim *= next_dim
        if not data:
##            print(self)
##            print(f'2 {index=}')
            raise IndexError('Invalid index for matrix!')
        if all_reg:
            return data[0]
        return data
    
    def __getitem__(self, index) -> Union[list, Union[int, float]]:
        # (row, column)
        if not isinstance(index, tuple) or len(index) < len(self.__shape):
            size = 'x'.join(map(str, self.shape))
            raise IndexError(f'Not enough arguments for {size} matrix.')
        if len(index) > len(self.__shape):
            size = 'x'.join(map(str, self.shape))
            raise IndexError(f'Too many arguments for {size} matrix.')
        index = self.__get_active_indices(index)
        if isinstance(index, int):
            return self.__m[index]
        return [self.__m[idx] for idx in index]
    
    def __setitem__(self, index, value) -> None:
        if not isinstance(index, tuple) or len(index) < len(self.__shape):
            size = 'x'.join(map(str, self.shape))
            raise IndexError(f'Not enough arguments for {size} matrix.')
        if len(index) > len(self.__shape):
            size = 'x'.join(map(str, self.shape))
            raise IndexError(f'Too many arguments for {size} matrix.')
        positions = self.__get_active_indices(index)
        if isinstance(positions, int):
            self.__m[positions] = value
            return
        if not hasattr(value, '__len__'):
            for idx in positions:
                self.__m[idx] = value
        elif hasattr(value, '__iter__'):
            values: Iterable = iter(value)
            for idx, val in zip(positions, values):
                self.__m[idx] = val
    
    @classmethod
    def from_iter(cls, iterable: Iterable, shape: tuple) -> 'Matrix':
        "Return Matrix from iterable."
        return cls(iterable, shape=shape)
    
    @classmethod
    def zeros(cls, shape: tuple) -> 'Matrix':
        "Return Matrix of zeros in given shapes."
        return cls([0]*reduce(multiply, shape), shape=shape)
    
    @classmethod
    def identity(cls, size: int) -> 'Matrix':
        "Return square identity Matrix of given size."
        values = []
        next_ = 0
        for i in range(size**2):
            if i == next_:
                values.append(1)
                next_ += size+1
            else:
                values.append(0)
        return cls(values, shape=(size, size))
    
    def copy(self) -> 'Matrix':
        "Return a copy of this matrix"
        return self.from_iter(self.__m, shape=self.shape)
    
    def __reversed__(self) -> reversed:
        "Return a copy of self, but order of elements is reversed."
        return reversed(self.__m)
    
    def __contains__(self, value: Union[int, float]) -> bool:
        "Return if self contains value"
        return value in self.__m
    
    @mapop
    def __pos__(self) -> 'Matrix':
        "Return unary positive of self"
        return +self
    
    @mapop
    def __neg__(self) -> 'Matrix':
        "Return negated matrix"
        return -self
    
    @onlytype(int)
    @mapop
    def __invert__(self) -> 'Matrix':
        "Return bitwise NOT of self if all items are intigers"
        return ~self
    
    @mapop
    def __abs__(self) -> 'Matrix':
        "Return abs'd matrix"
        return abs(self)
    
    def __round__(self, ndigits: int=None) -> 'Matrix':
        "Return matrix but each element is rounded"
        return self.from_iter((round(x, ndigits) for x in self.__m), shape=self.shape)
    
    @mapop
    def __ceil__(self) -> 'Matrix':
        "Return matrix but each element is ceil ed"
        # typecheck: error: Argument 1 to "ceil" has incompatible type "Matrix"; expected "Union[SupportsFloat, SupportsIndex]"
        return math.ceil(self)
    
    @mapop
    def __floor__(self) -> 'Matrix':
        "Return matrix but each element is floored"
        # typecheck: error: Argument 1 to "floor" has incompatible type "Matrix"; expected "Union[SupportsFloat, SupportsIndex]"
        return math.floor(self)
    
    @mapop
    def __trunc__(self) -> 'Matrix':
        "Return matrix but each element is trunc ed"
        # typecheck: error: Incompatible return value type (got "int", expected "Matrix")
        return math.trunc(self)
    
    def __bool__(self):
        "Return True if any element is true, False otherwise"
        return any(self.__m)
    
    @mmathop
    @simpleop
    def __add__(self, rhs) -> 'Matrix':
        "Add number to each element"
        return self + rhs
    __radd__ = __add__
    
    @mmathop
    @simpleop
    def __sub__(self, rhs):
        "Subtract number from each element"
        return self - rhs
    
    @mmathop
    @simpleop
    def __rsub__(self, lhs):
        "Subtract but from left hand side"
        return lhs - self
    
    @mmathop
    @simpleop
    def __mul__(self, rhs):
        "Multiply each element by number"
        return self * rhs
    __rmul__ = __mul__
    
    @mmathop
    @simpleop
    def __truediv__(self, rhs):
        "Divide each element by number"
        return self / rhs
    
    @mmathop
    @simpleop
    def __rtruediv__(self, lhs):
        "Division but from left hand side"
        return lhs / self
    
    @mmathop
    @simpleop
    def __floordiv__(self, rhs) -> 'Matrix':
        "Floor divide each element by number"
        return self // rhs
    
    @mmathop
    @simpleop
    def __rfloordiv__(self, lhs) -> 'Matrix':
        "Floor division but from left hand side"
        return lhs // self
    
    @mmathop
    @simpleop
    def __pow__(self, rhs):
        "Get element to the power of number for each element"
        return self ** rhs

    @mmathop
    @simpleop
    def __rpow__(self, lhs):
        "Power, but from left hand side"
        return lhs ** self
    
    @mmathop
    @simpleop
    def __mod__(self, rhs) -> 'Matrix':
        "Return remainder of division (modulo) of self by rhs"
        return self % rhs
    
    @mmathop
    @simpleop
    def __rmod__(self, lhs) -> 'Matrix':
        "Modulo but from left hand side."
        return lhs % self
    
    def __divmod__(self, rhs) -> tuple[Union[int, float, complex], Union[int, float]]:
        "Return tuple of (self // rhs, self % rhs)"
        return self // rhs, self % rhs
    
    def __rdivmod__(self, lhs) -> tuple[Union[int, float, complex], Union[int, float]]:
        "Divmod but from left hand side"
        return lhs // self, lhs % self
    
    @mmathop
    @boolop('all')
    def __eq__(self, rhs) -> bool:
        "Return True if all elements of both matrixs are equal."
        return self == rhs
    
    @mmathop
    @boolop('any')
    def __ne__(self, rhs) -> bool:
        "Return True if any element is not equal to it's counterpart in the other matrix"
        return self != rhs
    
    @mmathop
    @boolop('all')
    def __lt__(self, rhs) -> bool:
        "Return True if all elements of self are less than corresponding element in rhs."
        return self < rhs
    
    @mmathop
    @boolop('all')
    def __gt__(self, rhs) -> bool:
        "Return True if all elements of self are greater than corresponding element in rhs."
        return self > rhs
    
    @mmathop
    @boolop('all')
    def __le__(self, rhs) -> bool:
        "Return True if all elements of self are less than or equal to corresponding element."
        return self <= rhs
    
    @mmathop
    @boolop('all')
    def __ge__(self, rhs) -> bool:
        "Return True if all elements of self are greater than or equal to corresponding element."
        return self >= rhs
    
    def __hash__(self):
        return hash(self.__m)
    
    @mapop
    def conv_ints(self):
        "Return copy of self, but all items are intigers"
        return int(self)
    
    @mapop
    def conv_floats(self):
        "Return copy of self, but all items are floats"
        return float(self)
    
    # Intiger operators
    @mmathop
    @onlytypemath(int)
    @simpleop
    def __and__(self, rhs) -> 'Matrix':
        "Return bitwise AND of self and rhs if both are composed of intigers"
        return self & rhs
    __rand__ = __and__
    
    @mmathop
    @onlytypemath(int)
    @simpleop
    def __or__(self, rhs) -> 'Matrix':
        "Return bitwise OR of self and rhs if both are composed of intigers"
        return self | rhs
    __ror__ = __or__
    
    @mmathop
    @onlytypemath(int)
    @simpleop
    def __lshift__(self, rhs) -> 'Matrix':
        "Return bitwise left shift of self by rhs if both are composed of intigers"
        return self << rhs
    
    @mmathop
    @onlytypemath(int)
    @simpleop
    def __rlshift__(self, lhs) -> 'Matrix':
        "Bitwise left shift but from left hand side"
        return lhs << self
    
    @mmathop
    @onlytypemath(int)
    @simpleop
    def __rshift__(self, rhs) -> 'Matrix':
        "Return bitwise right shift of self by rhs if both are composed of intigers"
        return self >> rhs
    
    @mmathop
    @onlytypemath(int)
    @simpleop
    def __rrshift__(self, lhs) -> 'Matrix':
        "Bitwise right shift but from left hand side"
        return lhs >> self
    
    @mmathop
    @onlytypemath(int)
    @simpleop
    def __xor__(self, rhs) -> 'Matrix':
        return self ^ rhs
    __rxor__ = __xor__
    
    def __matmul__(self, rhs):
        "Return matrix multiply with rhs."
        if not hasattr(rhs, 'shape'):
            raise AttributeError('Right hand side has no `shape` attribute')
##        if not hasattr(rhs, '__getitem__'):
##            raise ValueError('Right hand side is not indexable!')
##        rhs_index = rhs.__getitem__
##        try:
##            rhs_index((slice(None), slice(None)))
##        except TypeError:
##            rhs_index = lambda x:[rhs.__getitem__(x[1])]
##        if not hasattr(rhs, 'shape'):
##            if not hasattr(rhs, '__len__'):
##                raise AttributeError('Right hand side has no `shape` or `len` attribute')
##            else:
##                rhs_shape = (len(rhs), 1)
##        else:
##            rhs_shape = rhs.shape
        if len(rhs.shape) != 2:
            raise ValueError('Right hand side is more than a two dimensional matrix')
        if self.shape[1] != rhs.shape[0]:
            raise ArithmeticError('Right hand side is of an incompatable shape for matrix'
                                  'multiplication')
        results = []
        for row_idx in range(self.shape[0]):
            row = self[row_idx, :]
            for column_idx in range(rhs.shape[1]):
                column = rhs[:, column_idx]
##                column = rhs_index((slice(None), column_idx))
                results.append(math.fsum(x*y for x, y in zip(row, column)))
        return self.__class__(results, (self.shape[0], rhs.shape[1]))
    
    def minor(self, index: tuple) -> 'Matrix':
        "Return new matrix without index location in any shape"
        pos_row, pos_col = index
        results = []
        for ridx, row in enumerate(self.rows()):
            if ridx == pos_row:
                continue
            for cidx, val in enumerate(row):
                if cidx == pos_col:
                    continue
                results.append(val)
        return self.__class__(results, (self.shape[0]-1, self.shape[1]-1))
    
    @onlysquare
    def determinent(self) -> int:
        "Return the determinent of this matrix."
        value = 0
        adding = True
        for mult, matrix in ((self[0, x], self.minor((0, x))) for x in range(self.shape[0])):
            if matrix.shape == (1, 1):
                val = matrix[0, 0]
            else:
                val = matrix.determinent()
            # typecheck: note: Both left and right operands are unions
            value += (adding*2-1) * val * mult
            adding = not adding
        return value
    
    def get_pos_cofactor(self, index) -> Union[int, float]:
        "Return cofactor of item at index in this matrix"
        return (-1) ** sum(index) * self.minor(index).determinent()
    
    def cofactor(self) -> 'Matrix':
        "Return cofactor of self"
        values = [
            self.get_pos_cofactor((r, c))
            for r in range(self.shape[0])
            for c in range(self.shape[1])
        ]
        return self.__class__(values, self.shape)
    
    def transpose(self) -> 'Matrix':
        "Return transpose of self"
        values = [self[:,x] for x in range(self.shape[1])]
        return self.__class__(values, self.shape)
    
    def adjugate(self) -> 'Matrix':
        "Return adjugate of self"
        return self.cofactor().transpose()
    adjoint = adjugate
    
    @onlysquare
    def inverse(self):
        "Return the inverse of this matrix"
        det = self.determinent()
        if det == 0:
            raise ZeroDivisionError('Determinent of this matrix is zero!')
        return self.adjugate() / det

class Matrix44(Matrix):
    "4x4 Matrix with extra 3d math functions"
    __slots__: tuple = tuple()
    def __init__(self, data, shape=(4, 4), dtype=list):
        super().__init__(data, (4, 4), dtype)
    
    # pylint: disable=unused-private-member
    def __get_row_0(self):
        return Vector4.from_iter(self[0, :], dtype=tuple)
    
    def __get_row_1(self):
        return Vector4.from_iter(self[1, :], dtype=tuple)
    
    def __get_row_2(self):
        return Vector4.from_iter(self[2, :], dtype=tuple)
    
    def __get_row_3(self):
        return Vector4.from_iter(self[3, :], dtype=tuple)
    
    def __set_row_0(self, values):
        values = tuple(values)[:4]
        self[0, :] = list(map(float, values))
    
    def __set_row_1(self, values):
        values = tuple(values)[:4]
        self[1, :] = list(map(float, values))
    
    def __set_row_2(self, values):
        values = tuple(values)[:4]
        self[2, :] = list(map(float, values))
    
    def __set_row_3(self, values):
        values = tuple(values)[:4]
        self[3, :] = list(map(float, values))
    
    __row0 = property(__get_row_0, __set_row_0, None, 'Row 0')
    __row1 = property(__get_row_1, __set_row_1, None, 'Row 1')
    __row2 = property(__get_row_2, __set_row_2, None, 'Row 2')
    __row3 = property(__get_row_3, __set_row_3, None, 'Row 3')
    
    x_axis = __row0
    right = __row0
    y_axis = __row1
    up = __row1
    z_axis = __row2
    forward = __row2
    translate = __row3
    
    def move(self,
             forward: Union[int, float]=None,
             right: Union[int, float]=None,
             # pylint: disable=invalid-name
             up: Union[int, float]=None
    ) -> None:
        """Changes the translation according to a direction vector.
        To move in opposite directions (i.e back, left and down), first
        negate the vector.
        
        forward -- Units to move in the 'forward' direction
        right -- Units to move in the 'right' direction
        up -- Units to move in the 'up' direction
        
        """
        
        if forward is not None:
            self.translate += self.forward * forward
        
        if right is not None:
            self.translate += self.right * right
        
        if up is not None:
            self.translate += self.up * up
    
    @classmethod
    def make_rotation_about_axis(cls, axis, angle):
        """Makes a rotation Matrix44 around an axis.

        axis -- An iterable containing the axis (three values)
        angle -- The angle to rotate (in radians)

        """
        
        # pylint: disable=invalid-name
        c = math.cos(angle)
        s = math.sin(angle)
        omc = 1 - c
        x, y, z = axis
        
        results = [x*x*omc+c,   y*x*omc+z*s, x*z*omc-y*s, 0,
                   x*y*omc-z*s, y*y*omc+c,   y*z*omc+x*s, 0,
                   x*z*omc+y*s, y*z*omc-x*s, z*z*omc+c,   0,
                   0,           0,           0,           1]
        return cls(results)
    
    @classmethod
    def make_xyz_rotation(cls, angle_x, angle_y, angle_z) -> 'Matrix44':
        "Makes a rotation Matrix44 about 3 axis."
        
        # pylint: disable=invalid-name
        cx = math.cos(angle_x)
        sx = math.sin(angle_x)
        cy = math.cos(angle_y)
        sy = math.sin(angle_y)
        cz = math.cos(angle_z)
        sz = math.sin(angle_z)
        
        sxsy = sx*sy
        cxsy = cx*sy
        
        # http://web.archive.org/web/20041029003853/http:/www.j3d.org/matrix_faq/matrfaq_latest.html#Q35
        #A = math.cos(angle_x)
        #B = math.sin(angle_x)
        #C = math.cos(angle_y)
        #D = math.sin(angle_y)
        #E = math.cos(angle_z)
        #F = math.sin(angle_z)
        
        #     |  CE      -CF       D   0 |
        #M  = |  BDE+AF  -BDF+AE  -BC  0 |
        #     | -ADE+BF   ADF+BE   AC  0 |
        #     |  0        0        0   1 |
        
        results = [ cy*cz,  sxsy*cz+cx*sz,  -cxsy*cz+sx*sz, 0,
                    -cy*sz, -sxsy*sz+cx*cz, cxsy*sz+sx*cz,  0,
                    sy,     -sx*cy,         cx*cy,          0,
                    0,      0,              0,              1]
        
        return cls(results)
    
    def trace(self):
        "Return sum of scale"
        return math.fsum((self[0, 0], self[1, 1], self[2, 2], self[3, 3]))

def test():
    "test"
    # pylint: disable=invalid-name
    A = Matrix([0, 0, 2, 1, 3, -2, 1, -2, 1], shape=(3, 3))
    X = Matrix([1, -2, 3], shape=(3, 1))
    print(f'{A @ X == [6, -11, 8]=}')
    
    A = Matrix([0, 0, 2, 1, 3, -2, 1, -2, 1], shape=(3, 3))
    X = Matrix([-1.1, 1.7, 4.5], shape=(3, 1))
    print(f'{A @ X == [9, -5, 0]=}')
    
    A = Matrix([-3, 4, 0, 2, -5, 1, 0, 2, 3], (3, 3))
    print(f'{A.determinent()==27=}')
    
    A = Matrix([-3, 4, 0, 2, -5, 1, 0, 2, 3], (3, 3))
    print(f'{round(A.inverse() @ A)==Matrix.identity(3)=}')

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    test()
