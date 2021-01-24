import pygame


class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render_board(self, screen):
        cnt_x = 0
        cnt_y = 0
        for y in range(self.top, self.cell_size * height, self.cell_size + self.left):
            for x in range(self.left, self.cell_size * width, self.cell_size + self.top):
                pygame.draw.rect(screen,
                                 pygame.Color('white'),
                                 (x + self.left, y + self.top,
                                  self.left + self.cell_size, self.top + self.cell_size,),
                                 width=2)

    def test_render(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'),
                         (10, 10, 10 + self.cell_size, 10 + self.cell_size,),
                         width=2)
        pygame.draw.rect(screen, pygame.Color('white'),
                         (50, 10, 10 + self.cell_size, 10 + self.cell_size,),
                         width=2)
        pygame.draw.rect(screen, pygame.Color('white'),
                         (90, 10, 10 + self.cell_size, 10 + self.cell_size,),
                         width=2)
        pygame.draw.rect(screen, pygame.Color('white'),
                         (10, 50, 10 + self.cell_size, 10 + self.cell_size,),
                         width=2)


if __name__ == '__main__':
    pygame.init()
    display = pygame.display
    size = width, height = 1024, 768
    screen = display.set_mode(size)
    display.set_caption('GameBoard')
    board = GameBoard(5, 7)
    board.render_board(screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
