import pygame as pg

class Score:
    
    def __init__(self, x, y, font, size):
        self.x_pos = x
        self.y_pos = y
        self.size = size
        self.obj = pg.font.Font(None, self.size)
        
    def update(self, text, screen):
        printed = self.obj.render(text, True, (255,255,255))
        screen.blit(printed, (self.x_pos, self.y_pos))