from agent import Agent
from game import Game
import random


class InfectionSpread(Game):

    def __init__(self):
        self.neighbors = {}

    def _get_neighbors(self, agent, all_agents):
        if agent.id not in self.neighbors:
            self.neighbors[agent.id] = []

        for other_agent in all_agents:
            if other_agent == agent or not other_agent.infected:
                continue

            distance_squared = (agent.x - other_agent.x) ** 2 + (agent.y - other_agent.y) ** 2

            # Przykładowy warunek na sąsiedztwo
            if distance_squared <= 100:
                self.neighbors[agent.id].append(other_agent)

    
    def _reset_neighbors(self):
        self.neighbors = {}

    def _spread_infection(self, infection_probability=0.2):
        new_infected_agents = []

        for infected_agent_id, neighbors_list in self.neighbors.items():
            # Prawdopodobieństwo zarażenia
            for neighbor in neighbors_list:
                if random.uniform(0, 1) < infection_probability:
                    new_infected_agents.append(neighbor)

        # Po 10 klatkach zerujemy listę napotkanych agentów
        self._reset_neighbors()

        return new_infected_agents
        