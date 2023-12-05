import pygame
from collections import namedtuple
from tile import Tile
from agent import Agent
import numpy as np
import pickle
import random

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

SPEED = 10


class Game:
    def __init__(self, w=1400, h=750, bs=50):
        # display params
        self.screen_width = w
        self.screen_height = h
        self.block_size = bs
        self.board_start = 50
        self.stats_width = 250

        self.width = int((w - self.board_start - self.stats_width))
        self.height = int((h - 2 * self.board_start))

        # init display
        self.display = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.game_board = pygame.surface.Surface(
            (self.width, self.height)
        ).convert()
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()

        self.tiles = []

        self.num_agents = 5
        self.agents = []
        # self.agent = Agent(
        #     self.block_size // 2 + 500, self.block_size // 2 + 250, "u"
        # )

        
        for _ in range(self.num_agents):
            new_agent = Agent(
            self.block_size // 2 + 500,
            self.block_size // 2 + 250,
            "u",
            WHITE
            )
            self.agents.append(new_agent)

        self._place_agents_randomly(
            self.board_start, self.board_start, self.width, self.height
        )
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
        pass
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
            print(f"Successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error loading from {file_path}: {e}")

    def move_left(self, agent):
        if agent.x - self.block_size <= 0:
            return
        else:
            for tile in self.tiles:  # @TODO: REVRITE
                if (
                    tile.rect.collidepoint(agent.x - self.block_size, agent.y)
                    and tile.solid
                ):
                    return
            agent.x -= self.block_size

    def move_right(self, agent):
        if agent.x + self.block_size > self.width:
            return
        else:
            for tile in self.tiles:  # @TODO: REVRITE
                if (
                    tile.rect.collidepoint(agent.x + self.block_size, agent.y)
                    and tile.solid
                ):
                    return
            agent.x += self.block_size

    def move_up(self, agent):
        if agent.y - self.block_size <= 0:
            return
        else:
            for tile in self.tiles:  # @TODO: REVRITE
                if (
                    tile.rect.collidepoint(agent.x, agent.y - self.block_size)
                    and tile.solid
                ):
                    return
            agent.y -= self.block_size

    def move_down(self, agent):
        if agent.y + self.block_size >= self.height:
            return
        else:
            for tile in self.tiles:  # @TODO: REVRITE
                if (
                    tile.rect.collidepoint(agent.x, agent.y + self.block_size)
                    and tile.solid
                ):
                    return
            agent.y += self.block_size

    def step_machine(self, sim_steps):
        for step in range(0, sim_steps):
            self.play_step()
            self.clock.tick(100)

    def play_step(self):
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

        for agent in self.agents:
            self._change_agent_color(agent)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_left(self.agent)
        elif keys[pygame.K_RIGHT]:
            self.move_right(self.agent)
        elif keys[pygame.K_UP]:
            self.move_up(self.agent)
        elif keys[pygame.K_DOWN]:
            self.move_down(self.agent)
        elif keys[pygame.K_s]:  # @TODO: do it properly
            self.save("pool")
        elif keys[pygame.K_q]:
            pygame.quit()
            quit()
        elif pygame.mouse.get_pressed()[0]:
            for tile in self.tiles:
                (x, y) = pygame.mouse.get_pos()
                if tile.rect.collidepoint((x - 50, y - 50)):
                    tile.change_solid()
        elif pygame.mouse.get_pressed()[2]:
            for tile in self.tiles:
                (x, y) = pygame.mouse.get_pos()
                if tile.rect.collidepoint((x - 50, y - 50)):
                    tile.change_not_solid()

        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        self._draw_background()
        self.display.blit(self.game_board, [50, 50])

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


if __name__ == "__main__":
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = Game(screen_width, screen_height)

    while True:
        game.play_step()

    pygame.quit()
