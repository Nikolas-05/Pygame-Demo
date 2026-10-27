# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:08:10 2026

@author: ramir
"""



import pygame as pg

class Lives:

    def __init__(self, start_lives=3, max_lives=10): 
        self.max_lives = max_lives
        self.lives = start_lives
        self.regen_timer = 0
        self.heart = pg.image.load('heart.png').convert_alpha()

    def lose_life(self, count=1):
        self.lives = max(0, self.lives - count)

    def add_life(self):
        # never more than the full row of hearts
        self.lives = min(self.lives + 1, self.max_lives)

    def out_of_lives(self):
        return self.lives <= 0

    def draw(self, screen):
        for i in range(self.lives):
            screen.blit(self.heart,(10 + i * (self.heart.get_width() + 4), 10))