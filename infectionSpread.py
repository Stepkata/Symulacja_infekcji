from agent import Agent
import random


class InfectionSpread():

    def __init__(self, block_size):
        self.infected_agent = None
        self.new_infected_agents = None
        self.neighbors = {}
        self.block_size = block_size

    def _get_neighbors(self, infected_agent, all_agents):

        if infected_agent.id not in self.neighbors:
            self.neighbors[infected_agent.id] = []

        for other_agent in all_agents:

            if other_agent.infected:
                continue
            distance_x = self.distance_x(infected_agent, other_agent)
            distance_y = self.distance_y(infected_agent, other_agent)

            #Sprawdzanie po osi x i osi y
            if distance_x == self.block_size and distance_y == self.block_size:
                self.neighbors[infected_agent.id].append(other_agent)
            
            #Sprawdzanie po przekatnej
            if distance_x == distance_y == self.block_size:
                self.neighbors[infected_agent.id].append(other_agent)
            
            
    def _reset_neighbors(self):
        self.neighbors = {}

    def distance_x(self, agent1, agent2):
        return abs(agent1.x - agent2.x)
    
    def distance_y(self, agent1, agent2):
        return abs(agent1.y - agent2.y)
    
    
    def _spread_infection(self, infection_probability=0.2):
        new_infected_agents = []


        for infected_agent_id, neighbors_list in self.neighbors.items():
           
            for neighbor in neighbors_list:
                if random.uniform(0, 1) < infection_probability:
                    new_infected_agents.append(neighbor)
                    neighbor.infected = True

        self._reset_neighbors()

        return new_infected_agents
        