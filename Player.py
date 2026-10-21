import pygame as pg
import math as m
import random as rand
import os
import sys

class Player:
"""
need to add to main 
---
player = Player(x=400, y=700, scale=2)
dt = 0
---
in while loop
    keys = pg.key.get_pressed()
    
    player.move(dt, keys)
    player.update()
    player.show(screen)
    
    pg.display.update() 
"""
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
