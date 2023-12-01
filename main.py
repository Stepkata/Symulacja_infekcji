from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from level_creator import GameLevelCreator
import os
 
pygame.init()
surface = pygame.display.set_mode((1400, 750))
game = GameLevelCreator()

def set_level(value, _):
    print("LOADED: ", value)
    game.load(value[0][0])
def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)
 
def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30) 
    while True:
        game.play_step()

def get_saved_levels():
    directory_path = 'saves'
    try:
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        
        # Create a dictionary with file names as keys and their order as values
        file_tuples = [(f, i) for i, f in enumerate(files)]
        
        return file_tuples
    except OSError as e:
        print(f"Error reading files in directory '{directory_path}': {e}")
        return []


mainmenu = pygame_menu.Menu('Welcome', 1400, 750, theme=themes.THEME_DARK)
mainmenu.add.text_input('Name: ', default='username')
mainmenu.add.button('Play', start_the_game)
levels = get_saved_levels()
print(levels)
mainmenu.add.selector('Level :', levels, onchange=set_level)

mainmenu.add.button('Quit', pygame_menu.events.EXIT)

loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

update_loading = pygame.USEREVENT + 0

def main():
    
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
            if event.type == pygame.QUIT:
                exit()
    
        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())
        
        pygame.display.update()

if __name__ == '__main__':
    main()