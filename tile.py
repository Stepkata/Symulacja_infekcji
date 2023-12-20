import pygame

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN=(0,255,0)


class Tile(): 
    def __init__(self, solid, size, x, y): 
        self.x = x
        self.y = y
        self.solid = solid
        self.checkpoint = False
        self.color = RED if self.solid else BLUE2
        self.rect = pygame.Rect(x, y, size, size) 
    
    def change_solid(self):
        self.solid = True
        self.checkpoint = False
        self.color = RED

    def change_not_solid(self):
        self.solid = False
        self.checkpoint = False
        self.color = BLUE2

    def change_checkpoint(self):
        self.checkpoint = True
        self.solid = False
        self.color = GREEN