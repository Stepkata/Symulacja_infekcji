import pygame
from collections import namedtuple
from tile import Tile
from agent import Agent
import numpy as np
import pickle

pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

    
Point = namedtuple('Point', 'x, y')
TilePoint = namedtuple('TilePoint', 'position, solid')

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN=(0,255,0)

SPEED = 100

class GameLevelCreator:
    
    def __init__(self, w=1400, h=750, bs=50):
        #display params
        self.screen_width = w
        self.screen_height = h
        self.block_size = bs
        self.board_start = 50
        self.stats_width = 250
        self.num_agents = 10

        self.width = int((w-self.board_start-self.stats_width))
        self.height = int((h-2*self.board_start))


        # init display
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_board = pygame.surface.Surface((self.width, self.height)).convert()
        self.toolbar = pygame.surface.Surface((self.stats_width, self.height)).convert()
        pygame.display.set_caption('GameLevelCreator')
        self.clock = pygame.time.Clock()

        self.bs_button_up = pygame.Rect(self.screen_width-140, 100, 30, 20)
        self.bs_button_up_hover = False
        self.bs_button_down = pygame.Rect(self.screen_width-140, 130, 30, 20)
        self.bs_button_down_hover = False

        self.na_button_up = pygame.Rect(self.screen_width-140, 180, 30, 20)
        self.na_button_up_hover = False
        self.na_button_down = pygame.Rect(self.screen_width-140, 210, 30, 20)
        self.na_button_down_hover = False

        self.draw = pygame.Rect(self.screen_width-100, 260, 50, 50)

        self.erase = pygame.Rect(self.screen_width-100, 340, 50, 50)

        self.create_check = pygame.Rect(self.screen_width-100, 420, 50, 50)

        self.save_btn = pygame.Rect(self.screen_width-100, 480, 50, 50)
        self.save_btn_hover = False

        self.wall_state = 0

        self.tiles = []
        self._setup()

    def _setup(self):
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                self.tiles.append(Tile(False, self.block_size, x, y))

    def _get_game_state(self):
        return {
            "block_size": self.block_size,
            "layout": self.tiles
        }
    
    def get_map(self):
        map = []
        for tile in self.tiles:
            tile_point = TilePoint((tile.x, tile.y), 1 if tile.solid else 0)
            map.append(tile_point)
        map = np.reshape(map, (self.width//self.block_size+1, self.height//self.block_size+1, -1))
        return map

    def get_checkpoints(self):
        checkpoints = []
        for tile in self.tiles:
            if tile.checkpoint:
                checkpoints.append(Point(tile.x, tile.y))
        return checkpoints
    
    def save(self, savefile):
        file_path = "saves/"+savefile
        try:
            with open(file_path, 'wb') as file:
                # Serialize the necessary data using pickle
                save_data = {
                    'block_size' : self.block_size,
                    'tiles': self.tiles,
                    'num_agents': self.num_agents,
                    'map': self.get_map(),
                    'checkpoints': self.get_checkpoints()
                }
                pickle.dump(save_data, file)
            print(f'Successfully saved to {file_path}')
        except Exception as e:
            print(f'Error saving to {file_path}: {e}')

    def load(self, savefile):
        file_path = "saves/"+savefile
        try:
            with open(file_path, 'rb') as file:
                # Deserialize the data using pickle
                load_data = pickle.load(file)
                self.block_size = load_data.get('block_size', 10)
                self.tiles = load_data.get('tiles', [])
                self.num_agents = load_data.get('num_agents', 10)
            print(f'Successfully loaded from {file_path}')
        except Exception as e:
            print(f'Error loading from {file_path}: {e}')


    def play_step(self):
        self.bs_button_down_hover = self.bs_button_down.collidepoint(pygame.mouse.get_pos())
        self.bs_button_up_hover = self.bs_button_up.collidepoint(pygame.mouse.get_pos())
        self.na_button_down_hover = self.na_button_down.collidepoint(pygame.mouse.get_pos())
        self.na_button_up_hover = self.na_button_up.collidepoint(pygame.mouse.get_pos())
        self.save_btn_hover = self.save_btn.collidepoint(pygame.mouse.get_pos())

        if self.draw.collidepoint(pygame.mouse.get_pos()):
            self.wall_state = 0
        elif self.erase.collidepoint(pygame.mouse.get_pos()):
            self.wall_state = 1
        elif self.create_check.collidepoint(pygame.mouse.get_pos()):
            self.wall_state = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]: #@TODO: do it properly
            self.save("pool")
        elif keys[pygame.K_q]:
            pygame.quit()
            quit()
        elif pygame.mouse.get_pressed()[0]:
            for tile in self.tiles:
                (x, y) = pygame.mouse.get_pos()
                if tile.rect.collidepoint((x-50, y-50)):
                    if self.wall_state == 0:
                        tile.change_solid()
                    elif self.wall_state == 2:
                        tile.change_checkpoint()
                    else:
                        tile.change_not_solid()
            if self.bs_button_down.collidepoint(pygame.mouse.get_pos()):
                self._handle_bs_button_down()
            elif self.bs_button_up.collidepoint(pygame.mouse.get_pos()):
                self._handle_bs_button_up()
            if self.na_button_down.collidepoint(pygame.mouse.get_pos()):
                self._handle_na_button_down()
            elif self.na_button_up.collidepoint(pygame.mouse.get_pos()):
                self._handle_na_button_up()
            elif self.save_btn.collidepoint(pygame.mouse.get_pos()):
                self.save("test")

        elif pygame.mouse.get_pressed()[2]:
            for tile in self.tiles:
                (x, y) = pygame.mouse.get_pos()
                if tile.rect.collidepoint((x-50, y-50)):
                    tile.change_not_solid()
                
        self._update_ui()
        self.clock.tick(SPEED)
        
        # 6. return game over and score
        return False
    
    def _handle_bs_button_up(self):
        self.block_size += 5
        self._setup()

    def _handle_bs_button_down(self):
        if self.block_size > 5:
            self.block_size -= 5
            self._setup()

    def _handle_na_button_up(self):
        self.num_agents += 1

    def _handle_na_button_down(self):
        if self.num_agents > 2:
            self.num_agents -= 1
    
    def _render_text(self, surface, text, font_size, position, color):
        font = pygame.font.Font(None, font_size)
        text_render = font.render(text, True, color)
        surface.blit(text_render, position)
        
    def _update_ui(self):
        self.display.fill(BLACK)
        self._draw_background()
        self.display.blit(self.game_board, [self.board_start, self.board_start])
        self._draw_toolbar()
        self.display.blit(self.toolbar, [self.screen_width-self.stats_width, 0])
        self._draw_clickable_buttons()

        pygame.display.flip()

    def _draw_background(self):
        for tile in self.tiles:
            pygame.draw.rect(self.game_board, tile.color, tile.rect)
        for x in range(0,   self.width, self.block_size):
            pygame.draw.line(self.game_board, (255, 255, 255, 0), (x, 0), ( x,  self.height))
        for y in range(0,  self.height, self.block_size):
            pygame.draw.line(self.game_board, (255, 255, 255, 20), (0, y), ( self.width, y))

    def _draw_toolbar(self):
        pygame.draw.rect(self.toolbar, WHITE, pygame.Rect(30, 100, 70, 50) )
        self._render_text(self.toolbar, str(self.block_size), 40, (50, 115), BLACK)
        pygame.draw.rect(self.toolbar, WHITE, pygame.Rect(30, 180, 70, 50) )
        self._render_text(self.toolbar, str(self.num_agents), 40, (50, 195), BLACK)

    def _draw_clickable_buttons(self):
        self._render_text(self.display, "Tile size", 30, (self.screen_width-200, 70), WHITE)
        pygame.draw.rect(self.display, WHITE if self.bs_button_up_hover else BLUE1, self.bs_button_up )
        pygame.draw.rect(self.display, WHITE if self.bs_button_down_hover else BLUE1, self.bs_button_down )
        self._render_text(self.display, "Number of agents", 30, (self.screen_width-200, 160), WHITE)
        pygame.draw.rect(self.display, WHITE if self.na_button_up_hover else BLUE1,   self.na_button_up )
        pygame.draw.rect(self.display, WHITE if self.na_button_down_hover else BLUE1, self.na_button_down )

        self._render_text(self.display, "Wall", 30, (self.screen_width-230, 280), WHITE)
        pygame.draw.rect(self.display, RED, self.draw)
        self._render_text(self.display, "Erase all", 30, (self.screen_width-230, 360), WHITE)
        pygame.draw.rect(self.display, BLUE2, self.erase)
        self._render_text(self.display, "Checkpoint", 30, (self.screen_width-230, 440), WHITE)
        pygame.draw.rect(self.display, GREEN, self.create_check)

        self._render_text(self.display, "Save", 30, (self.screen_width-230, 500), WHITE)
        pygame.draw.rect(self.display, GREEN, self.save_btn)


        

if __name__ == '__main__':
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = GameLevelCreator(screen_width, screen_height)

    while True:
        game.play_step()

    pygame.quit()
