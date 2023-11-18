import pygame
from collections import namedtuple
from tile import Tile
import numpy as np

pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

    
Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

SPEED = 500

class Agent:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Game:
    
    def __init__(self, w=1400, h=750, bs=20):
        #display params
        self.screen_width = w
        self.screen_height = h
        self.block_size = bs

        self.width = int((w-100))
        self.height = int((h-100))

        # init display
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_board = pygame.surface.Surface((self.width, self.height)).convert()
        pygame.display.set_caption('Game')
        self.clock = pygame.time.Clock()

        self.tiles = []
        self.agent = Agent(self.block_size//2, self.block_size//2)
        self.setup()

    def setup(self):
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                self.tiles.append(Tile(False, self.block_size, x, y))

    def move_left(self, agent):
        if (agent.x - self.block_size <= 0):
            return
        else:
            for tile in self.tiles: #@TODO: REVRITE
                if tile.rect.collidepoint(agent.x- self.block_size, agent.y) and tile.solid: 
                    return
            agent.x -= self.block_size

    def move_right(self, agent):
        if (agent.x + self.block_size > self.width):
            return
        else:
            for tile in self.tiles: #@TODO: REVRITE
                if tile.rect.collidepoint(agent.x +self.block_size, agent.y) and tile.solid:
                    return
            agent.x += self.block_size

    def move_up(self, agent):
        if (agent.y- self.block_size <= 0):
            return
        else:
            for tile in self.tiles: #@TODO: REVRITE
                if tile.rect.collidepoint(agent.x, agent.y- self.block_size) and tile.solid: 
                    return
            agent.y -= self.block_size

    def move_down(self, agent):
        if (agent.y + self.block_size >= self.height):
            return
        else:
            for tile in self.tiles: #@TODO: REVRITE
                if tile.rect.collidepoint(agent.x, agent.y + self.block_size) and tile.solid:
                    return
            agent.y += self.block_size


    def play_step(self):
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left(self.agent)
                elif event.key == pygame.K_RIGHT:
                    self.move_right(self.agent)
                elif event.key == pygame.K_UP:
                    self.move_up(self.agent)
                elif event.key == pygame.K_DOWN:
                    self.move_down(self.agent)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            elif pygame.mouse.get_pressed()[0]:
                for tile in self.tiles:
                    (x, y) = pygame.mouse.get_pos()
                    if tile.rect.collidepoint((x-50, y-50)):
                        tile.change_solid()
                
        self._update_ui()
        self.clock.tick(SPEED)
        
        # 6. return game over and score
        return False
    
        
    def _update_ui(self):
        self.display.fill(BLACK)
        self.drawBackground()
        self.display.blit(self.game_board, [50, 50])

        pygame.display.flip()

    def drawBackground(self):
        for tile in self.tiles:
            pygame.draw.rect(self.game_board, tile.color, tile.rect)
        for x in range(0,   self.width, self.block_size):
            pygame.draw.line(self.game_board, (255, 255, 255, 0), (x, 0), ( x,  self.height))
        for y in range(0,  self.height, self.block_size):
            pygame.draw.line(self.game_board, (255, 255, 255, 20), (0, y), ( self.width, y))
        pygame.draw.circle(self.game_board, BLACK, (self.agent.x, self.agent.y), self.block_size//4)   

if __name__ == '__main__':
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = Game(screen_width, screen_height)

    while True:
        game.play_step()

    pygame.quit()
