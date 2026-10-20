import pygame as pg
import sys
class Player:
"""
Initialize before the while loop
player = Player(x=400, y=700, scale=2)
dt = 0
player_sheet = pg.image.load("SpaceShooterAssetPack_Ships.png").convert_alpha()
In the while loop:
    keys = pg.key.get_pressed()
    player.get_sprite(player_sheet,180,32,64,16,16)
    player.update()
    player.show(screen)
    player.move(dt, keys)
    dt = clock.tick(60)/1000
"""
    def __init__(self, x = 0, y = 0, scale = 1):
        self.x_pos = x
        self.y_pos = y
        self.scale = scale
        
    def update(self):
        scale = self.scale
        self.player_rect = pg.Rect(scale*self.x_pos, scale*self.y_pos, 200*scale, 50*scale)
    
    def get_sprite(self,sheet,angle, x, y, width, height,scale=1):
        sprite=pg.Surface((width,height)).convert_alpha()
        sprite.blit(sheet,(0,0), (x,y,width,height))
        sprite=pg.transform.rotozoom(sprite,angle,self.scale)
        sprite_rect=sprite.get_rect(center=(self.x_pos,self.y_pos))
        return sprite, sprite_rect
    
    def show(self, layer):
        """
        Pygame draw on specified layer, default
        """
        player_ship, self.player_rect = self.get_sprite(player_sheet, 180, x=32, y=64, width=16, height=17, scale=self.scale)
        layer.blit(player_ship,self.player_rect)
        return player_sheet
        
    def move(self, dt, key, speed = 500):
        if key[pg.K_LEFT]:
            self.x_pos+=-speed*dt
        if key[pg.K_RIGHT]:
            self.x_pos+=speed*dt
