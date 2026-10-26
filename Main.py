import pygame as pg
import math as m
import random as rand
import os
import sys
import Player
import Laser
import Enemy
import Score
import Background
import ShootingEnemy
#Initialize everything
pg.init()


window_width = 800
window_height = 400
screen = pg.display.set_mode((window_width,window_height), pg.SCALED | pg.RESIZABLE)
background= Background.Background(window_width, window_height)

clock = pg.time.Clock()
player = Player.Player(x=400, y=700, scale=2)
dt = 0
lasers = []
enemies = []
last_laser_timer = 0
time_between_shot =  .5
score_obj = Score.Score(650,10, None, 40)
score = 0

#Wave handling
waves = open("waves.txt", "r")

def progressWave(waves):
    line = waves.readline().rstrip("\r\n")
    line = list(line)
    if not line:
        return
    while line[0] == "#":
        line = waves.readline().rstrip("\r\n")
        line = list(line)
    for i in range(len(line)):
        x_pos = window_width/(len(line)+1)*(i+1)
        if line[i] == "S":
            enemies.append(ShootingEnemy.ShootingEnemy(x_pos, y = 0, scale = 2, laser_time=1))
        elif line[i] == "E":
            enemies.append(Enemy.Enemy(x_pos, y = 0, scale = 5))

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
        progressWave(waves)
    
    for laser in lasers:
        laser.move(dt, speed_scale=50)
        laser.destroy()
        laser.update()
        laser.show(screen)
    lasers = [laser for laser in lasers if not laser.destroyed]
    
    for enemy in enemies:
        if not isinstance(enemy,ShootingEnemy.ShootingEnemy):
            enemy.move(dt, v_x=0, v_y = 80)
        else:
            enemy.move(dt, v_x=0, v_y = 50)
        enemy.update()
        enemy.show(screen)
        
        if isinstance(enemy, ShootingEnemy.ShootingEnemy):
            if (pg.time.get_ticks()-enemy.last_laser_timer)/1000 > enemy.laser_time:
                enemy.last_laser_timer = pg.time.get_ticks()
                lasers.append(enemy.shoot())   
        
        for laser in lasers:
            score+=enemy.destroy(laser)
            laser.destroy(enemy)
    enemies = [enemy for enemy in enemies if not enemy.destroyed]
    
    
    text = "Score: " + str(score)
    score_obj.update(text, screen)
    player.update()
    player.show(screen)
    
    pg.display.update()
    dt = clock.tick(60)/1000
