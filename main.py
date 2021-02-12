import pygame
from menu import Menu

if __name__ == '__main__':
    pygame.init()

    menu = Menu()
    running = True

    current_screen = menu

    while running:
        next_action = current_screen.start()

        if next_action == "close":
            running = False

    pygame.quit()
