import pygame
import math as m
import random as rand
import os
import sys



class Laser:
    
    def __init__(self, x, y, owner, color = "red", speed = 10, scale = 1):
        
        self.x_pos = x
        self.y_pos = y
        self.destroy = False
        self.color = color
        self.speed = speed
        self.owner = owner
        self.scale = scale
        self.proj = pygame.Rect(x, y, 20, 60)
        
    def update(self):
        self.proj = pygame.Rect(self.x_pos, self.y_pos, 20, 60)
    
    def show(self, layer):
        pygame.draw.rect(layer, self.color, self.proj)
    
    def move(self, dt):
        """
        Pass the dt time clock into this

        """
        self.y_pos += self.speed*dt
    
    def destroy(self):
        """
        Marks a flag to have destroy = True, need to run .remove somewhere in main

        """
        self.destroy = True