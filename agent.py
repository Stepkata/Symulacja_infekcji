CURED = (104, 197, 219)

class Agent:
    def __init__(self,id, x, y, direction, color, infected, controller) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.position = (x,y)
        self.direction = direction
        self.color = color
        self.infected = infected
        self.cured = False
        self.time_infected = 0
        self.controller = controller
        self.controller.agent = self

    def _run_controller(self):
        self.controller._step()

    def get_cured(self):
        self.infected = False
        self.cured = True
        self.time_infected = 0
        self.color = CURED