import pygame as pg
import math as m
import random as rand
import os
import sys

from lives_class import Lives
from Player import Spaceship


pg.init()

screen = pg.display.set_mode((800,400), pg.SCALED | pg.RESIZABLE)
clock = pg.time.Clock()

lives = Lives()
player = pg.sprite.GroupSingle()
player.add(Spaceship())
player.sprite.rect.midbottom = (600, 400)   # the cat starts in the apartment

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            full = pg.display.is_fullscreen()
            if event.key == pg.K_F11 or (event.key == pg.K_ESCAPE and full):
                pg.display.toggle_fullscreen()

        Spaceship = player.sprite

        # if cat.hard_landing or bitten or hit_by_car:
        #     shake_timer = SHAKE_FRAMES
        #     lives.lose_life(1)
        #     if lives.out_of_lives():
        #         haptics.set(0)
        #         py.quit()
        #         sys.exit()
        # lives.update()
        lives.draw(screen)
        pg.display.update()
        clock.tick(60)
