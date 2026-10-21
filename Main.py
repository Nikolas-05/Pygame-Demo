import pygame as pg
import math as m
import random as rand
import os
import sys
import Player
import Laser

#Initialize everything
pg.init()

screen = pg.display.set_mode((800,800), pg.SCALED | pg.RESIZABLE)
clock = pg.time.Clock()
player = Player.Player(x=400, y=700, scale=2)
dt = 0
lasers = []
last_laser_timer = 0
time_between_shot =  0.5


while True:
    
    #Basic Handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            full = pg.display.is_fullscreen()
            if event.key == pg.K_F11 or (event.key == pg.K_ESCAPE and full):
                pg.display.toggle_fullscreen()
    
    #Player control section
    keys = pg.key.get_pressed()
    screen.fill("black")
    
    if keys[pg.K_SPACE] and (pg.time.get_ticks()-last_laser_timer)/1000 > time_between_shot:
        laser = Laser.Laser(player.player_rect.centerx, player.player_rect.top, owner="player")
        lasers.append(laser)
        last_laser_timer= pg.time.get_ticks()
    
    player.move(dt, keys)
    
    
    #Game update section
    for laser in lasers:
        laser.move(dt, speed_scale=50)
        laser.destroy()
        laser.update()
        laser.show(screen)
    lasers = [laser for laser in lasers if not laser.destroyed]

    player.update()
    player.show(screen)
    
    pg.display.update()
    dt = clock.tick(60)/1000
    
