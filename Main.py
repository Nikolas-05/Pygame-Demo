import pygame as pg
import math as m
import random as rand
import os
import sys


pg.init()

screen = pg.display.set_mode((800,400), pg.SCALED | pg.RESIZABLE)
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            full = pg.display.is_fullscreen()
            if event.key == pg.K_F11 or (event.key == pg.K_ESCAPE and full):
                pg.display.toggle_fullscreen()
                
        pg.display.update()
        clock.tick(60)
