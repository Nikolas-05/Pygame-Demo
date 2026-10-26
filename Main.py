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
from Lives import Lives
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
time_between_shot =  .5
keys = pg.key.get_pressed()
num_enemy = 10

score_obj = Score.Score(650,10, None, 40)
score = 0
for i in range(num_enemy):
    x_pos = 800/(num_enemy+1)*(i+1)
    enemies.append(ShootingEnemy.ShootingEnemy(x_pos, y=0, scale = 2, laser_time = 1))

lives = Lives()


def game_over():                           # added: the outro, used by both ways of losing the last life
    outro_bg = pg.transform.smoothscale(pg.image.load('Galaxy_background_black.PNG').convert(), screen.get_size()) 
    title = pg.font.Font(None, 72).render('Good Game Engineer', True, 'white')      
    prompt = pg.font.Font(None, 32).render('See you Again', True, 'white') 
    while keys[pg.K_SPACE]:            # added: wait for the shoot button to be let go first

        pg.event.pump()                          # added



    while not keys[pg.K_SPACE]:                                           
        for event in pg.event.get():                                              
            if event.type == pg.QUIT:                                          
                pg.quit()                                                        
                sys.exit()                                                          
        screen.blit(outro_bg, (0, 0))  # adjusted: was intro_bg                                            
        screen.blit(title, title.get_rect(center=(400, 150)))               
        screen.blit(prompt, prompt.get_rect(center=(400, 260)))                 
        pg.display.update()                                                          
        clock.tick(60)
    pg.quit()                              # added
    sys.exit()    


    
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
        num_enemy +=10
        for i in range(num_enemy):
            x_pos = 800/(num_enemy+1)*(i+1)
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
        if isinstance(enemy, ShootingEnemy.ShootingEnemy):
            if (pg.time.get_ticks()-enemy.last_laser_timer)/1000 > enemy.laser_time:
                enemy.last_laser_timer = pg.time.get_ticks()
                lasers.append(enemy.shoot())        
        for laser in lasers:
            score+=enemy.destroy(laser)
            laser.destroy(enemy)
    enemies = [enemy for enemy in enemies if not enemy.destroyed]
    
    # if pg.sprite.spritecollide(player, enemies, True):
    #     lives.lose_life(1)
    # speed_boost = 0                       # added: a collision puts enemies back to their original speed
    # if lives.out_of_lives():
    #     game_over()     
    
    text = "Score: " + str(score)
    score_obj.update(text, screen)
    player.update()
    player.show(screen)
    lives.draw(screen)
    pg.display.update()
    dt = clock.tick(60)/1000