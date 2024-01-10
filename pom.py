import pygame 
import pygame_menu as pm 
  
pygame.init() 
  
# Screen 
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
  
# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
  
# Main function of the program 
  
  
def main():    
    controllers = [
        ("Random", 'random'),
        ("Checkpoint", 'checkpoint'),
        ("Herd", 'herd')
    ]
  
    # This function displays the currently selected options 
  
    def printSettings(): 
        print("\n\n") 
        # getting the data using "get_input_data" method of the Menu class 
        settingsData = settings.get_input_data() 
  
        for key in settingsData.keys(): 
            print(f"{key}\t:\t{settingsData[key]}") 
  
    # Creating the settings menu 
    settings = pm.Menu(title="Settings", 
                       width=WIDTH, 
                       height=HEIGHT, 
                       theme=pm.themes.THEME_GREEN) 
  
    # Adjusting the default values 
    settings._theme.widget_font_size = 25
    settings._theme.widget_font_color = BLACK 
    settings._theme.widget_alignment = pm.locals.ALIGN_LEFT 
  
    # Text input that takes in the username 
    settings.add.text_input(title="User Name : ", textinput_id="username") 
    settings.add.text_input(title="R_0: ", textinput_id="r0")
    settings.add.dropselect(title="Controller", items=controllers, 
                            dropselect_id="controller", default=0) 
    settings.add.range_slider(title="Number of agents", default=60, range_values=( 
        2, 100), increment=1, value_format=lambda x: str(int(x)), rangeslider_id="agents_num") 
    
    settings.add.button(title="Restore Defaults", action=settings.reset_value, 
                        font_color=WHITE, background_color=RED)

    settings.add.button(title="Return To Main Menu", 
                        action=pm.events.BACK, align=pm.locals.ALIGN_CENTER) 
  
    # Creating the main menu 
    mainMenu = pm.Menu(title="Main Menu", 
                       width=WIDTH, 
                       height=HEIGHT, 
                       theme=pm.themes.THEME_GREEN) 
  
    # Adjusting the default values 
    mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER 
  
    # Button that takes to the settings menu when clicked 
    mainMenu.add.button(title="Settings", action=settings, 
                        font_color=WHITE, background_color=GREEN) 
  
    # An empty label that is used to add a seperation between the two buttons 
    mainMenu.add.label(title="") 
  
    # Exit button that is used to terminate the program 
    mainMenu.add.button(title="Exit", action=pm.events.EXIT, 
                        font_color=WHITE, background_color=RED) 
  
    # Lets us loop the main menu on the screen 
    mainMenu.mainloop(screen) 
  
  
if __name__ == "__main__": 
    main() 