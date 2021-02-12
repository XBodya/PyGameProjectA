import os
import sys
import pygame
import datetime
import random


class Menu:
    def __init__(self):
        self.x = 0
        self.size = (720, 480)
        self.CHECK_TIME = pygame.USEREVENT + 1
        self.FPS = 60

        self.second = SecondMenu()
        self.sett = Settings()
        self.shop = Shop()
        pygame.mixer.init()
        pygame.mixer.music.load('data/MenuMusic/back.mp3')
        pygame.mixer.music.play(loops=-1)
        file = open('data/MenuResoures/settings.txt')
        volume = list(map(int, file.readlines()[0].split()))
        self.click_sound = pygame.mixer.Sound('data/MenuMusic/push.mp3')
        self.click_sound.set_volume(volume[1] / 100)
        file.close()
        pygame.mixer.music.set_volume(volume[0] / 100)

    def start(self):
        pygame.display.set_caption("Mario Party")
        pygame.time.set_timer(self.CHECK_TIME, 180000)

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(self.size)
        background = self.check_time()
        running = True

        while running:
            file = open('data/MenuResoures/settings.txt')
            volume = list(map(int, file.readlines()[0].split()))
            file.close()
            pygame.mixer.music.set_volume(volume[0] / 100)
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
            self.click_sound.play(0)

        st_top_left = self.settings_button_rect.topleft
        st_bottom_right = self.settings_button_rect.bottomright

        if st_top_left[0] <= x <= st_bottom_right[0] and \
                st_top_left[1] <= y <= st_bottom_right[1]:
            self.sett.start()
            self.click_sound.play(0)

        sp_top_left = self.rules_button_rect.topleft
        sp_bottom_right = self.rules_button_rect.bottomright
        if sp_top_left[0] <= x <= sp_bottom_right[0] and \
                sp_top_left[1] <= y <= sp_bottom_right[1]:
            self.shop.start()
            self.click_sound.play(0)

    def draw_menu(self, scr):
        fullname = os.path.join("data", 'MenuResoures', "play_button.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность файлов игры")
            sys.exit()

        x, y = self.size

        self.play_button = pygame.image.load(fullname).convert_alpha()
        self.play_button_rect = self.play_button.get_rect(center=(x // 2,
                                                                  y // 2 - 60))

        scr.blit(self.play_button, self.play_button_rect)

        fullname = os.path.join("data", 'MenuResoures', "settings_button.png")

        if not os.path.isfile(fullname):
            print(
                f"Файл {fullname} не найден! Проверьте целостность файлов игры")
            sys.exit()

        self.settings_button = pygame.image.load(fullname).convert_alpha()
        self.settings_button_rect = self.settings_button.get_rect(
            center=(x // 2 - 245, y // 2 + 90)
        )

        scr.blit(self.settings_button, self.settings_button_rect)

        fullname = os.path.join("data", 'MenuResoures', "rules_button.png")

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

        file = open('data/MenuResoures/settings.txt')
        volume = list(map(int, file.readlines()[0].split()))
        self.click_sound = pygame.mixer.Sound('data/MenuMusic/push.mp3')
        self.click_sound.set_volume(volume[1] / 100)
        file.close()

    def start(self):
        pygame.display.set_caption("Mario Party")
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
        elif not (pb_top_left[0] <= x <= pb_bottom_right[0] and
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
        elif not (sb_top_left[0] <= x <= sb_bottom_right[0] and
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
            self.click_sound.play(0)
            pygame.quit()
            os.system("python PacMan.py")
            quit()

        sn_bottom_right = self.snake_button_rect.bottomright
        sn_top_left = self.snake_button_rect.topleft
        if sn_top_left[0] <= x <= sn_bottom_right[0] and \
                sn_top_left[1] <= y <= sn_bottom_right[1]:
            self.click_sound.play(0)
            pygame.quit()
            os.system("python GameBoard.py")
            quit()


class Settings:
    def __init__(self):
        self.x = 0
        self.size = (720, 480)
        self.CHECK_TIME = pygame.USEREVENT + 1
        self.FPS = 60
        self.select = [pygame.Rect((int(self.size[0] * 0.1), int(self.size[1] * 0.1),
                                    int(self.size[0] * 0.8), int(self.size[1] * 0.2))),
                       pygame.Rect((int(self.size[0] * 0.1), int(self.size[1] * 0.4),
                                    int(self.size[0] * 0.8), int(self.size[1] * 0.2)))]
        self.index = 0
        file = open('data/MenuResoures/settings.txt')
        volume = list(map(int, file.readlines()[0].split()))
        self.click_sound = pygame.mixer.Sound('data/MenuMusic/push.mp3')
        self.click_sound.set_volume(volume[1] / 100)
        file.close()

    def start(self):
        pygame.display.set_caption("Mario Party")
        pygame.time.set_timer(self.CHECK_TIME, 180000)

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(self.size)
        background = self.check_time()
        running = True
        file = open('data/MenuResoures/settings.txt', 'r')
        koe_music_effect = list(map(int, file.readlines()[0].split()))
        file.close()

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.index = (self.index - 1) % 2
                        self.click_sound.play(0)
                    if event.key == pygame.K_UP:
                        self.index = (self.index + 1) % 2
                        self.click_sound.play(0)
                    if event.key == pygame.K_LEFT:
                        file = open('data/MenuResoures/settings.txt', 'r')
                        koe_music_effect = list(map(int, file.readlines()[0].split()))
                        file.close()
                        koe_music_effect[self.index] = koe_music_effect[self.index] - 1 \
                            if koe_music_effect[self.index] - 1 >= 0 else \
                            koe_music_effect[self.index]
                        file = open('data/MenuResoures/settings.txt', 'w')
                        print(koe_music_effect[0], koe_music_effect[1], file=file)
                        file.close()
                    if event.key == pygame.K_RIGHT:
                        file = open('data/MenuResoures/settings.txt', 'r')
                        koe_music_effect = list(map(int, file.readlines()[0].split()))
                        file.close()
                        koe_music_effect[self.index] = koe_music_effect[self.index] + 1 \
                            if koe_music_effect[self.index] + 1 <= 100 else \
                            koe_music_effect[self.index]
                        file = open('data/MenuResoures/settings.txt', 'w')
                        print(koe_music_effect[0], koe_music_effect[1], file=file)
                        file.close()

            screen.blit(background,
                        (0, 0))
            font = pygame.font.Font(None, 50)
            text = font.render("Музыка", True, (255, 0, 0))
            screen.blit(text, (int(self.size[0] * 0.1), 0))
            text2 = font.render("Звуковые эффекты", True, (255, 0, 0))
            screen.blit(text, (int(self.size[0] * 0.1), 0))
            screen.blit(text2, (int(self.size[0] * 0.1), int(self.size[1] * 0.3)))
            pygame.draw.rect(screen, (255, 255, 255), (int(self.size[0] * 0.1),
                                                       int(self.size[1] * 0.1),
                                                       int(self.size[0] * 0.8),
                                                       int(self.size[1] * 0.2)))
            pygame.draw.rect(screen, (255, 255, 255), (int(self.size[0] * 0.1),
                                                       int(self.size[1] * 0.4),
                                                       int(self.size[0] * 0.8),
                                                       int(self.size[1] * 0.2)))
            pygame.draw.rect(screen, (255, 0, 0), (int(self.size[0] * 0.1),
                                                   int(self.size[1] * 0.1),
                                                   int(self.size[0] * 0.8 * (koe_music_effect[0] / 100)),
                                                   int(self.size[1] * 0.2)))
            pygame.draw.rect(screen, (255, 0, 0), (int(self.size[0] * 0.1),
                                                   int(self.size[1] * 0.4),
                                                   int(self.size[0] * 0.8 * (koe_music_effect[1] / 100)),
                                                   int(self.size[1] * 0.2)))
            pygame.draw.rect(screen, (0, 0, 0), (int(self.size[0] * 0.1),
                                                 int(self.size[1] * 0.1),
                                                 int(self.size[0] * 0.8),
                                                 int(self.size[1] * 0.2)),
                             width=5)
            pygame.draw.rect(screen, (0, 0, 0), (int(self.size[0] * 0.1),
                                                 int(self.size[1] * 0.4),
                                                 int(self.size[0] * 0.8),
                                                 int(self.size[1] * 0.2)),
                             width=5)
            pygame.draw.rect(screen, (0, 255, 0), (self.select[self.index].topleft[0],
                                                   self.select[self.index].topleft[1],
                                                   self.select[self.index].width,
                                                   self.select[self.index].height),
                             width=5)
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


class Shop:
    def __init__(self):
        self.x = 0
        self.size = (720, 480)
        self.CHECK_TIME = pygame.USEREVENT + 1
        self.FPS = 60
        self.select = [pygame.Rect((
            int(self.size[0] * 0.1),
            int(self.size[1] * 0.01),
            int(self.size[0] * 0.8),
            int(self.size[1] * 0.15)
        )),
            pygame.Rect((
                int(self.size[0] * 0.1),
                int(self.size[1] * 0.3),
                int(self.size[0] * 0.8),
                int(self.size[1] * 0.15)
            )),
            pygame.Rect((
                int(self.size[0] * 0.1),
                int(self.size[1] * 0.6),
                int(self.size[0] * 0.8),
                int(self.size[1] * 0.15)
            ))]
        self.index = 0
        file = open('data/MenuResoures/settings.txt')
        volume = list(map(int, file.readlines()[0].split()))
        self.click_sound = pygame.mixer.Sound('data/MenuMusic/push.mp3')
        self.click_sound.set_volume(volume[1] / 100)
        file.close()

    def start(self):
        pygame.display.set_caption("Mario Party")
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.index = (self.index - 1) % 3
                        self.click_sound.play(0)
                    if event.key == pygame.K_DOWN:
                        self.index = (self.index + 1) % 3
                        self.click_sound.play(0)
                if event.type == pygame.K_SPACE:
                    file = open('data/MenuResoures/coins.txt', 'r')
                    coins = int(file.readlines()[0])
                    file.close()
                    file = open('data/MenuResoures/shop.txt', 'r')
                    skins = list(map(str, file.readlines()[0].split()))
                    file.close()
                    if str(self.index) in skins:
                        file = open('snakefiles/snake_rgb.txt', 'w')
                        print(self.index, file=file)
                        file.close()
                    else:
                        if self.index == 1 and coins >= 100:
                            file = open('data/MenuResoures/coins.txt', 'w')
                            print(coins - 100, file=file)
                            file.close()
                            file = open('data/MenuResoures/shop.txt', 'w')
                            skins.append(self.index)
                            print(' '.join(skins), file=file)
                            file.close()

                        elif self.index == 2 and coins >= 999:
                            file = open('data/MenuResoures/coins.txt', 'w')
                            print(coins - 100, file=file)
                            file.close()
                            file = open('data/MenuResoures/shop.txt', 'w')
                            skins.append(self.index)
                            print(' '.join(skins), file=file)
                            file.close()

            screen.blit(background,
                        (0, 0))
            pygame.draw.rect(screen, (255, 255, 255),
                             (
                                 int(self.size[0] * 0.1),
                                 int(self.size[1] * 0.01),
                                 int(self.size[0] * 0.8),
                                 int(self.size[1] * 0.15)
                             ))
            pygame.draw.rect(screen, (255, 255, 255),
                             (
                                 int(self.size[0] * 0.1),
                                 int(self.size[1] * 0.3),
                                 int(self.size[0] * 0.8),
                                 int(self.size[1] * 0.15)
                             ))
            pygame.draw.rect(screen, (255, 255, 255),
                             (
                                 int(self.size[0] * 0.1),
                                 int(self.size[1] * 0.6),
                                 int(self.size[0] * 0.8),
                                 int(self.size[1] * 0.15)
                             ))
            pygame.draw.rect(screen, (0, 0, 0),
                             (
                                 int(self.size[0] * 0.1),
                                 int(self.size[1] * 0.01),
                                 int(self.size[0] * 0.8),
                                 int(self.size[1] * 0.15)
                             ), width=5)
            pygame.draw.rect(screen, (0, 0, 0),
                             (
                                 int(self.size[0] * 0.1),
                                 int(self.size[1] * 0.3),
                                 int(self.size[0] * 0.8),
                                 int(self.size[1] * 0.15)
                             ), width=5)
            pygame.draw.rect(screen, (0, 0, 0),
                             (
                                 int(self.size[0] * 0.1),
                                 int(self.size[1] * 0.6),
                                 int(self.size[0] * 0.8),
                                 int(self.size[1] * 0.15)
                             ), width=5)
            pygame.draw.rect(screen, (0, 255, 0),
                             (
                                 int(self.size[0] * 0.11),
                                 int(self.size[1] * 0.03),
                                 int(self.size[0] * 0.5),
                                 int(self.size[1] * 0.1)
                             ))
            pygame.draw.rect(screen, (0, 0, 255),
                             (
                                 int(self.size[0] * 0.11),
                                 int(self.size[1] * 0.32),
                                 int(self.size[0] * 0.5),
                                 int(self.size[1] * 0.1)
                             ))
            pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                             (
                                 int(self.size[0] * 0.11),
                                 int(self.size[1] * 0.62),
                                 int(self.size[0] * 0.5),
                                 int(self.size[1] * 0.1)
                             ))
            pygame.draw.rect(screen, (0, 255, 0), (self.select[self.index].topleft[0],
                                                   self.select[self.index].topleft[1],
                                                   self.select[self.index].width,
                                                   self.select[self.index].height),
                             width=5)
            font = pygame.font.Font(None, 50)
            file = open('data/MenuResoures/shop.txt')
            skins = list(map(str, file.readlines()[0].split()))
            file.close()
            price1 = font.render('{}'.format(100 if '1' not in skins else ''), True, (255, 0, 0))
            price2 = font.render('{}'.format(999 if '2' not in skins else ''), True, (255, 0, 0))
            screen.blit(price1, (int(self.size[0] * 0.71),
                                 int(self.size[1] * 0.32)))
            screen.blit(price2, (int(self.size[0] * 0.71),
                                 int(self.size[1] * 0.62)))
            file = open('data/MenuResoures/coins.txt')
            coins = int(file.readlines()[0])
            file.close()
            font = pygame.font.Font(None, 40)
            text = font.render('Кол-во монет: {}'.format(coins), True, (255, 0, 0))
            screen.blit(text, (int(self.size[0] * 0.1), int(self.size[1] * 0.8)))
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
