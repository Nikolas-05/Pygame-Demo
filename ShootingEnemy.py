import pygame as pg
import Laser
import Player
import Enemy

class ShootingEnemy(Enemy.Enemy):
    Sprite_location=(48,64,17,16)
    def __init__(self, x = 0, y = 0, scale = 1, laser_time = 0.5):
        super().__init__(x, y, scale)
        self.laser_time = laser_time
        self.last_laser_timer = 0
        self.explosion_sound = pg.mixer.Sound("explosion.mp3")
        self.explosion_sound.set_volume(0.6)
        
    def shoot(self,window_height=800):
        return Laser.Laser(self.enemy_rect.centerx, self.enemy_rect.bottom, owner = Enemy, color = "green")
    
    def destroy(self, laser = None):
        """
        Marks a flag to have destroy = True, need to run .remove somewhere in main, add enemy collision also

        """
        if laser != None:
            if isinstance(laser, Laser.Laser):
                if isinstance(laser.owner, Player.Player) and laser.proj.colliderect(self.enemy_rect):
                    self.destroyed = True
                    self.explosion_sound.play()
                    return 2
        else:
            self.destroyed = True
            self.explosion_sound.play()
        return 0
        
