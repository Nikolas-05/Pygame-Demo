import pygame as pg
import math as m
import random as rand
import os
import sys
import Player
import Laser
import Enemy
import Background

#Initialize everything
pg.init()

window_width = 800
window_height = 800
screen = pg.display.set_mode((window_width,window_height), pg.SCALED | pg.RESIZABLE)
background= Background.Background(window_width, window_height)
clock = pg.time.Clock()
player = Player.Player(x=400, y=700, scale=2)
dt = 0
lasers = []
enemies = []
last_laser_timer = 0
time_between_shot =  0.5

for i in range(5):
    x_pos = 800/5*i
    enemies.append(Enemy.Enemy(x_pos, y=0, scale = 2))

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
    background.show(screen)
    
    if keys[pg.K_SPACE] and (pg.time.get_ticks()-last_laser_timer)/1000 > time_between_shot:
        laser = Laser.Laser(player.player_rect.centerx, player.player_rect.top, owner= player)
        lasers.append(laser)
        last_laser_timer= pg.time.get_ticks()
    
    player.move(dt, keys)
    
    
    #Game update section
    if not enemies:
        for i in range(5):
            x_pos = 800/5*i
            enemies.append(Enemy.Enemy(x_pos, y=0, scale = 2))
    
    
    for laser in lasers:
        laser.move(dt, speed_scale=50)
        laser.destroy()
        laser.update()
        laser.show(screen)
    lasers = [laser for laser in lasers if not laser.destroyed]
    
    for enemy in enemies:
        enemy.move(dt, v_x=0, v_y = 50)
        enemy.update()
        enemy.show(screen)
        for laser in lasers:
            enemy.destroy(laser)
            laser.destroy(enemy)
    enemies = [enemy for enemy in enemies if not enemy.destroyed]

    player.update()
    player.show(screen)
    
    pg.display.update()
    dt = clock.tick(60)/1000
    
    
    
