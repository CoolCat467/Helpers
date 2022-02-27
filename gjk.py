#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GJK algorithm

"""GJK algorithm

Implementation of the Gilbert–Johnson–Keerthi distance algorithm"""

# Programmed by CoolCat467 12/14/2021

__title__ = 'GJK'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import math
from vector import Vector

class Shape:
    "Shape made of vectors"
    def __init__(self, points:list):
        self.points = [Vector(*v, type_=3) for v in points]
    
    def __repr__(self):
        args = ', '.join(map(repr, self.points))
        return f'{self.__class__.__name__}(({args}))'
    
    @property
    def center(self):
        "Center of this shape"
        return sum(self.points) / len(self.points)
    
    def furthest_point(self, vector):
        "Return vertex on polygon furthest along direction."
        angles = []
        center = self.center
        for p in self.points:
            v = p - center
            v2 = Vector.from_iter(v, type_=2)
            if v[2] != 0:
                raise ValueError('Vector with Z component!')
            angles.append(v2.get_heading())
        target = Vector.from_iter(vector, type_=2)
        target_deg = target.get_heading()
        results = [abs(deg-target_deg) for deg in angles]
        return self.points[results.index(min(results))]
    
    def __iter__(self):
        return iter(self.points)

def regular_poly(edges, side_length):
    "Return regular polygon"
    points = []
    deg = edges/360
    for i in range(1, edges+1):
        r = math.radians(i*deg)
        v = math.sin(r)*side_length, math.cos(r)*side_length
        points.append(v)
    return Shape(points)

def support(shape1:Shape, shape2:Shape, d:Vector):
    "Return closest point in Minkowski sum of shapes."
    return shape1.furthest_point(d) - shape2.furthest_point(-d)

def triple_product(a:Vector, b:Vector, c:Vector):
    "Returns (a x b) x c -- x represents cross product."
    return a.cross(b).cross(c)
##    return b * c.dot(a) - a * c.dot(b)

def contains_origin(simplex, vector):
    "Return True if simplex contains the origin."
    A = simplex[-1]
    AO = -A
    if len(simplex) == 2:
        # Line case
        B = simplex[0]
        AB = B - A
        ABperp = triple_product(AB, AO, AB)
        # Needs to handle edge cases of if origin lies on an edge
        
        return ABperp
    if len(simplex) > 3 or len(simplex) < 2:
        return False
    # Triangle case
    B, C = simplex[1], simplex[0]
    AB = B - A
    AC = C - A
    ABperp = triple_product(AC, AB, AB)
    ACperp = triple_product(AB, AC, AC)
    
    if ABperp.dot(AO) > 0:
        del simplex[0]
        return ABperp
    if ACperp.dot(AO) > 0:
        del simplex[1]
        return ACperp
    
    # Otherwise origin must be in triangle
    return True

def GJK(shape1, shape2):
    "Return True if shapes 1 and 2 interesect."
    shape1, shape2 = Shape(shape1), Shape(shape2)
    d = (Vector(*shape2.center) - Vector(*shape1.center)).normalize()
    simplex = [support(shape1, shape2, d)]
    d = -simplex[0]
    while True:
        A = support(shape1, shape2, d)
        if A.dot(d) < 0:
            return False
        simplex.append(A)
        res = contains_origin(simplex, d)
        if isinstance(res, Vector):
            d = res
            continue
        return res

def run():
    "Test"
##    shape1 = [[0, 5], [3, 9], [0, 10]]
##    shape2 = [[1, 0], [4, 4], [4, 9], [1, 9]]
    shape1 = [[0, 0], [0, 4], [4, 4], [4, 0]]
    shape2 = [[0, 0], [-3, 0], [-3, -3], [0, 3]]
##    shape1 = [Vector.from_iter(v)+[0, 20] for v in shape2]
    print(GJK(shape1, shape2))

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
