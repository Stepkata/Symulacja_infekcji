import Controller


class Agent:
    def __init__(self, x, y, direction) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.controller = Controller.IndividualController(self)

    def _run_controller(self):
        self.controller._step()
