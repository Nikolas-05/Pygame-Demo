import pygame as pg
import math as m
import random as rand
import os
import sys


class Player:

    def __init__(self, x = 0, y = 0, scale = 1):
        self.x_pos = x
        self.y_pos = y
        self.scale = scale
        self.player_sheet = pg.image.load("SpaceShooterAssetPack_Ships.png").convert_alpha()
        self.player_ship, self.player_rect = Player.get_sprite(self,sheet=self.player_sheet,angle=180,x=32,y=64,width=16,height=17,scale=self.scale)

    def update(self):
        self.player_rect.center = self.x_pos, self.y_pos
    
    def get_sprite(self,sheet,angle, x, y, width, height,scale=1):
        sprite=pg.Surface((width,height)).convert_alpha()
        sprite.blit(sheet,(0,0), (x,y,width,height))
        sprite=pg.transform.rotozoom(sprite,angle,self.scale)
        sprite_rect=sprite.get_rect(center=(self.x_pos,self.y_pos))
        return sprite, sprite_rect
    
    def show(self, layer):
        """
        Pygame draw on specified layer, default
        """
        layer.blit(self.player_ship,self.player_rect)
        
    def move(self, dt, key, speed = 500):
        if key[pg.K_LEFT] and self.player_rect.left >= 0:
            self.x_pos+=-speed*dt
        if key[pg.K_RIGHT] and self.player_rect.right<=800:
            self.x_pos+=speed*dt
        
class Laser:
    
    def __init__(self, x, y, owner, color = "red", speed = 10, scale = 1):
        
        self.x_pos = x
        self.y_pos = y
        self.destroyed = False
        self.color = color
        self.speed = speed
        self.owner = owner
        self.scale = scale
        self.proj = pg.Rect(0, 0, 5*self.scale, 30*self.scale)
        self.proj.midbottom= (self.x_pos,self.y_pos)
        
    def update(self):
        self.proj.midbottom = (self.x_pos, self.y_pos) 
        
    def show(self, layer):
        pg.draw.rect(layer, self.color, self.proj)
    
    def move(self, dt, speed_scale):
        """
        Pass the dt time clock into this

        """
        if self.owner==player:
            self.y_pos -= self.speed*dt*speed_scale
        else:
            self.y_pos += self.speed*dt*speed_scale
            
    def destroy(self):
        """
        Marks a flag to have destroy = True, need to run .remove somewhere in main, add enemy collision also

        """
        if self.owner==player:
            if self.proj.bottom < 0:
                self.destroyed = True
        
pg.init()

screen = pg.display.set_mode((800,800), pg.SCALED | pg.RESIZABLE)
clock = pg.time.Clock()

player = Player(x=400, y=700, scale=2)
dt = 0

lasers=[]

last_laser_timer=0
time_between_shot=.2

while True:
    dt = clock.tick(60)/1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            full = pg.display.is_fullscreen()
            if event.key == pg.K_F11 or (event.key == pg.K_ESCAPE and full):
                pg.display.toggle_fullscreen()
            if event.key == pg.K_SPACE and (pg.time.get_ticks()-last_laser_timer)/1000 > time_between_shot:
                laser = Laser(player.player_rect.centerx, player.player_rect.top, owner=player)
                lasers.append(laser)
                last_laser_timer= pg.time.get_ticks()

    screen.fill('Black')
    
    keys = pg.key.get_pressed()
    
    player.move(dt, keys)
    player.update()
    player.show(screen)
    
    for laser in lasers:
        laser.move(dt, speed_scale=50)
        laser.destroy()
        laser.update()
        laser.show(screen)
    lasers = [laser for laser in lasers if not laser.destroyed]
    pg.display.update() 

