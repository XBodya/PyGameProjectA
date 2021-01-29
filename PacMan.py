import pygame
import os
import sys
from Pacman_board import game_board

game_board_copy = game_board[:]


class Ghost(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__(all_sprites)

        self.speed = 4

        self.facing = "left"
        self.next_facing = None

        self.game_start = True

        self.leave_home = True

        self.new_crosroad = False

        if color == "red":

            self.animations = {
                "up": [load_image("tile102.png"), load_image("tile103.png")],
                "left": [load_image("tile100.png"), load_image("tile101.png")],
                "right": [load_image("tile096.png"), load_image("tile097.png")],
                "down": [load_image("tile098.png"), load_image("tile099.png")]
            }

            self.aim = [25, 6]

            self.moving = True

            self.index_x = 14
            self.index_y = 14

            self.x = self.index_x * square
            self.y = self.index_y * square

            self.old_x = self.index_x
            self.old_y = self.index_y

            self.blocked_facing = "right"
        elif color == "pink":

            self.animations = {
                "up": [load_image("tile134.png"), load_image("tile135.png")],
                "left": [load_image("tile132.png"), load_image("tile133.png")],
                "right": [load_image("tile128.png"), load_image("tile129.png")],
                "down": [load_image("tile130.png"), load_image("tile131.png")]
            }

            self.moving = False

            self.index_x = 16
            self.index_y = 17

            self.x = self.index_x * square
            self.y = self.index_y * square
        elif color == "yellow":

            self.animations = {
                "up": [load_image("tile150.png"), load_image("tile151.png")],
                "left": [load_image("tile148.png"), load_image("tile149.png")],
                "right": [load_image("tile144.png"), load_image("tile145.png")],
                "down": [load_image("tile146.png"), load_image("tile147.png")]
            }

            self.moving = False

            self.index_x = 14
            self.index_y = 17

            self.x = self.index_x * square
            self.y = self.index_y * square
        elif color == "blue":

            self.animations = {
                "up": [load_image("tile142.png"), load_image("tile143.png")],
                "left": [load_image("tile140.png"), load_image("tile141.png")],
                "right": [load_image("tile136.png"), load_image("tile137.png")],
                "down": [load_image("tile138.png"), load_image("tile139.png")]
            }

            self.moving = False

            self.index_x = 12
            self.index_y = 17

            self.x = self.index_x * square
            self.y = self.index_y * square

        self.image = self.animations[self.facing][0]
        self.rect = self.image.get_rect()

        self.delta_x, self.delta_y = self.rect.width // 2, self.rect.height // 8

        self.current_animation = 0

    def crossroad(self, x, y):
        can_move = []

        if not check_wall(x + 1, y):
            can_move.append("right")
        if not check_wall(x - 1, y):
            can_move.append("left")
        if not check_wall(x, y - 1):
            can_move.append("up")
        if not check_wall(x, y + 1):
            can_move.append("down")

        if len(can_move) >= 3:
            return can_move
        return [False, can_move]

    def update(self):
        if self.moving is True:
            self.delta_x = 0

            if self.game_start:
                self.facing = "left"
                self.game_start = False

            directions = self.crossroad(self.index_x, self.index_y)

            if directions[0] and not self.new_crosroad:
                if self.index_x != self.old_x and self.index_y != self.old_y:
                    self.blocked_facing = self.block_facing(self.facing)

                variants = []

                for direction in directions:
                    if direction != self.blocked_facing:
                        if direction == "up":
                            variants.append([abs(self.aim[0] * square - self.x) + abs(self.aim[1] * square - (self.y - 1)), "up"])
                        elif direction == "down":
                            variants.append([abs(self.aim[0] * square - self.x) + abs(self.aim[1] * square - (self.y + 1)), "down"])
                        elif direction == "left":
                            variants.append([abs(self.aim[0] * square - (self.x - 1)) + abs(self.aim[1] * square - self.y), "left"])
                        else:
                            variants.append([abs(self.aim[0] * square - (self.x + 1)) + abs(self.aim[1] * square - self.y), "right"])

                self.facing = sorted(variants, key=lambda x: x[0])[0][1]

                self.new_crosroad = True

            if self.facing == "left":
                if not check_wall(self.index_x - 1, self.index_y):
                    if self.x == (self.index_x - 1) * square:
                        self.old_x = self.index_x

                        self.index_x -= 1

                        self.new_crosroad = False
                    else:
                        self.x -= self.speed
                else:
                    self.blocked_facing = self.block_facing(self.facing)

                    variants = self.change_direction(directions[1])

                    self.facing = sorted(variants, key=lambda x: x[0])[0][1]
            elif self.facing == "right":
                if not check_wall(self.index_x + 1, self.index_y):
                    if self.x == (self.index_x + 1) * square:
                        self.old_x = self.old_x

                        self.index_x += 1

                        self.new_crosroad = False
                    else:
                        self.x += self.speed
                else:
                    self.blocked_facing = self.block_facing(self.facing)

                    variants = self.change_direction(directions[1])

                    self.facing = sorted(variants, key=lambda x: x[0])[0][1]
            elif self.facing == "up":
                if not check_wall(self.index_x, self.index_y - 1):
                    if self.y == (self.index_y - 1) * square:
                        self.old_y = self.index_y

                        self.index_y -= 1

                        self.new_crosroad = False
                    else:
                        self.y -= self.speed
                else:
                    self.blocked_facing = self.block_facing(self.facing)

                    variants = self.change_direction(directions[1])

                    self.facing = sorted(variants, key=lambda x: x[0])[0][1]
            elif self.facing == "down":
                if not check_wall(self.index_x, self.index_y + 1):
                    if self.y == (self.index_y + 1) * square:
                        self.old_y = self.index_y

                        self.index_y += 1

                        self.new_crosroad = False
                    else:
                        self.y += self.speed
                else:
                    self.blocked_facing = self.block_facing(self.facing)

                    variants = self.change_direction(directions[1])

                    self.facing = sorted(variants, key=lambda x: x[0])[0][1]

            pygame.draw.circle(screen, YELLOW, (self.aim[0] * square, self.aim[1] * square), 10)

        self.image = self.animations[self.facing][self.current_animation]
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x - self.delta_x, self.y - self.delta_y)

    def block_facing(self, facing):
        if facing == "up":
            return "down"
        if facing == "down":
            return "up"
        if facing == "left":
            return "right"
        if facing == "right":
            return "left"

    def change_direction(self, directions):
        variants = []

        for direction in directions:
            if direction != self.blocked_facing:
                if direction == "up":
                    variants.append([abs(self.aim[0] - self.x) + abs(self.aim[1] - (self.y - 1)), "up"])
                elif direction == "down":
                    variants.append([abs(self.aim[0] - self.x) + abs(self.aim[1] - (self.y + 1)), "down"])
                elif direction == "left":
                    variants.append([abs(self.aim[0] - (self.x - 1)) + abs(self.aim[1] - self.y), "left"])
                else:
                    variants.append([abs(self.aim[0] - (self.x + 1)) + abs(self.aim[1] - self.y), "right"])

        return variants


def check_wall(x, y):
    if game_board[y][x] == 3:
        return True
    else:
        return False


class PacMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.index_x = 14
        self.index_y = 26

        self.x = self.index_x * square
        self.y = self.index_y * square

        self.speed = 4

        self.facing = "up"
        self.next_facing = None

        self.animations = {
            "up": [load_image("tile049.png"), load_image("tile051.png")],
            "left": [load_image("tile048.png"), load_image("tile050.png")],
            "right": [load_image("tile052.png"), load_image("tile054.png")],
            "down": [load_image("tile053.png"), load_image("tile055.png")]
        }

        self.image = self.animations[self.facing][0]
        self.rect = self.image.get_rect()

        self.delta_x, self.delta_y = self.rect.width // 2, self.rect.height // 8

        self.current_animation = 0

        self.moving = False

        game_board_copy[self.index_x][self.index_y] = -1

    def check_facing(self, facing):
        if facing == "up":
            return check_wall(self.index_x, self.index_y - 1)
        elif facing == "left":
            return check_wall(self.index_x - 1, self.index_y)
        elif facing == "right":
            return check_wall(self.index_x + 1, self.index_y)
        elif facing == "down":
            return check_wall(self.index_x, self.index_y + 1)

    def new_facing(self):
        if self.next_facing is not None and not self.check_facing(self.next_facing):
            self.facing = self.next_facing
            self.next_facing = None

    def update(self):
        if self.moving:
            if self.facing == "up":
                if not check_wall(self.index_x, self.index_y - 1):
                    if self.y == (self.index_y - 1) * square:
                        self.index_y -= 1

                        game_board_copy[self.index_y][self.index_x] = 1

                        self.new_facing()
                    else:
                        self.y -= self.speed
                else:
                    self.moving = False
            elif self.facing == "left":
                if not check_wall(self.index_x - 1, self.index_y):
                    if self.x == (self.index_x - 1) * square:
                        self.index_x -= 1

                        game_board_copy[self.index_y][self.index_x] = 1

                        self.new_facing()
                    else:
                        self.x -= self.speed
                else:
                    self.moving = False
            elif self.facing == "right":
                if not check_wall(self.index_x + 1, self.index_y):
                    if self.x == (self.index_x + 1) * square:
                        self.index_x += 1

                        game_board_copy[self.index_y][self.index_x] = 1

                        self.new_facing()
                    else:
                        self.x += self.speed
                else:
                    self.moving = False
            elif self.facing == "down":
                if not check_wall(self.index_x, self.index_y + 1):
                    if self.y == (self.index_y + 1) * square:
                        self.index_y += 1

                        game_board_copy[self.index_y][self.index_x] = 1

                        self.new_facing()
                    else:
                        self.y += self.speed
                else:
                    self.moving = False

        self.image = self.animations[self.facing][self.current_animation]
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x - self.delta_x, self.y - self.delta_y)

    def change_animation(self):
        if self.current_animation == 0 and self.moving:
            self.current_animation = 1
        elif self.moving:
            self.current_animation = 0

        self.update()

    def move(self, facing):
        if self.moving is True:
            self.next_facing = facing
        else:
            self.facing = facing
            self.moving = True
            self.delta_x = 0

            self.current_animation = 0


class Game:
    def __init__(self, group):
        self.pacman = PacMan()

        for color in ["red", "pink", "yellow", "blue"]:
            self.ghost = Ghost(color)

            ghosts.add(self.ghost)

        self.group = group

    def update(self):
        render(screen)

        self.group.update()
        self.group.draw(screen)


def load_image(name, color_key=None):
    fullname = os.path.join(os.path.join('data', "ElementImages"), name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()

        if color_key == -1:
            color_key = image.get_at((0, 0))

        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


def render(scr):
    scr.fill(BLACK)

    current_tile = 0

    for i in range(3, len(game_board_copy) - 2):
        for j in range(len(game_board_copy[0])):
            if game_board_copy[i][j] == 3:
                image_name = str(current_tile)
                if len(image_name) == 1:
                    image_name = "00" + image_name
                elif len(image_name) == 2:
                    image_name = "0" + image_name

                image_name = "tile" + image_name + ".png"
                tile_image = pygame.image.load(
                    os.path.join(BOARD_PATH, image_name))
                tile_image = pygame.transform.scale(tile_image,
                                                    (square, square))

                screen.blit(tile_image,
                            (j * square, i * square, square, square))
            elif game_board_copy[i][j] == 2:
                pygame.draw.circle(screen, WHITE, (
                    j * square + square // 2, i * square + square // 2),
                                   square // 8)
            elif game_board_copy[i][j] == 5:
                pygame.draw.circle(screen, BLACK, (
                    j * square + square // 2, i * square + square // 2),
                                   square // 4)
            elif game_board_copy[i][j] == 6:
                pygame.draw.circle(screen, PINK, (
                    j * square + square // 2, i * square + square // 2),
                                   square // 4)

            current_tile += 1


BLUE = pygame.Color("blue")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = pygame.Color("pink")
YELLOW = pygame.Color("yellow")
BOARD_PATH = os.path.join("data", "BoardImages")

ANIMATION_CHANGE = pygame.USEREVENT + 1

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("PacMan")
    pygame.time.set_timer(ANIMATION_CHANGE, 200)

    square = 20
    width, height = (len(game_board_copy[0]) * square, len(game_board_copy) * square)
    screen = pygame.display.set_mode((width, height))
    running = True

    all_sprites = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()

    game = Game(all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ANIMATION_CHANGE:
                game.pacman.change_animation()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    game.pacman.move("right")
                elif event.key == pygame.K_s:
                    game.pacman.move("down")
                elif event.key == pygame.K_a:
                    game.pacman.move("left")
                elif event.key == pygame.K_w:
                    game.pacman.move("up")

        game.update()

        pygame.display.flip()

    pygame.quit()
