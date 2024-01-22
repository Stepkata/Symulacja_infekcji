from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from level_creator import GameLevelCreator
from game import Game
import os
import pygame_menu as pm 


RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 

pygame.init()
surface = pygame.display.set_mode((1400, 750))
game = Game()
level_creator = GameLevelCreator()
level_creator_bool = False

controllers = [
        ("Random", 'random'),
        ("Checkpoint", 'checkpoint'),
        ("Herd", 'herd')
    ]


def set_level(value, level):
    global level_creator_bool
    level_creator_bool = True
    if level != 0:
        print("LOADED: ", value)
        game.load(value[0][0])
        level_creator.load(value[0][0])


def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)
    settingsData = settings.get_input_data() 
    print(settingsData)
    
    game.set_settings(settingsData)
    game.step_machine(10000)
    while True:
        game.play_step()


def start_the_level_creator():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)
    settingsData = settings.get_input_data() 
    while level_creator.return_to_main_menu == False:
        level_creator.play_step()
    

def get_saved_levels():
    directory_path = "saves"
    try:
        files = [
            f.replace(".dat.npy", "")
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]

        # Create a dictionary with file names as keys and their order as values
        file_tuples = [(f, i + 1) for i, f in enumerate(files)]

        return file_tuples
    except OSError as e:
        print(f"Error reading files in directory '{directory_path}': {e}")
        return []


settings = pm.Menu(title="Settings", 
                       width=1400,
                       height=750, 
                       theme=pm.themes.THEME_GREEN) 
  
    # Adjusting the default values 
settings._theme.widget_font_size = 25
settings._theme.widget_font_color = BLACK 
settings._theme.widget_alignment = pm.locals.ALIGN_LEFT 

# Text input that takes in the username 
settings.add.text_input(title="User Name : ", textinput_id="username", default='user') 
settings.add.text_input(title="R_0: ", textinput_id="r0", default=2)
settings.add.dropselect(title="Controller", items=controllers, 
                        dropselect_id="controller", default=0) 

settings.add.button(title="Restore Defaults", action=settings.reset_value, 
                    font_color=WHITE, background_color=RED)
settings.add.button(title="Return To Main Menu", 
                    action=pm.events.BACK, align=pm.locals.ALIGN_CENTER) 


mainmenu = pygame_menu.Menu("Welcome", 1400, 750, theme=themes.THEME_DARK)
mainmenu.add.button("Play", start_the_game)
mainmenu.add.button("Level creator", start_the_level_creator)
mainmenu.add.button(title="Simulation settings", action=settings) 
mainmenu.add.button(title="Exit", action=pm.events.EXIT) 


levels = get_saved_levels()
levels.insert(0, ("Empty", 0))
print(levels)
mainmenu.add.selector("Level :", levels, onchange=set_level)

mainmenu.add.button("Quit", pygame_menu.events.EXIT)

loading = pygame_menu.Menu(
    "Loading the Game...", 600, 400, theme=themes.THEME_DARK
)
loading.add.progress_bar(
    "Progress",
    progressbar_id="1",
    default=0,
    width=200,
)

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

update_loading = pygame.USEREVENT + 0


def main():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                new_value = min(progress.get_value() + 1, 100) 
                progress.set_value(new_value)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)          
            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if mainmenu.get_current().get_selected_widget():
                arrow.draw(
                    surface, mainmenu.get_current().get_selected_widget()
                )

        pygame.display.update()


if __name__ == "__main__":
    main()
