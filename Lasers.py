# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:50:43 2026

@author: ramir
"""

import pygame as pg
import math as m
import random as rand
import os
import sys
import Player
import Enemy_class as Enemy

class Laser:
    def __init__(self, x, y, owner, color = "blue", speed = 20, scale = 1):
        
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

        if isinstance(self.owner, Player.Spaceship):
            self.y_pos -= self.speed*dt*speed_scale
        else:
            self.y_pos += self.speed*dt*speed_scale
            
    def destroy(self, enemy = None):

        if isinstance(self.owner, Player.Spaceship):
            if self.proj.bottom < 0:
                self.destroyed = True
                
        elif self.proj.top > pg.display.get_surface().get_height():   # added: enemy lasers are used up once they leave the bottom of the screen
            self.destroyed = True                                     # added
        if enemy != None and isinstance(enemy, Enemy.Enemy):
            if self.proj.colliderect(enemy.rect):
                    self.destroyed = True