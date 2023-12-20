import pygame
from collections import namedtuple
from tile import Tile
from agent import Agent
import numpy as np
import pickle
import random
from infectionSpread import InfectionSpread

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont("arial", 25)


Point = namedtuple("Point", "x, y")

WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class Game:
    def __init__(self, w=1400, h=750, bs=50):
        # display params
        self.screen_width = w
        self.screen_height = h
        self.block_size = bs
        self.board_start = 50
        self.stats_width = 250

        self.speed = 100
        self.old_speed = 0

        self.width = int((w - self.board_start - self.stats_width))
        self.height = int((h - 2 * self.board_start))

        # init display
        self.display = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.game_board = pygame.surface.Surface(
            (self.width, self.height)
        ).convert()
        self.toolbar = pygame.surface.Surface(
            (self.stats_width, self.height)
        ).convert()
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()

        self.tiles = []
        self.sp_button_up = pygame.Rect(self.screen_width-140, 100, 30, 20)
        self.sp_button_up_hover = False
        self.sp_button_down = pygame.Rect(self.screen_width-140, 130, 30, 20)
        self.sp_button_down_hover = False
        self.stop_button = pygame.Rect(self.screen_width-180, 180, 80, 30)
        self.stop_button_hover = False

        #Ilość agentów
        self.num_agents = 10
        #Agenci
        self.agents = []
        #Zainfekopwani agenci
        self.infected_agents = []
        #Czas do iinfekcji
        self.time = 0
        # self.agent = Agent(
        #     self.block_size // 2 + 500, self.block_size // 2 + 250, "u"
        # )

        #ID agentow
        self.agent_id = 0

        infected_agent = Agent(
            self.agent_id,
            self.block_size // 2 + 500,
            self.block_size // 2 + 250,
            "u",
            RED,
            True
        )
        self.agents.append(infected_agent)
        self.infected_agents.append(infected_agent)
        
        self.agent_id += 1
        
        for _ in range(self.num_agents):
            new_agent = Agent(
                self.agent_id,
                self.block_size // 2 + 500,
                self.block_size // 2 + 250,
                "u",
                WHITE,
                False
            )
            self.agents.append(new_agent)
            self.agent_id += 1

        self._place_agents_randomly(
            self.board_start, self.board_start, self.width, self.height
        )

        self.infection_spread = InfectionSpread(self.block_size)
        self._setup()

    def _place_agents_randomly(self, start_x, start_y, end_x, end_y):
        squares = []
        for x in range(start_x + self.block_size // 2, end_x, self.block_size):
            for y in range(start_y + self.block_size // 2, end_y, self.block_size):
                squares.append((x, y))

        for agent in self.agents:
            selected_square = random.choice(squares)
            agent.x, agent.y = selected_square
            squares.remove(selected_square)

    def _change_agent_color(self, agent):
        if agent in self.infected_agents:
            agent.color = RED


    def _setup(self):
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                self.tiles.append(Tile(False, self.block_size, x, y))

    def _get_game_state(self):
        return {"block_size": self.block_size, "layout": self.tiles}

    def save(self, savefile):
        file_path = "saves/" + savefile
        try:
            with open(file_path, "wb") as file:
                # Serialize the necessary data using pickle
                save_data = {
                    "block_size": self.block_size,
                    "tiles": self.tiles,
                }
                pickle.dump(save_data, file)
            print(f"Successfully saved to {file_path}")
        except Exception as e:
            print(f"Error saving to {file_path}: {e}")

    def load(self, savefile):
        file_path = "saves/" + savefile
        try:
            with open(file_path, "rb") as file:
                # Deserialize the data using pickle
                load_data = pickle.load(file)
                self.block_size = load_data.get("block_size", 10)
                self.tiles = load_data.get("tiles", [])
                self.num_agents = load_data.get('num_agents', 10)
            print(f"Successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error loading from {file_path}: {e}")


    def step_machine(self, sim_steps):
        for step in range(0, sim_steps):
            self.play_step()
            self.clock.tick(100)

    def play_step(self):
        self.sp_button_down_hover = self.sp_button_down.collidepoint(pygame.mouse.get_pos())
        self.sp_button_up_hover = self.sp_button_up.collidepoint(pygame.mouse.get_pos())
        self.stop_button_hover = self.stop_button.collidepoint(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                quit()

        if pygame.mouse.get_pressed()[0]:
                if self.sp_button_down.collidepoint(pygame.mouse.get_pos()):
                    self._handle_sp_button_down()
                elif self.sp_button_up.collidepoint(pygame.mouse.get_pos()):
                    self._handle_sp_button_up()
                elif self.stop_button.collidepoint(pygame.mouse.get_pos()):
                    self._handle_stop()

        
        if self.speed > 0:
            sim_mode = 1
            # if sim_mode:
            #     self.agent._run_controller()
            if sim_mode:
                for agent in self.agents:
                    agent._set_agents_array(self.agents)
                    agent._set_dimensions(
                        self.width, self.height, self.block_size
                    )
                    agent._run_controller()

            #Zbieranie sąsiadów 
            for infected_agent in self.infected_agents:
                self.infection_spread._get_neighbors(infected_agent, self.agents)


            #Do wyznaczania zainfekowanych 
            self.time +=1
            if self.time % 10 == 0:
                self.time = 0 
                new_infected_agents = []
                for infected_agent in self.infected_agents:
                    new_infected_agents += self.infection_spread._spread_infection( 0.8)
                
                for new_infected_agent in new_infected_agents:
                    self.infected_agents.append(new_infected_agent)
        

            #Zmiana koloru zainfekowanych
            for agent in self.agents:
                self._change_agent_color(agent)

        self._update_ui()
        self.clock.tick(self.speed)
        return False
    
    def _handle_sp_button_up(self):
        if self.speed < 400:
            self.speed += 5

    def _handle_sp_button_down(self):
        if self.speed > 5:
            self.speed -= 5

    def _handle_stop(self):
        self.speed = 0

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
        for x in range(0, self.width, self.block_size):
            pygame.draw.line(
                self.game_board, (255, 255, 255, 0), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.block_size):
            pygame.draw.line(
                self.game_board, (255, 255, 255, 20), (0, y), (self.width, y)
            )
        # pygame.draw.circle(
        #     self.game_board,
        #     WHITE,
        #     (self.agent.x, self.agent.y),
        #     self.block_size // 4,
        # )
        for agent in self.agents:
            pygame.draw.circle(
                self.game_board,
                agent.color,
                (agent.x, agent.y),
                self.block_size // 4,
            )
    
    def _draw_toolbar(self):
        pygame.draw.rect(self.toolbar, WHITE, pygame.Rect(30, 100, 70, 50) )
        self._render_text(self.toolbar, str(self.speed), 40, (50, 115), BLACK)

    def _draw_clickable_buttons(self):
        pygame.draw.rect(self.display, WHITE if self.sp_button_up_hover else BLUE1, self.sp_button_up )
        pygame.draw.rect(self.display, WHITE if self.sp_button_down_hover else BLUE1, self.sp_button_down )
        pygame.draw.rect(self.display, RED if self.stop_button_hover else BLUE1, self.stop_button)




if __name__ == "__main__":
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = Game(screen_width, screen_height)

    while True:
        game.play_step()

    pygame.quit()
