import Controller


class Agent:
    def __init__(self, x, y, direction, color) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.controller = Controller.IndividualController(self)

    def _run_controller(self):
        self.controller._step()

    def _set_dimensions(self, screen_width, screen_height, block_size):
        self.controller._set_dimensions(screen_width, screen_height, block_size)
    
    def _set_agents_array(self, agents_array):
        self.controller._set_agents_array(agents_array)