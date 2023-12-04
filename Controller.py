import pygame
import random


class IndividualController:
    def __init__(self, agent):
        self.agent = agent
        pass

    def _step(self):
        rand_dir = random.randint(1, 4)
        if rand_dir == 1:
            self.agent.x += 50
        elif rand_dir == 2:
            self.agent.y += 50
        elif rand_dir == 3:
            self.agent.x -= 50
        elif rand_dir == 4:
            self.agent.y -= 50


class CrowdController:
    def __init__(self, agents_array):
        self.agents_array = agents_array

    def step(self):
        pass
