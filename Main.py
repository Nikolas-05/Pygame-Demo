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
import Lives                                   # added: the hearts / lives counter
#Initialize everything
pg.init()


window_width = 800
window_height = 800
screen = pg.display.set_mode((window_width,window_height), pg.SCALED | pg.RESIZABLE)
background= Background.Background(window_width, window_height)

clock = pg.time.Clock()
player = Player.Player(x=window_width/2, y=.875*window_height, scale=window_width*2/800)   # adjusted: y was 700, below the 400 tall window, so the player was off screen
dt = 0
lasers = []
enemies = []
last_laser_timer = 0
time_between_shot =  .5
score_obj = Score.Score(650*window_width/800,10*window_height/800, None, int(40*window_width/800))
score = 0
lives = Lives.Lives()                          # added: start with 3 lives
keys = pg.key.get_pressed()

#Wave handling
waves = open("waves.txt", "r")


# # ---- intro screen ----
intro_bg = pg.transform.smoothscale(pg.image.load('Galaxy_background_black.PNG').convert(), screen.get_size())   # adjusted: no outer while True, it trapped the game in the intro forever
title = pg.font.Font(None, int(72*window_width/800)).render('Galaga for Engineers', True, 'white')       # adjusted: moved out of the removed while True
prompt = pg.font.Font(None, int(32*window_width/400)).render('Press SPACE to start', True, 'white')      # adjusted: moved out of the removed while True

while not keys[pg.K_SPACE]:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    screen.blit(intro_bg, (0, 0))
    screen.blit(title, title.get_rect(center=(window_width/2, window_height*.375)))
    screen.blit(prompt, prompt.get_rect(center=(window_width/2, .65*window_height)))
    pg.display.update()
    clock.tick(60)
    keys = pg.key.get_pressed()                # added: re-read the keyboard every frame, so pressing SPACE ends the intro

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
            enemies.append(ShootingEnemy.ShootingEnemy(x_pos, y = 0, scale = 2*window_width/800, laser_time=1))
        elif line[i] == "E":
            enemies.append(Enemy.Enemy(x_pos, y = 0, scale = 5*window_width/800))

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
        laser = Laser.Laser(player.player_rect.centerx, player.player_rect.top, owner= player, scale=1*window_width/800)
        lasers.append(laser)
        last_laser_timer= pg.time.get_ticks()
    
    player.move(dt, keys, speed=500*window_width/800)
    
    #Game update section
    if not enemies:
        progressWave(waves)
    
    for laser in lasers:
        laser.move(dt, speed_scale=50*window_height/800)
        laser.destroy()
        laser.update()
        laser.show(screen)
    lasers = [laser for laser in lasers if not laser.destroyed]
    
    for enemy in enemies:
        if not isinstance(enemy,ShootingEnemy.ShootingEnemy):
            enemy.move(dt, v_x=0, v_y = 80*window_height/800)
        else:
            enemy.move(dt, v_x=0, v_y = 50*window_height/800)
        enemy.update()
        enemy.show(screen)
        
        if isinstance(enemy, ShootingEnemy.ShootingEnemy):
            if (pg.time.get_ticks()-enemy.last_laser_timer)/1000 > enemy.laser_time:
                enemy.last_laser_timer = pg.time.get_ticks()
                lasers.append(enemy.shoot())   
        
        for laser in lasers:
            score+=enemy.destroy(laser)
            laser.destroy(enemy)

        if enemy.enemy_rect.colliderect(player.player_rect):   # added: the enemy touched the player
            enemy.destroy()                                     # added: remove that enemy so it only costs one life
            lives.lose_life(1)                                  # added: the player loses one life
            if lives.out_of_lives():                            # added: no lives left
                pg.quit()                                       # added: end the game
                sys.exit()                                      # added
    enemies = [enemy for enemy in enemies if not enemy.destroyed]
    
    
    text = "Score: " + str(score)
    score_obj.update(text, screen)
    player.update()
    player.show(screen)
    lives.draw(screen)                         # added: draw the hearts in the top left
    
    pg.display.update()
    dt = clock.tick(60)/1000
