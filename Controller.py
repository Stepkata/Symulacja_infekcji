import pygame
import random
import AStar


class IndividualController:
    """A controller class to simulate random movement"""
    def __init__(self, width, height, block_size, tiles):
        self.agent = None
        self.width = width
        self.height = height
        self.block_size = block_size
        self.tiles = tiles
        for x, row in enumerate(self.tiles):
            for y, t in enumerate(row):
                print(x, y, t.solid)

    def _step(self):
        if self.agent is None:
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


        collision = False
        x, y = int((new_x)/self.block_size), int((new_y)/self.block_size)
        (w, h) = self.tiles.shape
        if (x < w and y < h):
                tile = self.tiles[x, y]
                collision = tile.solid  
            
        if not collision:
            self.agent.x, self.agent.y = new_x, new_y

    @staticmethod
    def is_within_screen_bounds(new_x, new_y, width, height, block_size) -> bool:
        half_block_size = block_size // 2

        if new_x  < 0 or new_x + half_block_size > width:
            return False
        if new_y - half_block_size < 0 or new_y + half_block_size > height:
            return False
        
        return True
        

class CrowdController:
    def __init__(self, agents_array):
        self.agents_array = agents_array

    def step(self):
        pass


class CheckpointController:
    def __init__(self, agent, tiles, checkpoints, wait_time) -> None:
        self.agent = agent
        self.map = map
        self.width = None
        self.height = None
        self.block_size = None
        self.agents_array = None

        self.checkpoints = self._random_subarray(checkpoints, random.randint(1, len(checkpoints)))
        self.waiting = 0
        self.wait_time = wait_time

        self.astar = AStar(self.map)
        self.path = []


    def _step(self):
        if (self.waiting > 0): #doing task in the checkpoint
            self.waiting -= 1
            if (self.waiting == 1): #finding best path to the next checkpoint
                next_check = random.choice(self.checkpoints)
                self.astar.set_endpoints(self.agent.position, next_check)
                self.path = self.astar.astar()
        else:
            if(len(self.path) > 0): #going to the checkpoint
                next_move = self.path.pop(0)
                self.agent.x, self.agent.y = next_move[0], next_move[1]
            else:
                self.waiting = self.wait_time #checkpoint reached, task time


    @staticmethod
    def is_within_screen_bounds(new_x, new_y, width, height, block_size) -> bool:
        half_block_size = block_size // 2

        if new_x  < 0 or new_x + half_block_size > width:
            return False
        if new_y - half_block_size < 0 or new_y + half_block_size > height:
            return False
        
        return True
    
    def _set_dimensions(self, width, height, block_size) -> None:
        self.width = width
        self.height = height
        self.block_size = block_size

    def _set_agents_array(self, agents_array) -> None:
        self.agents_array = agents_array
    
    def _random_subarray(array, subarray_length):
        if subarray_length > len(array):
            raise ValueError("Subarray length cannot be greater than the length of the array")

        start_index = random.randint(0, len(array) - subarray_length)
        end_index = start_index + subarray_length

        return array[start_index:end_index]