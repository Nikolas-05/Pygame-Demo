import pygame as pg
import math as m
import random as rand
import os
import sys

class Background:

    def __init__(self,width,height):
    
        self.background_sheet = pg.image.load("SpaceShooterAssetPack_BackGrounds.png").convert_alpha()
        self.base_surf, self.background_rect = Background.get_sprite(sheet=self.background_sheet,angle=0,x=128,y=93,width=128,height=256)
        self.background_surf = pg.transform.scale(self.base_surf, (width, height))
        
    def get_sprite(sheet,angle, x, y, width, height, scale=1):
        sprite=pg.Surface((width,height)).convert_alpha()
        sprite.blit(sheet,(0,0), (x,y,width,height))
        sprite=pg.transform.rotozoom(sprite,angle,scale)
        sprite_rect = sprite.get_rect()
        return sprite, sprite_rect
        
    def show(self, layer):
        layer.blit(self.background_surf,(0,0))