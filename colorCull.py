#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Basically compress images to use less colors.


"Compress images to use less colors"

# Programmed by CoolCat467

import numpy as np
import functools
from typing import Union

import pygame
from pygame.locals import *


__title__ = 'Color Cull'
__author__ = 'CoolCat467'
__version__ = '1.0.0'
__ver_major__ = 1
__ver_minor__ = 0
__ver_patch__ = 0

SCREENSIZE = (600, 600)
FPS = 60

class imegris:
    "Image"
    __slots__ = 'pallette_max_disjoint', 'pallette', 'image',\
    'location', 'rotation', 'rotation_speed', 'data'
    
    def __init__(self, filename: str, diff: Union[int, float] = 65, init_pallette=None):
        if init_pallette is None:
            init_pallette = []
        self.pallette = init_pallette
        self.image = None
        self.location = [0, 0]
        self.rotation_speed = 1
        self.rotation = 0
        self.data = None
        self.pallette_max_disjoint = diff
        self.get_image(filename)
    
    @functools.lru_cache()
    def get_pallette(self, color: tuple) -> int:
        "Return color's index in color pallette."
        if color in self.pallette:
            return self.pallette.index(color)
        success = {}
        for idx in reversed(range(len(self.pallette))):
            pcolor = self.pallette[idx]
            disjoint = [abs(i[0] - i[1]) for i in zip(color, pcolor)]
            mean = round(sum(disjoint) / len(disjoint))
            success[mean] = idx
        if not success:
            self.pallette.append(color)
            return len(self.pallette) - 1
        best = min(success)
        if best > self.pallette_max_disjoint:
            self.pallette.append(color)
            return len(self.pallette) - 1
        return success[best]
    
    def get_image(self, filename: str) -> list:
        "Load image file, generate color pallette, and update image from compression."
        surf = pygame.image.load(filename)
        surf.convert_alpha()
        w, h = surf.get_size()
        arr = np.empty((w, h), int)
        #vals = [];
        for y in range(h):
            for x in range(w):
                r, g, b, a = surf.get_at((x, y))
                cidx = self.get_pallette((r, g, b))
                #if not cidx in vals:#
##                vals.append(cidx);
                color = self.pallette[cidx]
                arr[x, y] = cidx
                col = (*color, a)
                surf.set_at((x, y), col)
        #print(self.pallette)
        surf.convert_alpha()
        
        self.image = surf
        self.data = arr
    
    def get_data(self) -> tuple:
        "Return size, pallette, and pixel data from image."
        diff = []
        for line in self.data:
            last = None
            for pixel in line:
                if last != pixel:
                    diff.append([1, pixel])
                    last = pixel
                else:
                    diff[-1][0] += 1
            diff.append([0, 'lb'])
        size = [len(self.data), len(line)]
        pal = [[x for x in rgb] for rgb in self.pallette]
        return size, pal, diff
    
    def update(self, time_passed_seconds) -> None:
        "Update rotation"
##        self.rotation += self.rotation_speed * time_passed_seconds
        self.rotation += 1
        self.rotation %= 360
    
    def render(self, surf) -> None:
        "Blit self.image to surf centered at self.location if self.image is not None."
        if self.image is None:
            return
        x, y = self.location
        image = pygame.transform.rotate(self.image, round(360 - self.rotation))
        image.convert_alpha()
        w, h = image.get_size()
        pos = (int(x - w / 2), int(y - h / 2))
        surf.blit(image, pos)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def run():
    "Load image and save data and predicted result after removing some colors."
    screen = pygame.display.set_mode(SCREENSIZE, 0, 16)
    pygame.display.set_caption(__title__+' '+__version__)
    
    # Set up the FPS clock
    clock = pygame.time.Clock()
##    pallette = ['e0e7e0',
##                'dead82',
##                '1d6454',
##                '55140e',
##                'e58169',
##                'c46b67',
##                '441414',
##                '000000',
##                'ffffff',
##                '13302b',
##                '1b5546',
##                'bf9275',
##                '646963',
##                'b8bdb7'
##                ]
##    pallette = list(map(hex_to_rgb, pallette))
    pallette = []
##    print(len(pallette))
    img = imegris('mr_floppy.jpg', 28, pallette)
    img.location = [SCREENSIZE[0]/2, SCREENSIZE[1]/2]
    img.rotation_speed = 0
##    size, pallette, diff = img.get_data()
##    text = 'var size = '
##    text += str(size) + ';\n'
##    text += 'var pallette = '
##    text += str(pallette) + ';\n'
##    text += 'var data = '
##    text += str(diff) + ';\n'
##    with open('data.txt', 'w', encoding='utf-8') as file:
##        file.write(text)
##        file.close()
    pygame.image.save(img.image, 'image.png')
    print(len(img.pallette))
    
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                RUNNING = False
            if event.type == KEYUP and event.key == K_ESCAPE:
                RUNNING = False
            if event.type == VIDEORESIZE:
                pass
        
        screen.fill((0, 255, 0))
        
        time_passed = clock.tick(FPS)
        time_passed_seconds = time_passed / 1000
        
        img.update(time_passed_seconds)
        img.render(screen)
        
        # Update the display
        pygame.display.update()

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    try:
        pygame.init()
        run()
    finally:
        pygame.quit()
