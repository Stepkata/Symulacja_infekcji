import pygame 
from collections import namedtuple

WHITE = (255,255,255)
Point = namedtuple('Point', 'x, y')

class Button:
    def __init__(self, name:str, x:int, y:int, w:int, h:int, color:tuple, render_name:bool = True) -> None:
        self.font_size = 40
        self.font = pygame.font.Font(None, self.font_size)
        self.name = self.font.render(name if render_name else "", True, WHITE)
        self.name_position = Point(x-60, y-self.font_size+10)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.default_color = color
        self.hover = False

    def is_hovering(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.color = WHITE if self.hover else self.default_color

    


