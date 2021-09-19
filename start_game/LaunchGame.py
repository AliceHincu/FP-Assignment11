import configparser
import UI.UI
import GUI.GUI


if __name__ == '__main__':
    """
    Launch the game
    """
    config = configparser.ConfigParser()
    config.read("settings.properties")

    if str(config["Settings"]["interface"]) == 'ui':
        import pygame
        pygame.quit()
        user_interface = UI.UI.UI()
        user_interface.main_menu_ui()
    elif str(config["Settings"]["interface"]) == 'gui':
        graphical_user_interface = GUI.GUI.GUI()
        graphical_user_interface.start_gui()
