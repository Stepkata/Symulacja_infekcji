import pygame
from level_creator import GameLevelCreator


if __name__ == '__main__':
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = GameLevelCreator(screen_width, screen_height)

    while True:
        game.play_step()

    pygame.quit()