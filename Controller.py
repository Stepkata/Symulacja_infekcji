import pygame
import random
from astar import Astar
from agent import Agent
from tile import Tile
import numpy as np
import math

class IndividualController:
    """A controller class to simulate random movement"""
    def __init__(self, width, height, block_size, tiles):
        self.agent = None
        self.width = width
        self.height = height
        self.block_size = block_size
        self.tiles = tiles

    def _step(self):
        if self.agent is None:
            raise ValueError("tablica agentów nie zostały ustawione")

        rand_dir = random.randint(1, 4)
        step_size = self.block_size

        new_x, new_y = self.agent.x, self.agent.y

        if rand_dir == 1:
            new_x = self.normalise(self.agent.x + step_size, self.width) 
        elif rand_dir == 2:
            new_y = self.normalise(self.agent.y + step_size, self.height) 
        elif rand_dir == 3:
            new_x = self.normalise(self.agent.x - step_size, self.width) 
        elif rand_dir == 4:
            new_y = self.normalise(self.agent.y - step_size, self.height) 

        collision = False
        x, y = int((new_x)/self.block_size), int((new_y)/self.block_size)
        (w, h) = self.tiles.shape
        if (x < w and y < h):
                tile = self.tiles[x, y]
                collision = tile.solid  
            
        if not collision:
            self.agent.x, self.agent.y = new_x, new_y
    
    def normalise(self, x, max):
        if x < 0:
            return self.block_size//2
        if x > max:
            return max - self.block_size//2
        return x
        

class CrowdController:
    def __init__(self, width, height, block_size, tiles):
        self.agents_array = None
        self.agent = None
        self.width = width
        self.height = height
        self.block_size = block_size
        self.tiles = tiles
        self.line_of_sight = 5*self.block_size

    def _step(self):
        if self.agent is None:
            raise ValueError("tablica agentów nie zostały ustawione")
        
        path = random.randint(1, 10)
        if path >= 4:
            self._go_radom()
        else:
            self.follow_nearest()

    def follow_nearest(self):
        to_follow = None
        distance = self.height*self.width
        for agent in self.agents_array:
            if (self.agent.x - self.line_of_sight <= agent.x <= self.agent.x + self.line_of_sight and 
                self.agent.y - self.line_of_sight <= agent.y <= self.agent.y + self.line_of_sight):
                dist_to_agent = self.get_distance(agent.x, agent.y)
                if (dist_to_agent < distance and dist_to_agent > 0):
                    to_follow = agent
                    distance = dist_to_agent
        if (to_follow is None):
            self._go_radom()
        else:
            new_x = self.normalise(self.agent.x + self.relu(self.agent.x, to_follow.x), self.width)
            new_y = self.normalise(self.agent.y + self.relu(self.agent.y, to_follow.y), self.height)
            if new_x == to_follow.x:
                new_x = self.agent.x
            if new_y == to_follow.y:
                new_y = self.agent.y
            collision = False
            x, y = int((new_x)/self.block_size), int((new_y)/self.block_size)
            (w, h) = self.tiles.shape
            if (x < w and y < h):
                    tile = self.tiles[x, y]
                    collision = tile.solid  
                
            if not collision:
                self.agent.x, self.agent.y = new_x, new_y


    def relu(self, x1, x2):
        if x2 > x1:
            return self.block_size
        elif x2 == x1:
            return 0
        else:
            return -self.block_size

    def get_distance(self, x, y):
        return math.sqrt(math.pow(x - self.agent.x, 2) + math.pow(y - self.agent.y, 2))

    def _go_radom(self):
        rand_dir = random.randint(1, 4)
        step_size = self.block_size

        new_x, new_y = self.agent.x, self.agent.y

        if rand_dir == 1:
            new_x = self.normalise(self.agent.x + step_size, self.width) 
        elif rand_dir == 2:
            new_y = self.normalise(self.agent.y + step_size, self.height) 
        elif rand_dir == 3:
            new_x = self.normalise(self.agent.x - step_size, self.width) 
        elif rand_dir == 4:
            new_y = self.normalise(self.agent.y - step_size, self.height) 

        collision = False
        x, y = int((new_x)/self.block_size), int((new_y)/self.block_size)
        (w, h) = self.tiles.shape
        if (x < w and y < h):
                tile = self.tiles[x, y]
                collision = tile.solid  
            
        if not collision:
            self.agent.x, self.agent.y = new_x, new_y

    def normalise(self, x, max):
        if x < 0:
            return self.block_size//2
        if x > max:
            return max - self.block_size//2
        return x


class CheckpointController:
    def __init__(self, width, height, block_size, tiles, checkpoints, wait_time) -> None:
        self.agent: Agent = None
        self.tiles: Tile = tiles
        self.width: int = width
        self.height: int = height
        self.block_size: int = block_size

        self.checkpoints: list = checkpoints #self._random_subarray(checkpoints, random.randint(1, len(checkpoints)))
        self.waiting: int = 0
        self.wait_time: int = wait_time

        self.astar = Astar(self.get_map())
        self.path = []

    def get_map(self):
        map = np.zeros(self.tiles.shape)
        for x, row in enumerate(self.tiles):
            for y, tile in enumerate(row):
                map[x, y] = 1 if tile.solid else 0
        print(map)
        return map

    def _step(self):
        if self.agent is None:
            raise ValueError("tablica agentów nie zostały ustawione")
        
        if len(self.checkpoints)==0:
            return

        if (self.waiting > 0): #doing task in the checkpoint
            self.waiting -= 1
            if (self.waiting == 1): #finding best path to the next checkpoint
                next_check = random.choice(self.checkpoints)
                check_position = (next_check.x//self.block_size, next_check.y//self.block_size)
                agent_position = (self.agent.x//self.block_size, self.agent.y//self.block_size)
                print(check_position)
                print(agent_position)
                if check_position == agent_position:
                    self.path = []
                else:
                    self.astar.set_endpoints(agent_position, check_position)
                    self.path = self.astar.astar()
                    print(self.path)
        else:
            if(len(self.path) > 0): #going to the checkpoint
                next_move = self.path.pop(0)
                self.agent.x, self.agent.y = (next_move[0]*self.block_size)+self.block_size//2, (next_move[1]*self.block_size)+self.block_size//2
            else:
                self.waiting = self.wait_time #checkpoint reached, task time

    
    def _random_subarray(array, subarray_length):
        if subarray_length > len(array):
            raise ValueError("Subarray length cannot be greater than the length of the array")

        start_index = random.randint(0, len(array) - subarray_length)
        end_index = start_index + subarray_length

        return array[start_index:end_index]