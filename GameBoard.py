import pygame
from pprint import pprint


class GameBoard:
    def __init__(self, width, height):
        self.width = width + 2
        self.height = height + 3
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 15
        self.line_size = 2

    def set_view(self, left, top, cell_size, line_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.line_size = line_size

    def render_board(self, screen):
        for y in range(self.top, self.cell_size * self.height, self.cell_size + self.left):
            for x in range(self.left, self.cell_size * self.width, self.cell_size + self.top):
                pygame.draw.rect(screen,
                                 pygame.Color('white'),
                                 (x + self.left, y + self.top,
                                  self.left + self.cell_size, self.top + self.cell_size,),
                                 width=self.line_size)


if __name__ == '__main__':
    pygame.init()
    display = pygame.display
    size = width, height = 1024, 768
    screens = display.set_mode(size)
    display.set_caption('GameBoard')
    board = GameBoard(10, 10)
    board.render_board(screens)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
