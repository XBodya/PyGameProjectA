import os
import sys
import pygame
import datetime


class Menu:
    def __init__(self):
        self.x = 0
        self.size = (720, 480)
        self.CHECK_TIME = pygame.USEREVENT + 1
        self.FPS = 60

        self.second = SecondMenu()

    def start(self):
        pygame.display.set_caption("Mario Party - menu")
        pygame.time.set_timer(self.CHECK_TIME, 180000)

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(self.size)
        background = self.check_time()
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return "close"
                if event.type == self.CHECK_TIME:
                    background = self.check_time()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        self.click(x, y)

            second_x = self.x % background.get_rect().width
            screen.blit(background,
                        (second_x - background.get_rect().width, 0))

            if second_x <= self.size[0]:
                screen.blit(background, (second_x - 1, 0))

            self.x -= 5

            self.draw_menu(screen)

            pygame.display.update()
            clock.tick(self.FPS)

    def load_background(self, name):
        fullname = os.path.join(os.path.join("data", "backgrounds"), name)

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность файлов игры")
            sys.exit()

        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (720, 480))

        return image

    def click(self, x, y):
        pb_top_left = self.play_button_rect.topleft
        pb_bottom_right = self.play_button_rect.bottomright

        if pb_top_left[0] <= x <= pb_bottom_right[0] and \
                pb_top_left[1] <= y <= pb_bottom_right[1]:
            self.second.start()

    def draw_menu(self, scr):
        fullname = os.path.join("data", "play_button.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность файлов игры")
            sys.exit()

        x, y = self.size

        self.play_button = pygame.image.load(fullname).convert_alpha()
        self.play_button_rect = self.play_button.get_rect(center=(x // 2,
                                                                  y // 2 - 60))

        scr.blit(self.play_button, self.play_button_rect)

        fullname = os.path.join("data", "settings_button.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность файлов игры")
            sys.exit()

        self.settings_button = pygame.image.load(fullname).convert_alpha()
        self.settings_button_rect = self.settings_button.get_rect(
            center=(x // 2 - 245, y // 2 + 90)
        )

        scr.blit(self.settings_button, self.settings_button_rect)

        fullname = os.path.join("data", "rules_button.png")

        self.rules_button = pygame.image.load(fullname).convert_alpha()
        self.rules_button_rect = self.rules_button.get_rect(
            center=(x - 270, y // 2 + 90)
        )

        scr.blit(self.rules_button, self.rules_button_rect)

    def check_time(self):
        hours = datetime.datetime.now().time().hour

        time = "evening"

        if hours < 6:
            time = "night"
        elif 6 <= hours < 12:
            time = "morning"
        elif 12 <= hours < 18:
            time = "day"

        return self.load_background(f"{time}.png")


class SecondMenu:
    def __init__(self):
        self.x = 0
        self.size = (720, 480)
        self.CHECK_TIME = pygame.USEREVENT + 1
        self.PACMAN_ANIM = pygame.USEREVENT + 2
        self.FPS = 60

        self.animation_pacman = 0
        self.animation_snake = 0

        self.pacman_start_animation = False
        self.snake_start_animation = False
        self.pacman_end_animation = False
        self.snake_end_animation = False

    def start(self):
        pygame.display.set_caption("Mario Party - menu")
        pygame.time.set_timer(self.CHECK_TIME, 180000)

        screen = pygame.display.set_mode(self.size)

        clock = pygame.time.Clock()
        background = self.check_time()
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return "close"


                if event.type == self.CHECK_TIME:
                    background = self.check_time()

                if event.type == self.PACMAN_ANIM:
                    self.draw_pacman_animation(screen)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        self.click(x, y)
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    self.aiming(x, y)

            second_x = self.x % background.get_rect().width
            screen.blit(background,
                        (second_x - background.get_rect().width, 0))

            if second_x <= self.size[0]:
                screen.blit(background, (second_x - 1, 0))

            self.x -= 5

            self.draw_menu(screen)

            pygame.display.update()
            clock.tick(self.FPS)

    def load_background(self, name):
        fullname = os.path.join(os.path.join("data", "backgrounds"), name)

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность файлов игры")
            sys.exit()

        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (720, 480))

        return image

    def aiming(self, x, y):
        pb_bottom_right = self.pacman_button_rect.bottomright
        pb_top_left = self.pacman_button_rect.topleft

        if pb_top_left[0] <= x <= pb_bottom_right[0] and \
            pb_top_left[1] <= y <= pb_bottom_right[1] and \
                not self.pacman_start_animation:
            self.pacman_start_animation = True
        elif not (pb_top_left[0] <= x <= pb_bottom_right[0] and \
            pb_top_left[1] <= y <= pb_bottom_right[1]) and \
                self.pacman_start_animation:
            self.pacman_start_animation = False
            self.pacman_end_animation = True

        sb_bottom_right = self.snake_button_rect.bottomright
        sb_top_left = self.snake_button_rect.topleft

        if sb_top_left[0] <= x <= sb_bottom_right[0] and \
            sb_top_left[1] <= y <= sb_bottom_right[1] and \
            not self.snake_start_animation:
            self.snake_start_animation = True
        elif not (sb_top_left[0] <= x <= sb_bottom_right[0] and \
            sb_top_left[1] <= y <= sb_bottom_right[1]) and \
            self.snake_start_animation:
            self.snake_start_animation = False
            self.snake_end_animation = True

    def draw_pacman(self, scr):
        fullname = os.path.join(os.path.join("data", "MenuImages"),
                                "pacmanButton.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность "
                f"файлов игры")
            sys.exit()

        x, y = self.size

        self.pacman_button = pygame.image.load(fullname).convert_alpha()
        self.pacman_button = pygame.transform.scale(
            self.pacman_button,
            (x // 2, round(self.pacman_button.get_rect().height * 1.5))
        )
        self.pacman_button_rect = self.pacman_button.get_rect(
            center=(x * 0.255, round(y * 0.228))
        )

        scr.blit(self.pacman_button, self.pacman_button_rect)

    def draw_snake(self, scr):
        fullname = os.path.join(os.path.join("data", "MenuImages"),
                                "snakeButton.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность "
                f"файлов игры")
            sys.exit()

        x, y = self.size

        self.snake_button = pygame.image.load(fullname).convert_alpha()
        self.snake_button = pygame.transform.scale(
            self.snake_button,
            (x // 2, round(self.snake_button.get_rect().height * 1.5))
        )
        self.snake_button_rect = self.snake_button.get_rect(
            center=(x * 0.75, round(y * 0.238))
        )

        scr.blit(self.snake_button, self.snake_button_rect)

    def draw_pacman_animation(self, scr, reverse=False):
        fullname = os.path.join(os.path.join("data", "MenuImages"),
                                f"pacmanButton_an{self.animation_pacman}.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность "
                f"файлов игры")
            sys.exit()

        x, y = self.size

        self.pacman_button = pygame.image.load(fullname).convert_alpha()
        self.pacman_button = pygame.transform.scale(
            self.pacman_button,
            (x // 2, round(self.pacman_button.get_rect().height * 1.5))
        )
        self.pacman_button_rect = self.pacman_button.get_rect(
            center=(x * 0.255, round(y * 0.228))
        )

        scr.blit(self.pacman_button, self.pacman_button_rect)

        if self.animation_pacman != 7 and not reverse:
            self.animation_pacman += 1
        elif self.animation_pacman != 0 and reverse:
            self.animation_pacman -= 1
        elif self.animation_pacman == 0 and reverse:
            self.animation_pacman = 0
            self.pacman_start_animation = False
            self.pacman_end_animation = False

    def draw_snake_animation(self, scr, reverse=False):
        fullname = os.path.join(os.path.join("data", "MenuImages"),
                                f"snakeButton_an{self.animation_snake}.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность "
                f"файлов игры")
            sys.exit()

        x, y = self.size

        self.snake_button = pygame.image.load(fullname).convert_alpha()
        self.snake_button = pygame.transform.scale(
            self.snake_button,
            (x // 2, round(self.snake_button.get_rect().height * 1.5))
        )
        self.snake_button_rect = self.snake_button.get_rect(
            center=(x * 0.75, round(y * 0.238))
        )

        scr.blit(self.snake_button, self.snake_button_rect)

        if self.animation_snake != 8 and not reverse:
            self.animation_snake += 1
        elif self.animation_snake != 0 and reverse:
            self.animation_snake -= 1
        elif self.animation_snake == 0 and reverse:
            self.animation_snake = 0
            self.snake_end_animation = False
            self.snake_start_animation = False

    def draw_menu(self, scr):
        if not self.pacman_start_animation and not self.snake_start_animation \
                and not self.pacman_end_animation \
                and not self.snake_end_animation:
            self.draw_pacman(scr)

            self.draw_snake(scr)
        elif self.pacman_start_animation and not self.snake_start_animation:
            self.draw_snake(scr)

            self.draw_pacman_animation(scr)
        elif self.pacman_end_animation and not self.snake_start_animation:
            self.draw_snake(scr)

            self.draw_pacman_animation(scr, reverse=True)
        elif self.snake_start_animation and not self.pacman_start_animation:
            self.draw_pacman(scr)

            self.draw_snake_animation(scr)
        elif self.snake_end_animation and not self.pacman_start_animation:
            self.draw_pacman(scr)

            self.draw_snake_animation(scr, reverse=True)

    def check_time(self):
        hours = datetime.datetime.now().time().hour

        time = "evening"

        if hours < 6:
            time = "night"
        elif 6 <= hours < 12:
            time = "morning"
        elif 12 <= hours < 18:
            time = "day"

        return self.load_background(f"{time}.png")

    def click(self, x, y):
        pb_bottom_right = self.pacman_button_rect.bottomright
        pb_top_left = self.pacman_button_rect.topleft

        if pb_top_left[0] <= x <= pb_bottom_right[0] and \
            pb_top_left[1] <= y <= pb_bottom_right[1]:
            pygame.quit()
            os.system("python PacMan.py")
