import pygame as pg
import Laser
import Player
import Enemy

class ShootingEnemy(Enemy.Enemy):
    
    def __init__(self, x = 0, y = 0, scale = 1, laser_time = 0.5):
        super().__init__(x, y, scale)
        self.laser_time = laser_time
        self.last_laser_timer = 0
        
    def shoot(self):
        return Laser.Laser(self.enemy_rect.centerx, self.enemy_rect.top, owner = Enemy, color = "green")
        