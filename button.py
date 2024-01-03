import pygame 

WHITE = (255,255,255)

class Button:
    def __init__(self, x:int, y:int, w:int, h:int, color:tuple, f:function) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.default_color = color
        self.fun = f
        self.hover = False

    def is_hovering(self, mouse_pos):
        self.hover = self.rect(mouse_pos)
        self.color = WHITE if self.hover else self.default_color

    def activate(self):
        self.fun()


