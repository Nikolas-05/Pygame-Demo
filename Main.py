import pygame as pg
import math as m
import random as rand
import os
import sys

from lives_class import Lives
from Player import Spaceship
from Enemy_class import Enemy


pg.init()

screen = pg.display.set_mode((800,400), pg.SCALED | pg.RESIZABLE)
clock = pg.time.Clock()

lives = Lives()
player = pg.sprite.GroupSingle()
player.add(Spaceship())
player.sprite.rect.midbottom = (400, 400)   # the ship starts at the bottom middle

enemies = pg.sprite.Group()
ENEMY_SPAWN = pg.USEREVENT + 1
pg.time.set_timer(ENEMY_SPAWN, 2000)      

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            full = pg.display.is_fullscreen()
            if event.key == pg.K_F11 or (event.key == pg.K_ESCAPE and full):
                pg.display.toggle_fullscreen()
        if event.type == ENEMY_SPAWN:
            enemies.add(Enemy(screen.get_width()))

    screen.fill('black')
    player.update(screen.get_size())
    player.draw(screen)
    enemies.update(screen.get_height())
    
    if pg.sprite.spritecollide(player.sprite, enemies, True):
        lives.lose_life(1)
        if lives.out_of_lives():
            pg.quit()
            sys.exit()

    enemies.draw(screen)
    lives.draw(screen)
    pg.display.update()
    clock.tick(60)
