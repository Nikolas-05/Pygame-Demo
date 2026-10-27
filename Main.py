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

# win screen

game_music=pg.mixer.Sound("music.mp3")
game_music.set_volume(0.3) # 0.0 to 1.0
music_channel=game_music.play(-1)

laser_sound = pg.mixer.Sound("laser.mp3")
laser_sound.set_volume(0.3)

winner_sound = pg.mixer.Sound("winner.mp3")
winner_sound.set_volume(0.3)



# restart when win/lose, maybe time, win screen
    
window_width = 800
window_height = 800
screen = pg.display.set_mode((window_width,window_height), pg.SCALED | pg.RESIZABLE)
background= Background.Background(window_width, window_height)

clock = pg.time.Clock()
player = Player.Player(x=window_width/2, y=.875*window_height, scale=window_width*2/800, window_width=window_width)   # adjusted: y was 700, below the 400 tall window, so the player was off screen
dt = 0
lasers = []
enemies = []
last_laser_timer = 0
time_between_shot =  .5
score_obj = Score.Score(650*window_width/800,10*window_height/800, None, int(40*window_width/800))
score = 0
lives = Lives.Lives(scale=1*window_width/400)                          # added: start with 3 lives
keys = pg.key.get_pressed()
start_time=0
game_active=True  
won=False


#Wave handling
waves = open("waves.txt", "r")


# # ---- intro screen ----
intro_bg = pg.transform.smoothscale(pg.image.load('Galaxy_background_black.PNG').convert(), screen.get_size())   # adjusted: no outer while True, it trapped the game in the intro forever
title = pg.font.Font(None, int(72*window_width/800)).render('Galaga for Engineers', True, 'white')       # adjusted: moved out of the removed while True
prompt = pg.font.Font(None, int(32*window_width/400)).render('Press SPACE to start', True, 'white')      # adjusted: moved out of the removed while True

trophy_surf=pg.image.load('GoldTrophy.png')
trophy_surf = pg.transform.scale(trophy_surf, (int(150*window_width/window_width), int(150*window_height/window_height)))
trophy_rect=trophy_surf.get_rect(center=(window_width/2,window_height*.45))

while not keys[pg.K_SPACE]:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            waves.close()
            pg.quit()
            sys.exit()
    screen.blit(intro_bg, (0, 0))
    screen.blit(title, title.get_rect(center=(window_width/2, window_height*.375)))
    screen.blit(prompt, prompt.get_rect(center=(window_width/2, .65*window_height)))
    pg.display.update()
    clock.tick(60)
    keys = pg.key.get_pressed()
    last_laser_timer = pg.time.get_ticks() #restart the shot cooldown   
    dt = 0
    start_time=pg.time.get_ticks()

def game_over():                           # added: the outro, used by both ways of losing the last life
    outro_bg = pg.transform.smoothscale(pg.image.load('Galaxy_background_black.PNG').convert(), screen.get_size()) 
    title = pg.font.Font(None, int(72*window_width/800)).render('Good Game Engineer', True, 'white') 
    score_after = pg.font.Font(None, int(72*window_width/800)).render(f'Score: {score}    Time: {round((end_time - start_time)/1000,4)}', True, 'white') 
    prompt = pg.font.Font(None, int(32*window_width/400)).render('Press Space to Restart', True, 'white') 
    while pg.key.get_pressed()[pg.K_SPACE]:
        pg.event.pump()                        
    while not pg.key.get_pressed()[pg.K_SPACE]:   # adjusted: read the keyboard fresh each time, so pressing SPACE ends the game                                           
        for event in pg.event.get():                                              
            if event.type == pg.QUIT: 
                waves.close()                                         
                pg.quit()                                                        
                sys.exit()                                                         
        screen.blit(outro_bg, (0, 0))  # adjusted: was intro_bg                                            
        screen.blit(title, title.get_rect(center=(window_width/2, window_height*.375)))
        screen.blit(score_after, score_after.get_rect(center=(window_width/2, .5*window_height)))                 
        screen.blit(prompt, prompt.get_rect(center=(window_width/2, .625*window_height)))                 
        pg.display.update()                                                          
        clock.tick(60)
    reset_game()
    return True

def reset_game():
    global score, lives, enemies, lasers, waves, last_laser_timer, dt, start_time, won, music_channel
    score = 0
    lives = Lives.Lives(scale=1*window_width/400)
    enemies = []
    lasers = []
    waves.seek(0)
    last_laser_timer = pg.time.get_ticks()   # blocks an instant shot
    dt = 0
    player.x_pos = window_width/2            # use your Player's attribute namesd
    start_time = pg.time.get_ticks()
    won=False
    winner_sound.stop()
    music_channel.unpause()
 
def progressWave(waves):
    line = waves.readline().rstrip("\r\n")
    line = list(line)
    if not line:
        return False
    while line[0] == "#":
        line = waves.readline().rstrip("\r\n")
        line = list(line)
    for i in range(len(line)):
        x_pos = window_width/(len(line)+1)*(i+1)
        if line[i] == "S":
            enemies.append(ShootingEnemy.ShootingEnemy(x_pos, y = 0, scale = 2*window_width/800, laser_time=1*800/window_height))
        elif line[i] == "E":
            enemies.append(Enemy.Enemy(x_pos, y = 0, scale = 5*window_width/800))
    return True

def winner():
    music_channel.pause()
    winner_sound.play(-1)
    title = pg.font.Font(None, int(72*window_width/800)).render('Congratulations!', True, 'white')
    stats = pg.font.Font(None, int(48*window_width/800)).render(f'Score: {score}    Time: {round((end_time - start_time)/1000,4)}', True, 'white')
    caption = pg.font.Font(None, int(48*window_width/800)).render('Try again? Press SPACE!', True, 'white')

    while pg.key.get_pressed()[pg.K_SPACE]:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waves.close()
                pg.quit()
                sys.exit()
        clock.tick(60)

    while not pg.key.get_pressed()[pg.K_SPACE]:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waves.close()
                pg.quit()
                sys.exit()
        screen.blit(intro_bg, (0, 0))
        screen.blit(title, title.get_rect(center=(window_width/2, window_height*.2)))
        screen.blit(trophy_surf, trophy_rect)
        screen.blit(stats, stats.get_rect(center=(window_width/2, window_height*.65)))
        screen.blit(caption, caption.get_rect(center=(window_width/2, window_height*.75)))
        pg.display.update()
        clock.tick(60)

    while pg.key.get_pressed()[pg.K_SPACE]:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waves.close()
                pg.quit()
                sys.exit()
        clock.tick(60)
    reset_game()
    return True
    
    
    
while True:
    #Basic Handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            waves.close()
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            full = pg.display.is_fullscreen()
            if event.key == pg.K_F11 or (event.key == pg.K_ESCAPE and full):
                pg.display.toggle_fullscreen()
    if game_active:
        #Player control section
        keys = pg.key.get_pressed()
        background.show(screen)
        
        if keys[pg.K_SPACE] and (pg.time.get_ticks()-last_laser_timer)/1000 > time_between_shot:
            laser_sound.play()
            laser = Laser.Laser(player.player_rect.centerx, player.player_rect.top, owner= player, scale=1*window_width/800)
            lasers.append(laser)
            last_laser_timer= pg.time.get_ticks()
        
        player.move(dt, keys, speed=500*window_width/800)
        
        #Game update section
        if not enemies:
            if not progressWave(waves):
                won= True
                game_active=False
                end_time = pg.time.get_ticks()
        
        for laser in lasers:
            laser.move(dt, speed_scale=50*window_height/800)
            laser.destroy()
            laser.update()
            if not isinstance(laser.owner, Player.Player) and laser.proj.colliderect(player.player_rect):   # added: an enemy laser hit the player
                laser.destroyed = True                      # added: the laser is used up, so it only costs one life
                lives.lose_life(1)                          # added: the player loses one life
            if laser.proj.top > window_height:              # added: enemy lasers that leave the bottom of the screen
                laser.destroyed = True                      # added: get cleaned up
            laser.show(screen)
        lasers = [laser for laser in lasers if not laser.destroyed]
        
        for enemy in enemies:
            if not isinstance(enemy,ShootingEnemy.ShootingEnemy):
                enemy.move(dt, v_x=0, v_y = 80*window_height/800)
            else:
                enemy.move(dt, v_x=0, v_y = 50*window_height/800)
            enemy.update()
            enemy.show(screen)
            if enemy.enemy_rect.bottom >= window_height:
                game_active=False
                end_time = pg.time.get_ticks()
                
            if isinstance(enemy, ShootingEnemy.ShootingEnemy):
                if (pg.time.get_ticks()-enemy.last_laser_timer)/1000 > enemy.laser_time:
                    enemy.last_laser_timer = pg.time.get_ticks()
                    lasers.append(enemy.shoot())   
            
            for laser in lasers: 
                score+=enemy.destroy(laser)
                laser.destroy(enemy)
                
            if enemy.enemy_rect.colliderect(player.player_rect):   # added: the enemy touched the player
                enemy.destroy()                                     # added: remove that enemy so it only costs one life
                lives.lose_life(1)    # added: the player loses one life
        
        if lives.out_of_lives():                    # added: no lives left
            game_active=False
            end_time = pg.time.get_ticks()
        enemies = [enemy for enemy in enemies if not enemy.destroyed]
        
        
        text = "Score: " + str(score)
        score_obj.update(text, screen)
        player.update()
        player.show(screen)
        lives.draw(screen)                         # added: draw the hearts in the top left
    else:
         game_active= winner() if won else game_over()
         
    pg.display.update()
    dt = clock.tick(60)/1000
