import pygame as pg
import math as m
import random as rand
import os
import sys

class Player:

    def __init__(self, x = 0, y = 0, scale = 1):
        self.x_pos = x
        self.y_pos = y
        self.color = 'red'
        #Create player "image"
        self.scale = scale
        self.leftblock = pg.Rect(scale*(x-50), scale*(y-100), 50*scale, 100*scale)
        self.baseblock = pg.Rect(scale*x, scale*y, 200*scale, 50*scale)
        self.rightblock = pg.Rect(scale*(x+200), scale*(y-100), 50*scale, 100*scale)
        self.frontblock = pg.Rect(scale*(x+75), scale*(y-200), 50*scale, 200*scale)
        
    def update(self):
        scale = self.scale
        self.leftblock = pg.Rect(scale*(self.x_pos-50), scale*(self.y_pos-100), 50*scale, 100*scale)
        self.baseblock = pg.Rect(scale*self.x_pos, scale*self.y_pos, 200*scale, 50*scale)
        self.rightblock = pg.Rect(scale*(self.x_pos+200), scale*(self.y_pos-100), 50*scale, 100*scale)
        self.frontblock = pg.Rect(scale*(self.x_pos+75), scale*(self.y_pos-200), 50*scale, 200*scale)
    
    
    def show(self, layer):
        """
        Pygame draw on specified layer, default
        """
        pg.draw.rect(layer, self.color, self.leftblock)
        pg.draw.rect(layer, self.color, self.rightblock)
        pg.draw.rect(layer, self.color, self.baseblock)
        pg.draw.rect(layer, self.color, self.frontblock)
        
    def move(self, dt, key, speed = 500):
        if key[pg.K_LEFT]:
            self.x_pos+=-speed*dt
        if key[pg.K_RIGHT]:
            self.x_pos+=speed*dt
            
