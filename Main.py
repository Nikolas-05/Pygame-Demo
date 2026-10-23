import pygame as pg
import math as m
import random as rand
import os
import sys

from lives_class import Lives
from Player import Spaceship
from Enemy_class import Enemy, Meteor


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

METEOR_SPAWN = pg.USEREVENT + 2
pg.time.set_timer(METEOR_SPAWN, 3000)      # a new meteor every 3 seconds

dt = 0


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
        if event.type == METEOR_SPAWN:
            enemies.add(Meteor(screen.get_width()))
    keys = pg.key.get_pressed()
    screen.fill('black')
    
    player.update(screen.get_size())
    player.draw(screen)
    enemies.update(screen.get_height())
    
    if pg.sprite.spritecollide(player.sprite, enemies, True):
        lives.lose_life(1)
        if lives.out_of_lives():
            pg.quit()
            sys.exit()
    for laser in player.sprite.lasers:
        laser.move(dt, speed_scale=50)
        
        laser.destroy()
        laser.update()
        # a laser that hits an enemy kills it and is used up
        for enemy in enemies:
            if laser.proj.colliderect(enemy.rect):
                enemy.kill()
                laser.destroyed = True
        laser.show(screen)
    player.sprite.lasers = [laser for laser in player.sprite.lasers if not laser.destroyed]


    enemies.draw(screen)
    lives.draw(screen)
    pg.display.update()
    dt = clock.tick(60) / 1000                # seconds since the last frame, for the lasers
