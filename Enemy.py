import pygame as pg
import Laser
import Player

class Enemy:
    Sprite_location=(56,25,8,8)
    def __init__(self, x = 0, y = 0, scale = 1):
        self.x_pos = x
        self.y_pos = y
        self.scale = scale
        self.enemy_sheet = pg.image.load("SpaceShooterAssetPack_Ships.png").convert_alpha()
        sprite_x, sprite_y, width, height = self.Sprite_location
        self.enemy_ship, self.enemy_rect = Enemy.get_sprite(self,sheet=self.enemy_sheet,angle=0,x=sprite_x,y=sprite_y,width=width,height=height,scale=self.scale)
        self.destroyed = False

    def update(self):
        self.enemy_rect.center = self.x_pos, self.y_pos
    
    def get_sprite(self,sheet,angle, x, y, width, height,scale=1):
        sprite=pg.Surface((width,height), pg.SRCALPHA).convert_alpha()
        sprite.blit(sheet,(0,0), (x,y,width,height))
        sprite=pg.transform.rotozoom(sprite,angle,self.scale)
        sprite_rect=sprite.get_rect(center=(self.x_pos,self.y_pos))
        return sprite, sprite_rect
    
    def show(self, layer):
        """
        Pygame draw on specified layer, default
        """
        layer.blit(self.enemy_ship,self.enemy_rect)
        
    def move(self, dt, v_x=0, v_y =0):
            self.x_pos+=v_x*dt
            self.y_pos+=v_y*dt
            
    def destroy(self, laser = None):
        """
        Marks a flag to have destroy = True, need to run .remove somewhere in main, add enemy collision also

        """
        if laser != None:
            if isinstance(laser, Laser.Laser):
                if isinstance(laser.owner, Player.Player) and laser.proj.colliderect(self.enemy_rect):
                    self.destroyed = True
                    return 1
        else:
            self.destroyed = True
        return 0
