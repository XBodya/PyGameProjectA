import pygame
import os
import sys
import datetime
import random
from Pacman_board import game_board

game_board_copy = game_board[:]


class Ghost(pygame.sprite.Sprite):
    def __init__(self, color, pacman, game):
        super().__init__(all_sprites)

        self.speed = 4
        self.color = color
        self.pacman = pacman
        self.game = game

        self.facing = "left"
        self.eat = False
        self.next_facing = None
        self.mode = RUN_UP_MODE
        self.color_notify = False

        self.game_start = True

        self.new_crosroad = False

        self.escape_animations = [load_image("tile072.png"),
                                  load_image("tile073.png")]
        self.color_escape_animations = [load_image("tile072.png"),
                                        load_image("tile070.png")]
        self.invisible_animations = {
            "up": [load_image("tile158.png"), load_image("tile159.png")],
            "left": [load_image("tile156.png"), load_image("tile157.png")],
            "right": [load_image("tile152.png"), load_image("tile153.png")],
            "down": [load_image("tile154.png"), load_image("tile155.png")]
        }

        if color == "red":

            self.animations = {
                "up": [load_image("tile102.png"), load_image("tile103.png")],
                "left": [load_image("tile100.png"), load_image("tile101.png")],
                "right": [load_image("tile096.png"),
                          load_image("tile097.png")],
                "down": [load_image("tile098.png"), load_image("tile099.png")]
            }

            self.aim_run = [25, 6]
            self.current_aim = self.aim_run

            self.house_exit_x = 14
            self.house_exit_y = 15

            self.in_house = False
            self.house = [14, 17]

            self.moving = False

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
                "right": [load_image("tile128.png"),
                          load_image("tile129.png")],
                "down": [load_image("tile130.png"), load_image("tile131.png")]
            }

            self.aim_run = [6, 8]
            self.current_aim = [14, 15]

            self.house_exit_x = 14
            self.house_exit_y = 15

            self.in_house = True
            self.house = [16, 17]

            self.moving = False

            self.index_x = 16
            self.index_y = 17

            self.x = self.index_x * square
            self.y = self.index_y * square

            self.old_x = self.index_x
            self.old_y = self.index_y

            self.blocked_facing = "right"
        elif color == "yellow":

            self.animations = {
                "up": [load_image("tile150.png"), load_image("tile151.png")],
                "left": [load_image("tile148.png"), load_image("tile149.png")],
                "right": [load_image("tile144.png"),
                          load_image("tile145.png")],
                "down": [load_image("tile146.png"), load_image("tile147.png")]
            }

            self.aim_run = [9, 30]
            self.current_aim = [14, 15]

            self.house_exit_x = 14
            self.house_exit_y = 15

            self.in_house = True
            self.house = [14, 17]

            self.moving = False

            self.index_x = 14
            self.index_y = 17

            self.x = self.index_x * square
            self.y = self.index_y * square

            self.old_x = self.index_x
            self.old_y = self.index_y

            self.blocked_facing = "right"
        elif color == "blue":

            self.animations = {
                "up": [load_image("tile142.png"), load_image("tile143.png")],
                "left": [load_image("tile140.png"), load_image("tile141.png")],
                "right": [load_image("tile136.png"),
                          load_image("tile137.png")],
                "down": [load_image("tile138.png"), load_image("tile139.png")]
            }

            self.aim_run = [21, 31]
            self.current_aim = [14, 15]

            self.house_exit_x = 14
            self.house_exit_y = 15

            self.in_house = True
            self.house = [12, 17]

            self.moving = False

            self.index_x = 12
            self.index_y = 17

            self.x = self.index_x * square
            self.y = self.index_y * square

            self.old_x = self.index_x
            self.old_y = self.index_y

            self.blocked_facing = "right"

        self.image = self.animations[self.facing][0]
        self.rect = self.image.get_rect()

        self.delta_x, self.delta_y = self.rect.width // 2, self.rect.height // 8

        self.current_animation = 0

    def crossroad(self, x, y):
        can_move = []

        try:
            if not check_wall(x + 1, y):
                can_move.append("right")
            if not check_wall(x - 1, y):
                can_move.append("left")
            if not check_wall(x, y - 1):
                can_move.append("up")
            if not check_wall(x, y + 1):
                can_move.append("down")
        except IndexError:
            return [False, ["left", "right"]]

        if len(can_move) >= 3:
            return can_move
        return [False, can_move]

    def update(self):
        if self.eat:
            self.current_aim = self.house
        elif self.mode == RUN_UP_MODE and not self.in_house:
            self.current_aim = self.aim_run
        elif self.mode == PURSUIT_MODE and not self.in_house:
            if self.color == "red":
                self.current_aim = [self.pacman.index_x, self.pacman.index_y]
            elif self.color == "pink":
                pacman_facing = self.pacman.facing

                if pacman_facing == "right":
                    x, y = self.pacman.index_x + 4, self.pacman.index_y
                elif pacman_facing == "left":
                    x, y = self.pacman.index_x - 4, self.pacman.index_y
                elif pacman_facing == "up":
                    x, y = self.pacman.index_x, self.pacman.index_y - 4
                elif pacman_facing == "down":
                    x, y = self.pacman.index_x, self.pacman.index_y + 4

                if x >= len(game_board_copy[0]):
                    x = len(game_board_copy[0]) - 1
                elif x < 0:
                    x = 0
                elif y >= len(game_board_copy):
                    y = len(game_board_copy) - 1
                elif y < 0:
                    y = 0

                self.current_aim = [x, y]
            elif self.color == "blue":
                pacman_facing = self.pacman.facing

                if pacman_facing == "right":
                    x, y = self.pacman.index_x + 2, self.pacman.index_y
                elif pacman_facing == "left":
                    x, y = self.pacman.index_x - 2, self.pacman.index_y
                elif pacman_facing == "up":
                    x, y = self.pacman.index_x, self.pacman.index_y - 2
                elif pacman_facing == "down":
                    x, y = self.pacman.index_x, self.pacman.index_y + 2

                red_x, red_y = 0, 0

                for ghost in self.game.ghosts:
                    if ghost.color == "red":
                        red_x, red_y = ghost.index_x, ghost.index_y
                        break

                self.current_aim = [red_x + abs(x - red_x) * 2,
                                    red_y + abs(y - red_y) * 2]
            elif self.color == "yellow":
                pacman_s = self.pacman.index_x + self.pacman.index_y

                delta = abs(pacman_s - (self.index_x + self.index_y))

                if delta > 8:
                    self.current_aim = [self.pacman.index_x,
                                        self.pacman.index_y]
                else:
                    self.current_aim = self.aim_run

        if game_board[self.index_y][self.index_x] == 4:
            self.current_aim = [self.house_exit_x, self.house_exit_y]

        if self.moving:
            self.delta_x = 0

            if self.mode != ESCAPE_MODE or self.eat:
                directions = self.crossroad(self.index_x, self.index_y)

                if directions[0] and not self.new_crosroad:
                    if self.index_x != self.old_x and self.index_y != self.old_y:
                        self.blocked_facing = self.block_facing(self.facing)

                    variants = []

                    for direction in directions:
                        if direction != self.blocked_facing:
                            if direction == "up":
                                variants.append([abs(self.current_aim[
                                                         0] * square - self.x) + abs(
                                    self.current_aim[1] * square - (
                                                self.y - 1)), "up"])
                            elif direction == "down":
                                variants.append([abs(self.current_aim[
                                                         0] * square - self.x) + abs(
                                    self.current_aim[1] * square - (
                                                self.y + 1)), "down"])
                            elif direction == "left":
                                variants.append([abs(
                                    self.current_aim[0] * square - (
                                                self.x - 1)) + abs(
                                    self.current_aim[1] * square - self.y),
                                                 "left"])
                            else:
                                variants.append([abs(
                                    self.current_aim[0] * square - (
                                                self.x + 1)) + abs(
                                    self.current_aim[1] * square - self.y),
                                                 "right"])

                    self.facing = sorted(variants, key=lambda x: x[0])[0][1]

                    self.new_crosroad = True
            else:
                directions = self.crossroad(self.index_x, self.index_y)

                if directions[0] is False:
                    directions = directions[1]

                checked_directions = []

                for direction in directions:
                    if direction != self.blocked_facing:
                        checked_directions.append(direction)

                if self.index_y * square == self.y and self.index_x * square == self.x:
                    self.facing = random.choice(checked_directions)

                    self.blocked_facing = self.block_facing(self.facing)

            if self.facing == "left":
                if not check_wall(self.index_x - 1, self.index_y):
                    if self.x == (self.index_x - 1) * square:
                        self.old_x = self.index_x

                        self.index_x -= 1

                        if self.index_x < 1:
                            self.index_x = len(game_board_copy[0]) - 1
                            self.x = self.index_x * square
                            self.facing = "left"
                            self.blocked_facing = "right"

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

                        if self.index_x >= len(game_board_copy[0]) - 1:
                            self.index_x = 1
                            self.x = square
                            self.facing = "right"
                            self.blocked_facing = "left"

                        self.new_crosroad = False
                    else:
                        self.x += self.speed
                else:
                    self.blocked_facing = self.block_facing(self.facing)

                    try:
                        variants = self.change_direction(directions[1])
                    except IndexError:
                        variants = self.change_direction(directions[0])
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

            if game_board_copy[self.index_y][self.index_x] == 4:
                self.in_house = True

            if self.in_house and self.index_x == self.house_exit_x and self.index_y == self.house_exit_y:
                self.current_aim = self.aim_run
                self.in_house = False
            elif self.in_house and not self.eat:
                self.current_aim = [self.house_exit_x, self.house_exit_y]
            elif self.in_house and self.eat:
                self.current_aim = [self.house_exit_x, self.house_exit_y]
                self.eat = False
                self.speed = 4

        if self.mode != ESCAPE_MODE:
            self.image = self.animations[self.facing][self.current_animation]
        elif self.mode == ESCAPE_MODE and not self.eat and self.color_notify:
            self.image = self.color_escape_animations[self.current_animation]
        else:
            if self.eat:
                self.image = self.invisible_animations[self.facing][
                    self.current_animation]
            else:
                self.image = self.escape_animations[self.current_animation]
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x - self.delta_x,
                                   self.y - self.delta_y)

    def change_animation(self):
        if self.current_animation == 0:
            self.current_animation = 1
        elif self.current_animation == 1:
            self.current_animation = 0

        self.update()

    def block_facing(self, facing):
        if facing == "up":
            return "down"
        if facing == "down":
            return "up"
        if facing == "left":
            return "right"
        if facing == "right":
            return "left"

    def change_mode(self, mode):
        if self.mode == ESCAPE_MODE:
            self.eat = False
            self.color_notify = False

            self.speed = 4

        self.mode = mode

        self.blocked_facing = self.facing
        self.facing = self.block_facing(self.facing)

    def change_direction(self, directions):
        variants = []

        for direction in directions:
            if direction != self.blocked_facing:
                if direction == "up":
                    variants.append([abs(self.current_aim[0] - self.x) + abs(
                        self.current_aim[1] - (self.y - 1)), "up"])
                elif direction == "down":
                    variants.append([abs(self.current_aim[0] - self.x) + abs(
                        self.current_aim[1] - (self.y + 1)), "down"])
                elif direction == "left":
                    variants.append([abs(
                        self.current_aim[0] - (self.x - 1)) + abs(
                        self.current_aim[1] - self.y), "left"])
                else:
                    variants.append([abs(
                        self.current_aim[0] - (self.x + 1)) + abs(
                        self.current_aim[1] - self.y), "right"])

        return variants


def check_wall(x, y):
    try:
        if game_board[y][x] == 3:
            if x == 14 and y == 15:
                return False
            return True
        else:
            return False
    except IndexError:
        return True


class PacMan(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(all_sprites)
        self.index_x = 14
        self.index_y = 26

        self.x = self.index_x * square
        self.y = self.index_y * square

        self.speed = 4

        self.facing = "up"
        self.next_facing = None
        self.game = game

        self.died = False
        self.died_animation_started = False

        self.animations = {
            "up": [load_image("tile049.png"), load_image("tile051.png")],
            "left": [load_image("tile048.png"), load_image("tile050.png")],
            "right": [load_image("tile052.png"), load_image("tile054.png")],
            "down": [load_image("tile053.png"), load_image("tile055.png")],
            "spawn": load_image("tile112.png"),
            "death": [load_image("tile116.png"), load_image("tile117.png"),
                      load_image("tile118.png"), load_image("tile119.png"),
                      load_image("tile120.png"), load_image("tile121.png"),
                      load_image("tile122.png"), load_image("tile123.png"),
                      load_image("tile124.png"), load_image("tile125.png"),
                      load_image("tile126.png")]
        }

        self.image = self.animations[self.facing][0]
        self.rect = self.image.get_rect()

        self.delta_x, self.delta_y = self.rect.width // 2, self.rect.height // 8

        self.current_animation = 0
        self.sound_number = 1

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
        if self.next_facing is not None and not self.check_facing(
                self.next_facing):
            self.facing = self.next_facing
            self.next_facing = None

    def update(self):
        global can_press

        if self.moving:
            if self.facing == "up":
                if not check_wall(self.index_x, self.index_y - 1):
                    if self.y == (self.index_y - 1) * square:
                        self.index_y -= 1

                        self.checker()

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

                        if self.index_x == 0:
                            self.index_x = len(game_board_copy[0]) - 2
                            self.x = self.index_x * square

                        self.checker()

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

                        if self.index_x == len(game_board_copy[0]) - 1:
                            self.index_x = 1
                            self.x = square

                        self.checker()

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

                        self.checker()

                        game_board_copy[self.index_y][self.index_x] = 1

                        self.new_facing()
                    else:
                        self.y += self.speed
                else:
                    self.moving = False

        if not can_press:
            self.image = self.animations["spawn"]
        elif self.died:
            try:
                self.image = self.animations["death"][self.current_animation]
            except IndexError:
                self.game.restart()
        else:
            self.image = self.animations[self.facing][self.current_animation]
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x - self.delta_x,
                                   self.y - self.delta_y)

    def checker(self):
        if game_board_copy[self.index_y][self.index_x] == 6:
            self.game.ghost_mode(ESCAPE_MODE)
            print("Eat super-berry")
        elif game_board_copy[self.index_y][
            self.index_x] == 2 and self.game.mode != EATING_GAME_MODE:
            self.game.score += 10

            if self.sound_number == 1:
                EAT_BERRY_SOUND1.play(0)
                self.sound_number = 2
            else:
                EAT_BERRY_SOUND2.play(0)
                self.sound_number = 1
        elif game_board_copy[self.index_y][
            self.index_x] == 2 and self.game.mode == EATING_GAME_MODE:
            self.game.score += 10

    def change_animation(self):
        if self.current_animation == 0 and self.moving:
            self.current_animation = 1
        elif self.moving:
            self.current_animation = 0
        elif self.died and not self.died_animation_started:
            print(1)
            print(self.died, self.died_animation_started)
            print(self.moving)
            self.current_animation = 0
            self.died_animation_started = True
            DEATH_SOUND.play(0)
        elif self.died and self.died_animation_started:
            self.current_animation += 1

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
        self.pacman = PacMan(self)

        self.ghosts = []
        self.active_ghosts = []
        self.eated_ghosts = []

        self.score = 0

        self.mode = DEFAULT_GAME_MODE

        self.starting = True
        self.restarting = False
        self.gameover = False
        self.run_up_count = 0
        self.lives = 1
        self.current_player = 1
        self.draw_eat_scores = False

        self.run_up_timings = {0: 7000, 1: 7000, 2: 5000, 3: 5000}
        self.score_images = {
            200: load_image("tile104.png"), 400: load_image("tile105.png"),
            800: load_image("tile106.png"), 1600: load_image("tile107.png")
        }

        for color in ["red", "pink", "yellow", "blue"]:
            ghost = Ghost(color, self.pacman, self)

            ghosts.add(ghost)
            self.ghosts.append(ghost)

        self.group = group

    def restart(self):
        if self.current_player == 1:
            self.current_player = 2

            self.pacman.kill()

            self.pacman = PacMan(self)

            self.ghosts = []
            self.active_ghosts = []

            self.score = 0
            self.lives = 1

            self.mode = DEFAULT_GAME_MODE

            self.starting = True
            self.run_up_count = 0
            self.restarting = False

            for color in ["red", "pink", "yellow", "blue"]:
                ghost = Ghost(color, self.pacman, self)

                ghosts.add(ghost)
                self.ghosts.append(ghost)

            pygame.time.set_timer(ACTIVATE_RUN_UP, 0)
            pygame.time.set_timer(ACTIVATE_PURSUIT, 0)
            pygame.time.set_timer(ACTIVATE_ESCAPE, 0)
            pygame.time.set_timer(ESCAPE_OVER, 0)
        else:
            print("GAMEOVER")

    def update(self):
        render(screen)

        self.group.update()
        self.group.draw(screen)

        for ghost in self.ghosts:
            if ghost.index_x == self.pacman.index_x and ghost.index_y == self.pacman.index_y or self.restarting:
                if self.mode == DEFAULT_GAME_MODE or self.restarting:
                    self.lives -= 1

                    self.restarting = True

                    for ghost in ghosts:
                        ghost.kill()

                    self.pacman.died = True
                    self.pacman.moving = False
                else:
                    if ghost.color not in self.eated_ghosts:
                        print(f"Ghost {ghost.color} has been eat")

                        self.eated_ghosts.append(ghost.color)

                        EAT_GHOST_SOUND.play(0)

                        self.score += list(self.score_images.keys())[
                            len(self.eated_ghosts) - 1]

                        self.score_image = self.score_images[
                            list(self.score_images.keys())[
                                len(self.eated_ghosts) - 1]]
                        self.score_image_rect = self.score_image.get_rect(
                            center=(self.pacman.x, self.pacman.y))
                        screen.blit(self.score_image, self.score_image_rect)
                        self.draw_eat_scores = True

                        pygame.time.set_timer(STOP_DRAW_EAT_SCORES, 1000, 1)

                        ghost.eat = True
                        ghost.x = ghost.index_x * square
                        ghost.y = ghost.index_y * square
                        ghost.speed = 20

        if self.starting:
            START_SOUND.play(0)
            self.start_game()

        if self.draw_eat_scores:
            screen.blit(self.score_image, self.score_image_rect)

    def start_game(self):
        global can_press

        for ghost in self.ghosts:
            ghost.moving = False

        pygame.time.set_timer(GAME_START, 4000, 1)

        self.starting = False
        can_press = False

    def activate_game(self):
        global can_press

        can_press = True

        for ghost in self.ghosts:
            if ghost.color == "red":
                ghost.moving = True
                self.active_ghosts.append("red")
                break

        pygame.time.set_timer(GHOST_ADD, 2000, 3)

    def ghost_mode(self, mode):
        if mode == RUN_UP_MODE and not self.starting:
            if self.run_up_count < 3:
                self.run_up_count += 1
            else:
                return
        if self.mode != EATING_GAME_MODE:
            for ghost in self.ghosts:
                ghost.change_mode(mode)

            print(f"{mode} activated {datetime.datetime.now().time()}")

        if mode == RUN_UP_MODE and self.mode != EATING_GAME_MODE and not self.starting:
            pygame.time.set_timer(ACTIVATE_PURSUIT,
                                  self.run_up_timings[self.run_up_count], 1)
        elif mode == PURSUIT_MODE and self.run_up_count != 3 and self.mode != EATING_GAME_MODE:
            pygame.time.set_timer(ACTIVATE_RUN_UP, 20000, 1)
        elif mode == ESCAPE_MODE and not self.starting:
            self.mode = EATING_GAME_MODE

            self.pacman.x = self.pacman.index_x * square
            self.pacman.y = self.pacman.index_y * square
            self.pacman.speed = 5

            pygame.time.set_timer(ESCAPE_OVER, 0)
            pygame.time.set_timer(PLAY_SUPER_BERRY_SOUND, 0)

            pygame.time.set_timer(ESCAPE_OVER, 10000, 1)
            pygame.time.set_timer(PLAY_SUPER_BERRY_SOUND, 2100, 4)
            pygame.time.set_timer(COLOR_NOTIFY_ON, 7000, 1)

            SUPER_BERRY_SOUND.play(0)

        elif mode == ESCAPE_OVER_MODE and not self.starting:
            print("ESCAPE OVER")

            self.eated_ghosts = []

            self.pacman.x = self.pacman.index_x * square
            self.pacman.y = self.pacman.index_y * square
            self.pacman.speed = 4

            self.mode = DEFAULT_GAME_MODE
            for ghost in self.ghosts:
                ghost.change_mode(PURSUIT_MODE)
            pygame.time.set_timer(ACTIVATE_RUN_UP, 20000, 1)

    def ghost_add(self):
        for ghost in self.ghosts:
            if ghost.color not in self.active_ghosts:
                ghost.moving = True
                self.active_ghosts.append(ghost.color)
                break

        if len(self.active_ghosts) == 4:
            print("WAIT PURSUIT")
            pygame.time.set_timer(ACTIVATE_PURSUIT, 7000, 1)

    def ghost_notify(self):
        for ghost in self.ghosts:
            ghost.color_notify = True

    def draw_score(self):
        score = str(self.score)

        for i in range(len(score)):
            img = NUMBERS[int(score[i])]
            img_rect = img.get_rect(
                bottomleft=(i * square + square, square * 2))

            screen.blit(img, img_rect)

    def draw_player(self):
        for letter in range(len(PLAYER)):
            img = PLAYER[letter]
            img_rect = img.get_rect(
                bottomleft=(letter * square + (square * 10), square * 21))

            screen.blit(img, img_rect)

        img = NUMBERS[self.current_player]
        img_rect = img.get_rect(
            bottomleft=(letter * square + (square * 11), square * 21))

        screen.blit(img, img_rect)


def load_sound(name):
    fullname = os.path.join(os.path.join("data", "Music"), name)

    if not os.path.isfile(fullname):
        print(f"Файл с звуком '{fullname}' не найден")
        sys.exit()

    sound = pygame.mixer.Sound(fullname)

    return sound


def load_text(name):
    global square

    fullname = os.path.join(os.path.join("data", "TextImages"), name)

    if not os.path.isfile(fullname):
        print(f"Файл с текстом '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (square, square))

    return image


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
FPS = 60

ANIMATION_CHANGE = pygame.USEREVENT + 1
GAME_START = pygame.USEREVENT + 2
GHOST_ADD = pygame.USEREVENT + 3
ACTIVATE_PURSUIT = pygame.USEREVENT + 4
ACTIVATE_RUN_UP = pygame.USEREVENT + 5
ACTIVATE_ESCAPE = pygame.USEREVENT + 6
ESCAPE_OVER = pygame.USEREVENT + 7
PLAY_SUPER_BERRY_SOUND = pygame.USEREVENT + 8
STOP_DRAW_EAT_SCORES = pygame.USEREVENT + 9
COLOR_NOTIFY_ON = pygame.USEREVENT + 10
COLOR_NOTIFY = pygame.USEREVENT + 11

DEFAULT_GAME_MODE = "DEFAULT"
EATING_GAME_MODE = "EATING"

RUN_UP_MODE = "RUN"
PURSUIT_MODE = "PURSUIT"
ESCAPE_MODE = "ESCAPE"
ESCAPE_OVER_MODE = "OVER"

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("PacMan")
    pygame.time.set_timer(ANIMATION_CHANGE, 200)

    EAT_BERRY_SOUND1 = load_sound("munch_1.wav")
    EAT_BERRY_SOUND2 = load_sound("munch_2.wav")
    START_SOUND = load_sound("game_start.wav")
    DEATH_SOUND = load_sound("death_1.wav")
    SUPER_BERRY_SOUND = load_sound("power_pellet.wav")
    EAT_GHOST_SOUND = load_sound("eat_ghost.wav")

    square = 20
    width, height = (
    len(game_board_copy[0]) * square, len(game_board_copy) * square)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()

    NUMBERS = [
        load_text("tile032.png"), load_text("tile033.png"),
        load_text("tile034.png"), load_text("tile035.png"),
        load_text("tile036.png"), load_text("tile037.png"),
        load_text("tile038.png"), load_text("tile039.png"),
        load_text("tile040.png"), load_text("tile041.png")
    ]
    PLAYER = [
        load_text("tile016.png"), load_text("tile011.png"),
        load_text("tile000.png"), load_text("tile025.png"),
        load_text("tile004.png"), load_text("tile018.png")
    ]

    can_press = True
    game = Game(all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == ANIMATION_CHANGE:
                game.pacman.change_animation()

                for ghost in game.ghosts:
                    ghost.change_animation()

            if event.type == ACTIVATE_PURSUIT:
                game.ghost_mode(PURSUIT_MODE)
            if event.type == ACTIVATE_RUN_UP:
                game.ghost_mode(RUN_UP_MODE)
            if event.type == ESCAPE_OVER:
                game.ghost_mode(ESCAPE_OVER_MODE)

            if event.type == COLOR_NOTIFY_ON:
                game.ghost_notify()

            if event.type == PLAY_SUPER_BERRY_SOUND:
                SUPER_BERRY_SOUND.play(0)

            if event.type == STOP_DRAW_EAT_SCORES:
                game.draw_eat_scores = False

            if event.type == pygame.KEYDOWN and can_press:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    game.pacman.move("right")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    game.pacman.move("down")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    game.pacman.move("left")
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    game.pacman.move("up")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

            if event.type == GAME_START:
                game.activate_game()

            if event.type == GHOST_ADD:
                game.ghost_add()

        game.update()
        game.draw_score()

        if not can_press:
            game.draw_player()

        pygame.display.flip()

    pygame.quit()
