import pygame
import os
import sys
import random
import time


def write_coins(coins):
    file = open('data/MenuResoures/coins.txt', 'r')
    curr_coins = int(file.readlines()[0])
    file = open('data/MenuResoures/coins.txt', 'w')
    print(((coins + curr_coins) * 10) // 7, file=file)
    file.close()


class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.way = "RIGHT"

    def change_way(self, way):
        if way == "RIGHT" and not self.way == "LEFT":
            self.way = "RIGHT"
        elif way == "LEFT" and not self.way == "RIGHT":
            self.way = "LEFT"
        elif way == "UP" and not self.way == "DOWN":
            self.way = "UP"
        elif way == "DOWN" and not self.way == "UP":
            self.way = "DOWN"

    def move(self, foodPos):
        if self.way == "RIGHT":
            self.position[0] = self.position[0] + 10
        elif self.way == "LEFT":
            self.position[0] = self.position[0] - 10
        elif self.way == "UP":
            self.position[1] = self.position[1] - 10
        elif self.way == "DOWN":
            self.position[1] = self.position[1] + 10
        self.body.insert(0, list(self.position))

        if self.position == foodPos:
            return 1
        else:
            self.body.pop()
            return 0

    def move_right(self):
        self.position[0] = self.position[0] + 10

    def move_left(self):
        self.position[0] = self.position[0] - 10

    def move_up(self):
        self.position[0] = self.position[1] - 10

    def move_down(self):
        self.position[0] = self.position[1] + 10

    def check_hitbox(self):
        if self.position[0] > width - 10 or self.position[0] < 10:
            return 1
        elif self.position[1] > height or self.position[1] < 10:
            return 1
        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                return 1
        return 0

    def get_head_snake(self):
        return self.position

    def get_body_snake(self):
        return self.body


class Food:
    def __init__(self):
        self.position = [random.randint(4, 46) * 10, random.randint(4, 46) * 10]
        self.isFoodOnScreen = True

    def spawn_food(self):
        if not self.isFoodOnScreen:
            self.position = [random.randrange(4, 46) * 10, random.randrange(4, 46) * 10]
            self.isFoodOnScreen = True
        return self.position

    def set_food_on_screen(self, b):
        self.isFoodOnScreen = b


def player_one():
    wait = True
    score = 0
    while wait:
        screens.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        text = font.render("Игрок 1. Нажмите на любую кнопку, чтобы продолжить", True, (0, 160, 255))
        screens.blit(text, (0, height * .3))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
                wait = False
            if event.type == pygame.QUIT:
                return score
    while True:
        SNAKE_COLOR = [
            (0, 255, 0),
            (0, 0, 255),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_way('RIGHT')
                elif event.key == pygame.K_LEFT:
                    snake.change_way('LEFT')
                elif event.key == pygame.K_UP:
                    snake.change_way('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_way('DOWN')
        food_pos = food.spawn_food()
        while food_pos[0] not in snake.get_body_snake() and food_pos[1] not in snake.get_body_snake():
            food_pos = food.spawn_food()
        if snake.move(food_pos) == 1:
            eat_sound.play()
            score += 1
            food.set_food_on_screen(False)

        screens.blit(background, (0, 0))
        pygame.draw.rect(screens, (244, 164, 96), (10, 10, width, height), width=10)

        for pos in snake.get_body_snake():
            pygame.draw.rect(screens, SNAKE_COLOR[index_snake_color], pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screens, pygame.Color(225, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake.check_hitbox() == 1:
            return score

        pygame.display.set_caption("Змейка | Очки: " + str(score))
        pygame.display.flip()
        fps.tick(25)
    return score


def player_two():
    wait = True
    score = 0
    while wait:
        screens.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        text = font.render("Игрок 2. Нажмите на любую кнопку, чтобы продолжить", True, (0, 160, 255))
        screens.blit(text, (0, height * .3))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
                wait = False
            if event.type == pygame.QUIT:
                return score
    while True:
        SNAKE_COLOR = [
            (0, 255, 0),
            (0, 0, 255),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_way('RIGHT')
                elif event.key == pygame.K_LEFT:
                    snake.change_way('LEFT')
                elif event.key == pygame.K_UP:
                    snake.change_way('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_way('DOWN')

        food_pos = food.spawn_food()
        while food_pos[0] not in snake.get_body_snake() and food_pos[1] not in snake.get_body_snake():
            food_pos = food.spawn_food()
        if snake.move(food_pos) == 1:
            eat_sound.play()
            score += 1
            food.set_food_on_screen(False)

        screens.blit(background, (0, 0))
        pygame.draw.rect(screens, (244, 164, 96), (10, 10, width, height), width=10)

        for pos in snake.get_body_snake():
            pygame.draw.rect(screens, SNAKE_COLOR[index_snake_color], pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screens, pygame.Color(225, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake.check_hitbox() == 1:
            return score

        pygame.display.set_caption("Змейка | Очки: " + str(score))
        pygame.display.flip()
        fps.tick(25)
    return score


pygame.init()
pygame.mixer.init()
display = pygame.display
size = width, height = 900, 900
screens = display.set_mode((width + 20, height + 20))
file = open('data/MenuResoures/settings.txt')
sounds = list(map(int, file.readlines()[0].split()))
file.close()
pygame.mixer.music.load('snakefiles/msc_back.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(sounds[0] / 100)
eat_sound = pygame.mixer.Sound('snakefiles/eat.wav')
eat_sound.set_volume(sounds[1] / 100)
file_index = open('snakefiles/snake_rgb.txt', 'r')
index_snake_color = int(file_index.readlines()[0])
fps = pygame.time.Clock()
background = pygame.image.load('snakefiles/background2.jpg')
pygame.display.set_caption('Змейка')
screens.blit(background, (0, 0))
snake = Snake()
food = Food()
cnt1 = player_one()
pygame.display.set_caption('Змейка')
snake = Snake()
food = Food()
cnt2 = player_two()
if cnt1 or cnt2:
    write_coins(cnt1 + cnt2)
pygame.quit()
os.system("python main.py")
