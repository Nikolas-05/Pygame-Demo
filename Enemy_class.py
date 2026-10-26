"""
Created on Tue Oct 20 18:18:06 2026

@author: ramir
"""

import pygame as pg
import math as m
import random as r
import Lasers                  # added: so enemies can fire Laser objects

ENEMY_WIDTH = 30


class Enemy(pg.sprite.Sprite):
    lasers = []                # added: one list shared by every enemy, so shots keep flying after the enemy dies

    def __init__(self, screen_width=800):
        super().__init__()
        image = pg.image.load('Demo_images/spaceship.PNG').convert_alpha()
        height = round(image.get_height() * ENEMY_WIDTH / image.get_width())
        image = pg.transform.smoothscale(image, (ENEMY_WIDTH, height))
        self.image = pg.transform.flip(image, False, True)     # point it down, toward the player
        self.screen_width = screen_width

        # starts just above the top of the screen at a random x
        self.x = r.randint(ENEMY_WIDTH, screen_width - ENEMY_WIDTH)
        self.y = -height
        self.rect = self.image.get_rect(midbottom=(self.x, 0))

        # every enemy gets its own random path: a fall speed, a sideways drift
        # and a side to side weave
        self.speed = r.uniform(1.5, 3.5)
        self.drift = r.uniform(-1, 1)
        self.weave_size = r.uniform(20, 80)
        self.weave_speed = r.uniform(0.02, 0.06)
        self.weave_timer = r.uniform(0, m.tau)
        self.turn_timer = r.randint(60, 180)
        self.shot_timer = r.randint(20, 120)       # added: frames until this enemy's first shot

    def move(self):
        self.y += self.speed
        self.x += self.drift
        self.weave_timer += self.weave_speed

        # every so often it picks a new drift, so no two paths look the same
        self.turn_timer -= 1
        if self.turn_timer <= 0:
            self.drift = r.uniform(-1.5, 1.5)
            self.turn_timer = r.randint(60, 180)

        # bounce off the sides of the screen
        if self.x < ENEMY_WIDTH or self.x > self.screen_width - ENEMY_WIDTH:
            self.drift = -self.drift
            self.x = max(ENEMY_WIDTH, min(self.x, self.screen_width - ENEMY_WIDTH))

        self.rect.centerx = round(self.x + m.sin(self.weave_timer) * self.weave_size)
        self.rect.bottom = round(self.y + self.rect.height)

    def update(self, screen_height=400):
        self.move()
        self.shot_timer -= 1                                       # added: count down to the next shot
        if self.shot_timer <= 0:                                   # added: time to shoot
            Enemy.lasers.append(Lasers.Laser(self.rect.centerx, self.rect.bottom + 30, owner=self, color='red', speed=8))  # added: red laser starting just under the ship, moving down
            self.shot_timer = r.randint(60, 150)                   # added: wait 1 to 2.5 seconds before shooting again
        if self.rect.top > screen_height:
            self.kill()
            
class Meteor(pg.sprite.Sprite):
    def __init__(self, screen_width=800):
        super().__init__()
        image = pg.image.load('Demo_images/Meteor.PNG').convert_alpha()
        height = round(image.get_height() * ENEMY_WIDTH / image.get_width())
        self.image = pg.transform.smoothscale(image, (ENEMY_WIDTH, height))
        self.screen_width = screen_width

        # starts just above the top of the screen at a random x
        self.x = r.randint(ENEMY_WIDTH, screen_width - ENEMY_WIDTH)
        self.y = -height
        self.rect = self.image.get_rect(midbottom=(self.x, 0))
        self.speed = r.uniform(1, 2)


    def move(self):
        self.y += self.speed
        self.rect.bottom = round(self.y + self.rect.height)

    def update(self, screen_height=400):
        self.move()
        if self.rect.top > screen_height:
            self.kill()
