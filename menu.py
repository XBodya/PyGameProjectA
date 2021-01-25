import os
import sys
import pygame
import datetime


def load_background(name):
    fullname = os.path.join(os.path.join("data", "backgrounds"), name)

    if not os.path.isfile(fullname):
        print(f"Файл {fullname} не найден! Проверьте целостность файлов игры")
        sys.exit()

    image = pygame.image.load(fullname).convert()
    image = pygame.transform.scale(image, (720, 480))

    return image


def draw_menu(scr):
    fullname = os.path.join("data", "menu.png")

    if not os.path.isfile(fullname):
        print(f"Файл {fullname} не найден! Проверьте целостность файлов игры")
        sys.exit()

    x, y = size

    menu = pygame.image.load(fullname).convert_alpha()
    menu_rect = menu.get_rect(center=(x // 2, y // 2))

    scr.blit(menu, menu_rect)


def check_time():
    hours = datetime.datetime.now().time().hour

    time = "evening"

    if hours < 6:
        time = "night"
    elif 6 <= hours < 12:
        time = "morning"
    elif 12 <= hours < 18:
        time = "day"

    return load_background(f"{time}.png")


FPS = 60
CHECK_TIME = pygame.USEREVENT + 1

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Mario Party - menu")
    pygame.time.set_timer(CHECK_TIME, 180000)

    size = (720, 480)
    x = 0

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    background = check_time()
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == CHECK_TIME:
                background = check_time()

        second_x = x % background.get_rect().width
        screen.blit(background, (second_x - background.get_rect().width, 0))

        if second_x <= size[0]:
            screen.blit(background, (second_x - 1, 0))

        x -= 5

        draw_menu(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
