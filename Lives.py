# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:08:10 2026

@author: ramir
"""



import pygame as pg

class Lives:

    def __init__(self, start_lives=3, max_lives=10, scale=1):
        self.max_lives = max_lives
        self.scale = scale
        self.lives = start_lives
        self.regen_timer = 0
        self.explosion_sound = pg.mixer.Sound("explosion.mp3")
        self.explosion_sound.set_volume(0.6)

        img = pg.image.load('heart.png').convert_alpha()
        w, h = img.get_size()
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        self.heart = pg.transform.scale(img, new_size)   # scale once, not every frame

        self.margin = int(10 * scale) 
        self.gap = int(4 * scale)

    def lose_life(self, count=1):
        self.lives = max(0, self.lives - count)
        self.explosion_sound.play()

    def add_life(self):
        # never more than the full row of hearts
        self.lives = min(self.lives + 1, self.max_lives)

    def out_of_lives(self):
        return self.lives <= 0

    def draw(self, screen):
        for i in range(self.lives):
            x = self.margin + i * (self.heart.get_width() + self.gap)
            screen.blit(self.heart, (x, self.margin))