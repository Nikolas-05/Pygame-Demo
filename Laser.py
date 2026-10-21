import pygame as pg
import math as m
import random as rand
import os
import sys
from Player import *
class Laser:
    """
    add in code
                if event.key == pg.K_SPACE and (pg.time.get_ticks()-last_laser_timer)/1000 > time_between_shot:
                    laser = Laser(player.player_rect.centerx, player.player_rect.top, owner=player)
                    lasers.append(laser)
                    last_laser_timer= pg.time.get_ticks()
    in while loop
        for laser in lasers:
            laser.move(dt, speed_scale=50)
            laser.destroy()
            laser.update()
            laser.show(screen)
        lasers = [laser for laser in lasers if not laser.destroyed]
    """
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
        if self.owner=="player":
            self.y_pos -= self.speed*dt*speed_scale
        else:
            self.y_pos += self.speed*dt*speed_scale
            
    def destroy(self):
        """
        Marks a flag to have destroy = True, need to run .remove somewhere in main, add enemy collision also

        """
        if isinstance(self.owner, Player):
            if self.proj.bottom < 0:
                self.destroyed = True
