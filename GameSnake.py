import pygame
import time
import random

from GameBoard import GameBoard


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, pygame.Color('black'), [x[0], x[1], snake_block, snake_block])


if __name__ == '__main__':
    pygame.init()
    background = pygame.image.load('snakefiles/backgroundsnake.jpg')
    food = pygame.image.load('snakefiles/food.png')
    food = pygame.transform.scale(food, (food.get_width() // 1, food.get_height() // 1))
    rect_food = food.get_rect()
    dis_width = 600 * 2
    dis_height = 400 * 2
    lose_text = pygame.font.Font(None, 50).render("You lose", True, (100, 255, 100))
    screen = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    snake_block = 10
    snake_speed = 25
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    lose_text_x = dis_width // 2 - lose_text.get_width() // 2
    lose_text_y = dis_height // 2 - lose_text.get_height() // 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    len_snake = 1
    cur_button = None
    food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            screen.blit(background, (0, 0))
            screen.blit(lose_text, (lose_text_x, lose_text_y))
            pygame.display.update()
            for event in pygame.event.get():
                pygame.display.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and pygame.K_LEFT != cur_button:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and pygame.K_RIGHT != cur_button:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and pygame.K_UP != cur_button:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and pygame.K_DOWN != cur_button:
                    y1_change = snake_block
                    x1_change = 0
                cur_button = event.key

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.blit(background, (0, 0))
        screen.blit(food, (food_x, food_y))
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > len_snake:
            del snake_list[0]
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
        our_snake(snake_block, snake_list)
        pygame.display.update()
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            len_snake += 1
        clock.tick(snake_speed)
    pygame.quit()
    quit()
