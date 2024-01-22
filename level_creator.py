import pygame
from collections import namedtuple
from tile import Tile
from agent import Agent
import numpy as np
import pickle
from button import Button 

pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

    
Point = namedtuple('Point', 'x, y')


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

        self.h = int(self.height/self.block_size)
        self.w = int(self.width/self.block_size)


        # init display
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_board = pygame.surface.Surface((self.width, self.height)).convert()
        self.toolbar = pygame.surface.Surface((self.stats_width, self.height)).convert()
        pygame.display.set_caption('GameLevelCreator')
        self.clock = pygame.time.Clock()

        self.buttons = [
            Button("Block size", self.screen_width-140, 100, 30, 20, BLUE1),
            Button("Block_size_down", self.screen_width-140, 130, 30, 20, BLUE1, False),
            Button("Agents num", self.screen_width-140, 180, 30, 20, BLUE1),
            Button("Agents_num_down", self.screen_width-140, 210, 30, 20, BLUE1, False),
            Button("Draw", self.screen_width-180, 280, 50, 50, RED),
            Button("Erase", self.screen_width-180, 370, 50, 50, BLUE2),
            Button("Create_check", self.screen_width-180, 460, 50, 50, GREEN),
            Button("Save", self.screen_width-180, 550, 50, 50, RED),
        ]

        self.button_actions = {
            self.buttons[0]: self._handle_bs_button_up,
            self.buttons[1]:self._handle_bs_button_down,
            self.buttons[2]:self._handle_na_button_up,
            self.buttons[3]:self._handle_na_button_down,
            self.buttons[4]:self._handle_draw,
            self.buttons[5]:self._handle_erase,
            self.buttons[6]:self._handle_check,
            self.buttons[7]:self._handle_save
        }

        #Przycisk powrotu do menu
        self.return_to_main_menu = False
        self.buttons.append(Button("Return to Menu", self.screen_width-180, 640, 150, 50, GREEN))
        self.button_actions[self.buttons[-1]] = self._handle_return_to_main_menu

        self.wall_state = 0

        self.tiles = np.empty((self.w, self.h), dtype=object)
        self.checkpoints = []
        self._setup()

    def _handle_return_to_main_menu(self):
        print("returning to main menu")
        self.return_to_main_menu = True

    def _setup(self) -> None:
        self.h = int(self.height/self.block_size)+1
        self.w = int(self.width/self.block_size)+1
        self.tiles = np.empty((self.w, self.h), dtype=object)
        for x in range(0, self.w):
            for y in range(0, self.h):
                self.tiles[x,y] = Tile(False, self.block_size, x*self.block_size, y*self.block_size)

    def get_checkpoints(self) -> []:
        checkpoints = []
        for row in self.tiles:
            for tile in row:
                if tile.checkpoint:
                    checkpoints.append(Point(tile.x, tile.y))
        return checkpoints
    
    def save(self, savefile):
        file_path = "saves/"+savefile+".dat"
        try:
            save_data = {
                'block_size' : self.block_size,
                'num_agents': self.num_agents,
                'tiles': self.tiles,
                'checkpoints': self.get_checkpoints()
            }
            np.save(file_path, save_data, allow_pickle=True)
            print(f'Successfully saved to {file_path}')
        except Exception as e:
            print(f'Error saving to {file_path}: {e}')

    def load(self, savefile):
        file_path = "saves/"+savefile+".dat.npy"
        try:
            load_data = np.load( file_path ,  allow_pickle=True)
            print(load_data[()]['block_size'])
            self.block_size = load_data[()]['block_size']
            self.h = int(self.height/self.block_size)+1
            self.w = int(self.width/self.block_size)+1
            self.tiles = load_data[()]['tiles']
            self.num_agents = load_data[()]['num_agents']
            self.checkpoints =load_data[()]['checkpoints']
            print(f'Successfully loaded from {file_path}')
        except Exception as e:
            print(f'Error loading from {file_path}: {e}')


    def play_step(self):

        for button in self.buttons:
            button.is_hovering(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.save("pool")
        elif keys[pygame.K_q]:
            pygame.quit()
            quit()
        elif pygame.mouse.get_pressed()[0]:
            (x, y) = pygame.mouse.get_pos()
            x, y = int((x-50)/self.block_size), int((y-50)/self.block_size)
            if (x < self.w and y < self.h):
                tile = self.tiles[x, y]
                if self.wall_state == 0:
                    tile.change_solid()
                elif self.wall_state == 2:
                    tile.change_checkpoint()
                else:
                    tile.change_not_solid()
            for button in self.buttons:
                if (button.hover):
                    self.button_actions[button]()
     
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

    def _handle_draw(self):
        self.wall_state = 0
    
    def _handle_erase(self):
        self.wall_state = 1
    
    def _handle_check(self):
        self.wall_state = 2

    def _handle_save(self):
        self.save("test")
    
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
        for row in self.tiles:
            for tile in row:
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
        for button in self.buttons:
            pygame.draw.rect(self.display, button.color, button.rect)
            self.display.blit(button.name, button.name_position)


        

if __name__ == '__main__':
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = GameLevelCreator(screen_width, screen_height)

    while True:
        game.play_step()

    pygame.quit()
