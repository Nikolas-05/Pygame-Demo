import pygame as pg
import math as m
import random as rand
import os
import sys

from lives_class import Lives
from Player import Spaceship, read_controls      # adjusted: read_controls lets the intro use the same 'throw' button
from Enemy_class import Enemy, Meteor


pg.init()

screen = pg.display.set_mode((800,400), pg.SCALED | pg.RESIZABLE)
clock = pg.time.Clock()

# ---- intro screen ----
intro_bg = pg.transform.smoothscale(pg.image.load('Demo_images/Galaxy_background_black.PNG').convert(), screen.get_size()) 
title = pg.font.Font(None, 72).render('Galaga for Engineers', True, 'white')      
prompt = pg.font.Font(None, 32).render('Press SPACE or X to start', True, 'white') 
while not read_controls()['shoot']:                                           
    for event in pg.event.get():                                              
        if event.type == pg.QUIT:                                          
            pg.quit()                                                        
            sys.exit()                                                          
    screen.blit(intro_bg, (0, 0))                                            
    screen.blit(title, title.get_rect(center=(400, 150)))               
    screen.blit(prompt, prompt.get_rect(center=(400, 260)))                 
    pg.display.update()                                                          
    clock.tick(60)

lives = Lives()

player = pg.sprite.GroupSingle()
player.add(Spaceship())
player.sprite.rect.midbottom = (400, 400)   # the ship starts at the bottom middle

enemies = pg.sprite.Group()
ENEMY_SPAWN = pg.USEREVENT + 1
pg.time.set_timer(ENEMY_SPAWN, 2000)

METEOR_SPAWN = pg.USEREVENT + 2
pg.time.set_timer(METEOR_SPAWN, 3000)      # a new meteor every 3 seconds

SPAWN_RAMP = pg.USEREVENT + 3              # added: an event that fires every 5 seconds to raise the spawn rate
pg.time.set_timer(SPAWN_RAMP, 5000)        # added
spawns_per_5s = 2.5                        # added: the starting rate, one enemy every 2 seconds = 2.5 per 5 seconds

dt = 0
stars = [[rand.randint(0, 800), rand.randint(0, 400), rand.choice([1, 1, 2])] for _ in range(80)]   # added: 120 stars as [x, y, size], most small, some bigger
speed_boost = 0                            # added: extra speed every enemy ship gets, grows over time


def game_over():                           # added: the outro, used by both ways of losing the last life
    outro_bg = pg.transform.smoothscale(pg.image.load('Demo_images/Galaxy_background_black.PNG').convert(), screen.get_size()) 
    title = pg.font.Font(None, 72).render('Good Game Engineer', True, 'white')      
    prompt = pg.font.Font(None, 32).render('See you Again', True, 'white') 
    while read_controls()['shoot']:            # added: wait for the shoot button to be let go first

        pg.event.pump()                          # added



    while not read_controls()['shoot']:                                           
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
    sys.exit()                             # added


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

        if event.type == SPAWN_RAMP:                                          # added: every 5 seconds
            spawns_per_5s += 1                                                # added: one more enemy per 5 seconds
            pg.time.set_timer(ENEMY_SPAWN, max(200, int(5000 / spawns_per_5s)))   # added: new time between spawns, never faster than one every 0.2s
            
    keys = pg.key.get_pressed()
    screen.fill('black')
    
    player.update(screen.get_size())
    scroll = player.sprite.scroll                                   # added: the ship flying left or right slides the world the other way
    width = screen.get_width()                                      # added
    for enemy in enemies:                                           # added: slide every enemy and meteor
        enemy.x = (enemy.x - scroll) % width                        # added: wrap so the world never ends
        if isinstance(enemy, Meteor):                               # added: meteors don't set their own x each frame
            enemy.rect.centerx = round(enemy.x)                     # added
    for laser in player.sprite.lasers + Enemy.lasers:               # added: slide every laser too
        laser.x_pos = (laser.x_pos - scroll) % width                # added
    for star in stars:                                              # added: the star background
        star[0] = (star[0] - scroll * star[2] / 2) % width          # added: slide with the world, bigger stars faster so they look closer
        star[1] = (star[1] + star[2] * 0.5) % screen.get_height()   # added: drift slowly down, so the ship looks like it's flying forward
        pg.draw.circle(screen, 'white', (star[0], star[1]), star[2])   # added: draw the star
    player.draw(screen)
    enemies.update(screen.get_height())
    
    if pg.sprite.spritecollide(player.sprite, enemies, True):
        lives.lose_life(1)
        speed_boost = 0                       # added: a collision puts enemies back to their original speed
        if lives.out_of_lives():
            game_over()                       # adjusted: show the outro, then quit
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

    for laser in Enemy.lasers:                                # added: move and draw every enemy laser
        laser.move(dt, speed_scale=50)                        # added: enemy lasers move down
        laser.destroy()                                       # added: used up once off the bottom of the screen
        laser.update()                                        # added
        if laser.proj.colliderect(player.sprite.rect):        # added: an enemy laser hit the player
            laser.destroyed = True                            # added: the laser is used up
            lives.lose_life(1)                                # added: the player loses one life
            if lives.out_of_lives():                          # added: all lives gone, so the game ends
                game_over()                                   # adjusted: show the outro, then quit
        laser.show(screen)                                    # added
    Enemy.lasers[:] = [laser for laser in Enemy.lasers if not laser.destroyed]   # added: drop used up enemy lasers

    speed_boost += 0.001                      # adjusted: enemies slowly speed up, every frame
    for enemy in enemies:                     # adjusted: loop over the enemies on screen
        if isinstance(enemy, Enemy):          # adjusted: only enemy ships, not meteors
            enemy.y += speed_boost            # adjusted: move it down a little extra on top of its own speed

    enemies.draw(screen)
    lives.draw(screen)
    pg.display.update()
    dt = clock.tick(60) / 1000                # seconds since the last frame, for the lasers
