from agent import Agent
import random
import math


class InfectionSpread():

    def __init__(self, block_size):
        self.infected_agent = None
        self.block_size = block_size

    def _get_neighbors(self, infected_agent, all_agents):

        neighbors = []
        for other_agent in all_agents:
            if other_agent.infected:
                continue
            distance = self.get_distance(infected_agent.x, infected_agent.y,
                                         other_agent.x, other_agent.y)

            if distance <= 1.41*self.block_size:
                neighbors.append(other_agent)
            if distance <= 2.8*self.block_size:
                if random.uniform(0, 1) < 0.5:
                    neighbors.append(other_agent)
        return neighbors

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1- y2, 2))      
            
    def _reset_neighbors(self):
        self.neighbors = {}

    def distance_x(self, agent1, agent2):
        return abs(agent1.x - agent2.x)
    
    def distance_y(self, agent1, agent2):
        return abs(agent1.y - agent2.y)
    
    
    def _spread_infection(self, potential_infection, num_infected, r0=2, reinfection_probability = 0.05):
        new_infected_agents = []
        if len(potential_infection) == 0:
            return new_infected_agents
        sample_size = num_infected*r0 if num_infected*r0 < len( potential_infection) else len(potential_infection)-1
        chosen = random.sample(list(potential_infection), sample_size )
        for agent in chosen:
            if agent.cured:
                if random.uniform(0, 1) < reinfection_probability:
                    new_infected_agents.append(agent)
                    agent.infected = True
            else:
                new_infected_agents.append(agent)
                agent.infected = True

        return new_infected_agents
        