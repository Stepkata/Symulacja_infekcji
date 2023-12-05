import pygame
import random


class IndividualController:
    def __init__(self, agent):
        self.agent = agent
        self.width = None
        self.height = None
        self.block_size = None
        self.agents_array = None
        pass

    def _step(self):
        if self.width is None or self.height is None or self.block_size is None or self.agents_array is None:
            raise ValueError("Wymiary planszy lub tablica agentów nie zostały ustawione")

        rand_dir = random.randint(1, 4)
        step_size = self.block_size

        new_x, new_y = self.agent.x, self.agent.y

        if rand_dir == 1:
            new_x = (self.agent.x + step_size) 
            if new_x > self.width:
                new_x = self.width - self.block_size // 2
        elif rand_dir == 2:
            new_y = (self.agent.y + step_size) 
            if new_y > self.height:
                new_y = self.height - self.block_size // 2
        elif rand_dir == 3:
            new_x = (self.agent.x - step_size) 
            if new_x <0:
                new_x = self.agent.x + step_size
        elif rand_dir == 4:
            new_y = (self.agent.y - step_size) 
            if new_y < 0:
                new_y = self.agent.y + step_size

    
        # Sprawdzenie kolizji z innymi agentami
        collides_with_other_agents = any(
            (
                agent != self.agent and
                new_x - self.block_size // 2 < agent.x < new_x + self.block_size // 2 and
                new_y - self.block_size // 2 < agent.y < new_y + self.block_size // 2
            )
            for agent in self.agents_array
        )

        if not collides_with_other_agents:
            self.agent.x, self.agent.y = new_x, new_y

    @staticmethod
    def is_within_screen_bounds(new_x, new_y, width, height, block_size):
        half_block_size = block_size // 2

        if new_x  < 0 or new_x + half_block_size > width:
            return False
        if new_y - half_block_size < 0 or new_y + half_block_size > height:
            return False
        
        return True
    
    def _set_dimensions(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size

    def _set_agents_array(self, agents_array):
        self.agents_array = agents_array
        

class CrowdController:
    def __init__(self, agents_array):
        self.agents_array = agents_array

    def step(self):
        pass
