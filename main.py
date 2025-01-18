import os
from rich import print
from time import sleep
import copy


class Wall:
    def __init__(self, direction):
        self.is_blocking = False
        if direction == 'H':
            self.char = '-'
        elif direction == 'V':
            self.char = '|'
        self.color = "bold bright_white"

    def wall_activation(self):
        self.is_blocking = True
        self.color = "bold bright_yellow"


class Center:
    def __init__(self):
        self.is_activated = False
        self.char = "x"
        self.direction = None
        self.color = "bold bright_white"

    def center_activation(self, direction):
        self.is_activated = True
        self.color = "bold bright_yellow"
        self.direction = direction


class Entry:
    def __init__(self):
        self.containing_ball = False
        self.char = ' '
        self.color = "unknown"
        self.neighbors = {'U': True, 'R': True, 'D': True, 'L': True, 'UU': False, 'RR': False, 'DD': False,
                          'LL': False,
                          'UL': False, 'UR': False, 'DR': False, 'DL': False}

    def moving_ball_to(self, player_color):
        self.containing_ball = True
        self.char = 'O'
        self.color = player_color

    def moving_ball_from(self):
        self.containing_ball = False
        self.char = ' '
        self.color = "unknown"

    def add_limit(self, key):
        self.neighbors[key] = False

    def del_limit(self, key):
        self.neighbors[key] = True


class Table:
    def __init__(self):
        self.table = [["" for _ in range(17)] for _ in range(17)]
        for i in range(17):
            for j in range(17):
                if i % 2 == 0 and j % 2 == 0:
                    self.table[i][j] = Entry()
                    if i == 0:
                        self.table[i][j].add_limit('U')
                    elif i == 16:
                        self.table[i][j].add_limit('D')
                    if j == 0:
                        self.table[i][j].add_limit('L')
                    elif j == 16:
                        self.table[i][j].add_limit('R')
                elif i % 2 == 0 and j % 2 != 0:
                    self.table[i][j] = Wall('V')
                elif i % 2 != 0 and j % 2 == 0:
                    self.table[i][j] = Wall('H')
                else:
                    self.table[i][j] = Center()
        self.centers = set([(x, y) for x in range(1, 16, 2) for y in range(1, 16, 2)])

    def print_table(self):
        for i in range(17):
            for j in range(17):
                print(f"[{self.table[i][j].color}]{self.table[i][j].char}[/{self.table[i][j].color}]", end=" ")
            print()


class Player:
    def __init__(self, user_name, x, y, row, player_color):
        self.name = user_name
        self.pos_x = x
        self.pos_y = y
        self.target_row = row
        self.color = player_color
        self.num_wall = 10
        self.num_wall_per_turn = 128

    def change_pos(self, delta_x, delta_y):
        self.pos_x += delta_x
        self.pos_y += delta_y


class Game:
    def __init__(self, game_id, user_1, user_2):
        self.id = game_id
        self.table = Table()
        self.is_finished = False
        self.first_player = Player(user_1, 16, 8, 0, "bold magenta")
        self.second_player = Player(user_2, 0, 8, 16, "bold bright_cyan")
        self.turn = 0
        self.time = 0
        self.moves = {'U': (-2, 0), 'R': (0, 2), 'D': (2, 0), 'L': (0, -2), 'UU': (-4, 0), 'RR': (0, 4),
                      'DD': (4, 0), 'LL': (0, -4), 'UL': (-2, -2), 'UR': (-2, 2), 'DR': (2, 2), 'DL': (2, -2)}
        self.is_putting_wall_possilble = True

    def clear_terminal(self, time):
        sleep(time)
        os.system('clear')

    def valid_moves(self, player, x, y):
        self.clear_terminal(1)
        self.table.print_table()
        print(f"[bold green]{player.name} please choose one of the valid moves below ![/bold green]")
        valid_moves = []
        for move in self.table.table[x][y].neighbors.keys():
            if self.table.table[x][y].neighbors[move]:
                valid_moves.append(move)
                print(f"[bold green]{move}[/bold green]", end=" ")
        print()
        move = input()
        if move in valid_moves:
            return move
        else:
            print("[bold red1]oops ! invalid move is chosen .[/bold red1]")
            return self.valid_moves(player, x, y)

    def is_terminated(self, player):
        if player.pos_x == player.target_row:
            print(f"[bold green]{player.name} won the game ![/bold green]")
            return True
        else:
            return False

    def update_position_ball_elimination(self, current_x, current_y, direction):
        lower_bound = 0
        upper_bound = 16
        up_wall = (-1, 0)
        down_wall = (1, 0)
        right_wall = (0, 1)
        left_wall = (0, -1)
        if direction in set(['U', 'D']):
            if direction == 'U':
                up_neighbor = (-2, 0)
                if current_x > lower_bound and not self.table.table[current_x + up_wall[0]][current_y].is_blocking and \
                        self.table.table[current_x + up_neighbor[0]][current_y + up_neighbor[1]].containing_ball:
                    if current_x + up_neighbor[0] == lower_bound or \
                            self.table.table[current_x + up_neighbor[0] + up_wall[0]][current_y].is_blocking:
                        if current_y < upper_bound and not self.table.table[current_x + up_neighbor[0]][
                            current_y + right_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction + 'R')
                        if current_y > lower_bound and not self.table.table[current_x + up_neighbor[0]][
                            current_y + left_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction + 'L')
                    else:
                        self.table.table[current_x][current_y].add_limit(direction * 2)
            else:
                down_neighbor = (2, 0)
                if current_x < upper_bound and not self.table.table[current_x + down_wall[0]][current_y].is_blocking and \
                        self.table.table[current_x + down_neighbor[0]][current_y + down_neighbor[1]].containing_ball:
                    if current_x + down_neighbor[0] == upper_bound or \
                            self.table.table[current_x + down_neighbor[0] + down_wall[0]][current_y].is_blocking:
                        if current_y < upper_bound and not self.table.table[current_x + down_neighbor[0]][
                            current_y + right_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction + 'R')
                        if current_y > lower_bound and not self.table.table[current_x + down_neighbor[0]][
                            current_y + left_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction + 'L')
                    else:
                        self.table.table[current_x][current_y].add_limit(direction * 2)
        else:
            if direction == 'R':
                right_neighbor = (0, 2)
                if current_y < upper_bound and not self.table.table[current_x][
                    current_y + right_wall[1]].is_blocking and self.table.table[current_x + right_neighbor[0]][
                    current_y + right_neighbor[1]].containing_ball:
                    if current_y + right_neighbor[1] == upper_bound or self.table.table[current_x][
                        current_y + right_neighbor[1] + right_wall[1]].is_blocking:
                        if current_x > lower_bound and not self.table.table[current_x + up_wall[0]][
                            current_y + right_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('U' + direction)
                        if current_x < upper_bound and not self.table.table[current_x + down_wall[0]][
                            current_y + right_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('D' + direction)
                    else:
                        self.table.table[current_x][current_y].add_limit(direction * 2)
            else:
                left_neighbor = (0, -2)
                if current_y > lower_bound and not self.table.table[current_x][current_y + left_wall[1]].is_blocking and \
                        self.table.table[current_x + left_neighbor[0]][current_y + left_neighbor[1]].containing_ball:
                    if current_y + left_neighbor[1] == lower_bound or self.table.table[current_x][
                        current_y + left_neighbor[1] + left_wall[1]]:
                        if current_x > lower_bound and not self.table.table[current_x + up_wall[0]][
                            current_y + left_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('U' + direction)
                        if current_x < upper_bound and not self.table.table[current_x + down_wall[0]][
                            current_y + left_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('D' + direction)
                    else:
                        self.table.table[current_x][current_y].add_limit(direction * 2)

    def update_neighbors_ball_elimination(self, current_x, current_y, direction):
        lower_bound = 0
        upper_bound = 16
        up_wall = (-1, 0)
        down_wall = (1, 0)
        right_wall = (0, 1)
        left_wall = (0, -1)
        if direction in set(['U', 'D']):
            opposite_direction = max(set(['U', 'D']).difference(set([direction])))
            if direction == 'U':
                up_neighbor = (-2, 0)
                if current_x > lower_bound and not self.table.table[current_x + up_wall[0]][
                    current_y + up_wall[1]].is_blocking:
                    self.table.table[current_x + up_neighbor[0]][current_y + up_neighbor[1]].del_limit(
                        opposite_direction)
                    if self.table.table[current_x + up_neighbor[0]][current_y + up_neighbor[1]].containing_ball:
                        if current_x == upper_bound or self.table.table[current_x + down_wall[0]][
                            current_y + down_wall[1]].is_blocking:
                            if current_y < upper_bound and not self.table.table[current_x + right_wall[0]][
                                current_y + right_wall[1]].is_blocking:
                                self.table.table[current_x + up_neighbor[0]][current_y + up_neighbor[1]].add_limit(
                                    opposite_direction + 'R')
                            if current_y > lower_bound and not self.table.table[current_x + left_wall[0]][
                                current_y + left_wall[1]].is_blocking:
                                self.table.table[current_x + up_neighbor[0]][current_y + up_neighbor[1]].add_limit(
                                    opposite_direction + 'L')
                        else:
                            self.table.table[current_x + up_neighbor[0]][current_y + up_neighbor[1]].add_limit(
                                opposite_direction * 2)
            else:
                down_neighbor = (2, 0)
                if current_x < upper_bound and not self.table.table[current_x + down_wall[0]][
                    current_y + down_wall[1]].is_blocking:
                    self.table.table[current_x + down_neighbor[0]][current_y + down_neighbor[1]].del_limit(
                        opposite_direction)
                    if self.table.table[current_x + down_neighbor[0]][current_y + down_neighbor[1]].containing_ball:
                        if current_x == lower_bound or self.table.table[current_x + up_wall[0]][
                            current_y + up_wall[1]].is_blocking:
                            if current_y < upper_bound and not self.table.table[current_x + right_wall[0]][
                                current_y + right_wall[1]].is_blocking:
                                self.table.table[current_x + down_neighbor[0]][current_y + down_neighbor[1]].add_limit(
                                    opposite_direction + 'R')
                            if current_y > lower_bound and not self.table.table[current_x + left_wall[0]][
                                current_y + left_wall[1]].is_blocking:
                                self.table.table[current_x + down_neighbor[0]][current_y + down_neighbor[1]].add_limit(
                                    opposite_direction + 'L')
                        else:
                            self.table.table[current_x + down_neighbor[0]][current_y + down_neighbor[1]].add_limit(
                                opposite_direction * 2)
        elif direction in set(['R', 'L']):
            opposite_direction = max(set(['R', 'L']).difference(set([direction])))
            if direction == 'R':
                right_neighbor = (0, 2)
                if current_y < upper_bound and not self.table.table[current_x + right_wall[0]][
                    current_y + right_wall[1]].is_blocking:
                    self.table.table[current_x + right_neighbor[0]][current_y + right_neighbor[1]].del_limit(
                        opposite_direction)
                    if self.table.table[current_x + right_neighbor[0]][current_y + right_neighbor[1]].containing_ball:
                        if current_y == lower_bound or self.table.table[current_x + left_wall[0]][
                            current_y + left_wall[1]].is_blocking:
                            if current_x > lower_bound and not self.table.table[current_x + up_wall[0]][
                                current_y + up_wall[1]].is_blocking:
                                self.table.table[current_x + right_neighbor[0]][
                                    current_y + right_neighbor[1]].add_limit('U' + opposite_direction)
                            if current_x < upper_bound and not self.table.table[current_x + down_wall[0]][
                                current_y + down_wall[1]].is_blocking:
                                self.table.table[current_x + right_neighbor[0]][
                                    current_y + right_neighbor[1]].add_limit('D' + opposite_direction)
                        else:
                            self.table.table[current_x + right_neighbor[0]][current_y + right_neighbor[1]].add_limit(
                                opposite_direction * 2)
            else:
                left_neighbor = (0, -2)
                if current_y > lower_bound and not self.table.table[current_x + left_wall[0]][
                    current_y + left_wall[1]].is_blocking:
                    self.table.table[current_x + left_neighbor[0]][current_y + left_neighbor[1]].del_limit(
                        opposite_direction)
                    if self.table.table[current_x + left_neighbor[0]][current_y + left_neighbor[1]].containing_ball:
                        if current_y == upper_bound or self.table.table[current_x + right_wall[0]][
                            current_y + right_wall[1]].is_blocking:
                            if current_x > lower_bound and not self.table.table[current_x + up_wall[0]][
                                current_y + up_wall[1]].is_blocking:
                                self.table.table[current_x + left_neighbor[0]][current_y + left_neighbor[1]].add_limit(
                                    'U' + opposite_direction)
                            if current_x < upper_bound and not self.table.table[current_x + down_wall[0]][
                                current_y + down_wall[1]].is_blocking:
                                self.table.table[current_x + left_neighbor[0]][current_y + left_neighbor[1]].add_limit(
                                    'D' + opposite_direction)
                        else:
                            self.table.table[current_x + left_neighbor[0]][current_y + left_neighbor[1]].add_limit(
                                opposite_direction * 2)

    def update_position_ball_addition(self, new_x, new_y, direction):
        lower_bound = 0
        upper_bound = 16
        up_wall = (-1, 0)
        down_wall = (1, 0)
        right_wall = (0, 1)
        left_wall = (0, -1)
        if direction in set(['U', 'D']):
            if direction == 'U':
                up_neighbor = (-2, 0)
                if new_x > lower_bound and not self.table.table[new_x + up_wall[0]][new_y].is_blocking and \
                        self.table.table[new_x + up_neighbor[0]][new_y + up_neighbor[1]].containing_ball:
                    if new_x + up_neighbor[0] == lower_bound or self.table.table[new_x + up_neighbor[0] + up_wall[0]][
                        new_y].is_blocking:
                        if new_y < upper_bound and not self.table.table[new_x + up_neighbor[0]][
                            new_y + right_wall[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit(direction + 'R')
                        if new_y > lower_bound and not self.table.table[new_x + up_neighbor[0]][
                            new_y + left_wall[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit(direction + 'L')
                    else:
                        self.table.table[new_x][new_y].del_limit(direction * 2)
            else:
                down_neighbor = (2, 0)
                if new_x < upper_bound and not self.table.table[new_x + down_wall[0]][new_y].is_blocking and \
                        self.table.table[new_x + down_neighbor[0]][new_y + down_neighbor[1]].containing_ball:
                    if new_x + down_neighbor[0] == upper_bound or \
                            self.table.table[new_x + down_neighbor[0] + down_wall[0]][new_y].is_blocking:
                        if new_y < upper_bound and not self.table.table[new_x + down_neighbor[0]][
                            new_y + right_wall[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit(direction + 'R')
                        if new_y > lower_bound and not self.table.table[new_x + down_neighbor[0]][
                            new_y + left_wall[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit(direction + 'L')
                    else:
                        self.table.table[new_x][new_y].del_limit(direction * 2)
        else:
            if direction == 'R':
                right_neighbor = (0, 2)
                if new_y < upper_bound and not self.table.table[new_x][new_y + right_wall[1]].is_blocking and \
                        self.table.table[new_x + right_neighbor[0]][new_y + right_neighbor[1]].containing_ball:
                    if new_y + right_neighbor[1] == upper_bound or self.table.table[new_x][
                        new_y + right_neighbor[1] + right_wall[1]].is_blocking:
                        if new_x > lower_bound and not self.table.table[new_x + up_wall[0]][
                            new_y + right_neighbor[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit('U' + direction)
                        if new_x < upper_bound and not self.table.table[new_x + down_wall[0]][
                            new_y + right_neighbor[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit('D' + direction)
                    else:
                        self.table.table[new_x][new_y].del_limit(direction * 2)
            else:
                left_neighbor = (0, -2)
                if new_y > lower_bound and not self.table.table[new_x][new_y + left_wall[1]].is_blocking and \
                        self.table.table[new_x + left_neighbor[0]][new_y + left_neighbor[1]].containing_ball:
                    if new_y + left_neighbor[1] == lower_bound or self.table.table[new_x][
                        new_y + left_neighbor[1] + left_wall[1]]:
                        if new_x > lower_bound and not self.table.table[new_x + up_wall[0]][
                            new_y + left_neighbor[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit('U' + direction)
                        if new_x < upper_bound and not self.table.table[new_x + down_wall[0]][
                            new_y + left_neighbor[1]].is_blocking:
                            self.table.table[new_x][new_y].del_limit('D' + direction)
                    else:
                        self.table.table[new_x][new_y].del_limit(direction * 2)

    def update_neighbors_ball_addition(self, new_x, new_y, direction):
        lower_bound = 0
        upper_bound = 16
        up_wall = (-1, 0)
        down_wall = (1, 0)
        right_wall = (0, 1)
        left_wall = (0, -1)
        if direction in set(['U', 'D']):
            opposite_direction = max(set(['U', 'D']).difference(set([direction])))
            if direction == 'U':
                up_neighbor = (-2, 0)
                if new_x > lower_bound and not self.table.table[new_x + up_wall[0]][new_y + up_wall[1]].is_blocking:
                    self.table.table[new_x + up_neighbor[0]][new_y + up_neighbor[1]].add_limit(opposite_direction)
                    if self.table.table[new_x + up_neighbor[0]][new_y + up_neighbor[1]].containing_ball:
                        if new_x == upper_bound or self.table.table[new_x + down_wall[0]][
                            new_y + down_wall[1]].is_blocking:
                            if new_y < upper_bound and not self.table.table[new_x + right_wall[0]][
                                new_y + right_wall[1]].is_blocking:
                                self.table.table[new_x + up_neighbor[0]][new_y + up_neighbor[1]].del_limit(
                                    opposite_direction + 'R')
                            if new_y > lower_bound and not self.table.table[new_x + left_wall[0]][
                                new_y + left_wall[1]].is_blocking:
                                self.table.table[new_x + up_neighbor[0]][new_y + up_neighbor[1]].del_limit(
                                    opposite_direction + 'L')
                        else:
                            self.table.table[new_x + up_neighbor[0]][new_y + up_neighbor[1]].del_limit(
                                opposite_direction * 2)
            else:
                down_neighbor = (2, 0)
                if new_x < upper_bound and not self.table.table[new_x + down_wall[0]][new_y + down_wall[1]].is_blocking:
                    self.table.table[new_x + down_neighbor[0]][new_y + down_neighbor[1]].add_limit(opposite_direction)
                    if self.table.table[new_x + down_neighbor[0]][new_y + down_neighbor[1]].containing_ball:
                        if new_x == lower_bound or self.table.table[new_x + up_wall[0]][new_y + up_wall[1]].is_blocking:
                            if new_y < upper_bound and not self.table.table[new_x + right_wall[0]][
                                new_y + right_wall[1]].is_blocking:
                                self.table.table[new_x + down_neighbor[0]][new_y + down_neighbor[1]].del_limit(
                                    opposite_direction + 'R')
                            if new_y > lower_bound and not self.table.table[new_x + left_wall[0]][
                                new_y + left_wall[1]].is_blocking:
                                self.table.table[new_x + down_neighbor[0]][new_y + down_neighbor[1]].del_limit(
                                    opposite_direction + 'L')
                        else:
                            self.table.table[new_x + down_neighbor[0]][new_y + down_neighbor[1]].del_limit(
                                opposite_direction * 2)
        elif direction in set(['R', 'L']):
            opposite_direction = max(set(['R', 'L']).difference(set([direction])))
            if direction == 'R':
                right_neighbor = (0, 2)
                if new_y < upper_bound and not self.table.table[new_x + right_wall[0]][
                    new_y + right_wall[1]].is_blocking:
                    self.table.table[new_x + right_neighbor[0]][new_y + right_neighbor[1]].add_limit(opposite_direction)
                    if self.table.table[new_x + right_neighbor[0]][new_y + right_neighbor[1]].containing_ball:
                        if new_y == lower_bound or self.table.table[new_x + left_wall[0]][
                            new_y + left_wall[1]].is_blocking:
                            if new_x > lower_bound and not self.table.table[new_x + up_wall[0]][
                                new_y + up_wall[1]].is_blocking:
                                self.table.table[new_x + right_neighbor[0]][new_y + right_neighbor[1]].del_limit(
                                    'U' + opposite_direction)
                            if new_x < upper_bound and not self.table.table[new_x + down_wall[0]][
                                new_y + down_wall[1]].is_blocking:
                                self.table.table[new_x + right_neighbor[0]][new_y + right_neighbor[1]].del_limit(
                                    'D' + opposite_direction)
                        else:
                            self.table.table[new_x + right_neighbor[0]][new_y + right_neighbor[1]].del_limit(
                                opposite_direction * 2)
            else:
                left_neighbor = (0, -2)
                if new_y > lower_bound and not self.table.table[new_x + left_wall[0]][new_y + left_wall[1]].is_blocking:
                    self.table.table[new_x + left_neighbor[0]][new_y + left_neighbor[1]].add_limit(opposite_direction)
                    if self.table.table[new_x + left_neighbor[0]][new_y + left_neighbor[1]].containing_ball:
                        if new_y == upper_bound or self.table.table[new_x + right_wall[0]][
                            new_y + right_wall[1]].is_blocking:
                            if new_x > lower_bound and not self.table.table[new_x + up_wall[0]][
                                new_y + up_wall[1]].is_blocking:
                                self.table.table[new_x + left_neighbor[0]][new_y + left_neighbor[1]].del_limit(
                                    'U' + opposite_direction)
                            if new_x < upper_bound and not self.table.table[new_x + down_wall[0]][
                                new_y + down_wall[1]].is_blocking:
                                self.table.table[new_x + left_neighbor[0]][new_y + left_neighbor[1]].del_limit(
                                    'D' + opposite_direction)
                        else:
                            self.table.table[new_x + left_neighbor[0]][new_y + left_neighbor[1]].del_limit(
                                opposite_direction * 2)

    def complete_primary_table(self):
        self.table.table[0][8].moving_ball_to(self.first_player.color)
        self.table.table[16][8].moving_ball_to(self.second_player.color)
        for direction in ['U', 'R', 'D', 'L']:
            self.update_neighbors_ball_addition(0, 8, direction)
            self.update_neighbors_ball_addition(16, 8, direction)

    def update_entries_wall_addition(self, wall_x, wall_y, direction):
        lower_bound = 0
        upper_bound = 16
        up_wall = (-1, 0)
        down_wall = (1, 0)
        right_wall = (0, 1)
        left_wall = (0, -1)
        if direction == 'H':
            first_up_neighbor = (-1, 0)
            second_up_neighbor = (-3, 0)
            first_down_neighbor = (1, 0)
            second_down_neighbor = (3, 0)

            for move in self.table.table[wall_x + first_up_neighbor[0]][wall_y].neighbors.keys():
                if 'D' in move:
                    self.table.table[wall_x + first_up_neighbor[0]][wall_y].add_limit(move)

            for move in self.table.table[wall_x + first_down_neighbor[0]][wall_y].neighbors.keys():
                if 'U' in move:
                    self.table.table[wall_x + first_down_neighbor[0]][wall_y].add_limit(move)

            if self.table.table[wall_x + first_up_neighbor[0]][wall_y].containing_ball:
                if wall_x + first_up_neighbor[0] > lower_bound and not \
                self.table.table[wall_x + first_up_neighbor[0] + up_wall[0]][wall_y].is_blocking and \
                        self.table.table[wall_x + second_up_neighbor[0]][wall_y].containing_ball:
                    self.table.table[wall_x + second_up_neighbor[0]][wall_y].add_limit('DD')
                    if wall_y < upper_bound and not self.table.table[wall_x + first_up_neighbor[0]][
                        wall_y + right_wall[1]].is_blocking:
                        self.table.table[wall_x + second_up_neighbor[0]][wall_y].del_limit('DR')
                    if wall_y > lower_bound and not self.table.table[wall_x + first_up_neighbor[0]][
                        wall_y + left_wall[1]].is_blocking:
                        self.table.table[wall_x + second_up_neighbor[0]][wall_y].del_limit('DL:')

            if self.table.table[wall_x + first_down_neighbor[0]][wall_y].containing_ball:
                if wall_x + first_down_neighbor[0] < upper_bound and not \
                self.table.table[wall_x + first_down_neighbor[0] + down_wall[0]][wall_y].is_blocking and \
                        self.table.table[wall_x + second_down_neighbor[0]][wall_y].containing_ball:
                    self.table.table[wall_x + second_down_neighbor[0]][wall_y].add_limit('UU')
                    if wall_y < upper_bound and not self.table.table[wall_x + first_down_neighbor[0]][
                        wall_y + right_wall[1]].is_blocking:
                        self.table.table[wall_x + second_down_neighbor[0]][wall_y].del_limit('UR')
                    if wall_y > lower_bound and not self.table.table[wall_x + first_down_neighbor[0]][
                        wall_y + left_wall[1]].is_blocking:
                        self.table.table[wall_x + second_down_neighbor[0]][wall_y].del_limit('UL')
        else:
            first_right_neighbor = (0, 1)
            second_right_neighbor = (0, 3)
            first_left_neighbor = (0, -1)
            second_left_neighbor = (0, -3)
            for move in self.table.table[wall_x][wall_y + first_right_neighbor[1]].neighbors.keys():
                if 'L' in move:
                    self.table.table[wall_x][wall_y + first_right_neighbor[1]].add_limit(move)

            for move in self.table.table[wall_x][wall_y + first_left_neighbor[1]].neighbors.keys():
                if 'R' in move:
                    self.table.table[wall_x][wall_y + first_left_neighbor[1]].add_limit(move)

            if self.table.table[wall_x][wall_y + first_right_neighbor[1]].containing_ball:
                if wall_y + first_right_neighbor[1] < upper_bound and not self.table.table[wall_x][
                    wall_y + first_right_neighbor[1] + right_wall[1]].is_blocking and self.table.table[wall_x][
                    wall_y + second_right_neighbor[1]].containing_ball:
                    self.table.table[wall_x][wall_y + second_right_neighbor[1]].add_limit('LL')
                    if wall_x > lower_bound and not self.table.table[wall_x + up_wall[0]][
                        wall_y + first_right_neighbor[1]].is_blocking:
                        self.table.table[wall_x][wall_y + second_right_neighbor[1]].del_limit('UL')
                    if wall_x < upper_bound and not self.table.table[wall_x + down_wall[0]][
                        wall_y + first_right_neighbor[1]].is_blocking:
                        self.table.table[wall_x][wall_y + second_right_neighbor[1]].del_limit('DL')

            if self.table.table[wall_x][wall_y + first_left_neighbor[1]].containing_ball:
                if wall_y + first_left_neighbor[1] > lower_bound and not self.table.table[wall_x][
                    wall_y + first_left_neighbor[1] + left_wall[1]].is_blocking and self.table.table[wall_x][
                    wall_y + second_left_neighbor[1]].containing_ball:
                    self.table.table[wall_x][wall_y + second_left_neighbor[1]].add_limit('RR')
                    if wall_x > lower_bound and not self.table.table[wall_x + up_wall[0]][
                        wall_y + first_left_neighbor[1]].is_blocking:
                        self.table.table[wall_x][wall_y + second_left_neighbor[1]].del_limit('UR')
                    if wall_x < upper_bound and not self.table.table[wall_x + down_wall[0]][
                        wall_y + first_left_neighbor[1]].is_blocking:
                        self.table.table[wall_x][wall_y + second_left_neighbor[1]].del_limit('DR')

    def wall_overlap_detection(self, x, y, direction):
        if x > 1 and self.table.table[x - 2][y].direction == direction and direction == 'V':
            return True
        if x < 15 and self.table.table[x + 2][y].direction == direction and direction == 'V':
            return True
        if y > 1 and self.table.table[x][y - 2].direction == direction and direction == 'H':
            return True
        if y < 15 and self.table.table[x][y + 2].direction == direction and direction == 'H':
            return True
        return False

    def dfs(self, player, visited):
        visited[(player.pos_x, player.pos_y)] = True
        if player.pos_x == player.target_row:
            return True
        for move in self.table.table[player.pos_x][player.pos_y].neighbors.keys():
            if self.table.table[player.pos_x][player.pos_y].neighbors[move] and not visited[
                (player.pos_x + self.moves[move][0], player.pos_y + self.moves[move][1])]:
                game_copy = copy.deepcopy(self)
                player_copy = copy.deepcopy(player)
                for direction in ['U', 'R', 'D', 'L']:
                    game_copy.update_neighbors_ball_elimination(player_copy.pos_x, player_copy.pos_y, direction)
                    game_copy.update_position_ball_elimination(player_copy.pos_x, player_copy.pos_y, direction)
                game_copy.table.table[player_copy.pos_x][player_copy.pos_y].moving_ball_from()
                player_copy.change_pos(self.moves[move][0], self.moves[move][1])
                for direction in ['U', 'R', 'D', 'L']:
                    game_copy.update_neighbors_ball_addition(player_copy.pos_x, player_copy.pos_y, direction)
                    game_copy.update_position_ball_addition(player_copy.pos_x, player_copy.pos_y, direction)
                self.table.table[player_copy.pos_x][player_copy.pos_y].moving_ball_to(player_copy.color)
                if game_copy.dfs(player_copy, visited):
                    del game_copy
                    del player_copy
                    return True
                del game_copy
                del player_copy
        return False

    def put_valid_wall(self, player):
        if player.num_wall_per_turn == 0:
            return -1, -1, -1
        else:
            self.clear_terminal(1)
            self.table.print_table()
            print(
                f"[bold green]{player.name} please enter a pair of positive odd numbers less equal 15 as the coordinate of a center ![bold blue] (example : x y)[/bold blue][/bold green]")
            try:
                x, y = [int(x) for x in input().split()]
            except:
                print("[bold red1]oops ! the format of input is invalid ![/bold red1]")
                return self.put_valid_wall(player)
            if (x, y) in self.table.centers:
                if self.table.table[x][y].is_activated:
                    print("[bold red1]oops ! overlapping walls .[/bold red1]")
                    player.num_wall_per_turn -= 1
                    return self.put_valid_wall(player)
                else:
                    print(
                        f"[bold green]{player.name} please choose one of the directions below for your wall .[/bold green]")
                    print("[bold green]H : horizontal\tV : vertical[/bold green]")
                    direction = input()
                    if not direction in ['H', 'V']:
                        print("[bold red1]oops ! invalid direction is given .[/bold red1]")
                        return self.put_valid_wall(player)
                    else:
                        if self.wall_overlap_detection(x, y, direction):
                            print("[bold red1]oops ! overlapping walls .[/bold red1]")
                            player.num_wall_per_turn -= 1
                            return self.put_valid_wall(player)
                        else:
                            visited = dict([((x, y), False) for x in range(0, 17, 2) for y in range(0, 17, 2)])
                            game_copy = copy.deepcopy(self)
                            if direction == 'H':
                                game_copy.update_entries_wall_addition(x, y - 1, 'H')
                                game_copy.update_entries_wall_addition(x, y + 1, 'H')
                            else:
                                game_copy.update_entries_wall_addition(x - 1, y, 'V')
                                game_copy.update_entries_wall_addition(x + 1, y, 'V')
                            if game_copy.dfs(game_copy.first_player, visited.copy()) and game_copy.dfs(
                                    game_copy.second_player, visited.copy()):
                                del game_copy
                                del visited
                                return x, y, direction
                            else:
                                print("[bold red1]oops ! your choice blocked all the possible paths .[/bold red1]")
                                player.num_wall_per_turn -= 1
                                return self.put_valid_wall(player)
            else:
                print("[bold red1]oops ! invalid numbers are entered .[/bold red1]")
                return self.put_valid_wall(player)

    def play(self):
        self.clear_terminal(1.5)

        if self.time == 0:
            self.complete_primary_table()

        if self.turn == 0:
            player = self.first_player
        else:
            player = self.second_player

        print(f"[bold green]{player.name} please choose one of the options below ![/bold green]")
        if player.num_wall != 0 and self.is_putting_wall_possilble:
            player.num_wall_per_turn = 128
            print("[bold green]M : move\tW : wall\tQ : quit[/bold green]")
        else:
            print("[bold green]M : move\tQ : quit[/bold green]")

        print(f"[bold blue]number of your remaining walls : {player.num_wall}[/bold blue]")
        request = input()

        if request == "M":
            move = self.valid_moves(player, player.pos_x, player.pos_y)
            for direction in ['U', 'R', 'D', 'L']:
                self.update_neighbors_ball_elimination(player.pos_x, player.pos_y, direction)
                self.update_position_ball_elimination(player.pos_x, player.pos_y, direction)
            self.table.table[player.pos_x][player.pos_y].moving_ball_from()
            player.change_pos(self.moves[move][0], self.moves[move][1])
            for direction in ['U', 'R', 'D', 'L']:
                self.update_neighbors_ball_addition(player.pos_x, player.pos_y, direction)
                self.update_position_ball_addition(player.pos_x, player.pos_y, direction)
            self.table.table[player.pos_x][player.pos_y].moving_ball_to(player.color)
            self.clear_terminal(1)
            self.table.print_table()
            if self.is_terminated(player):
                self.is_finished = True
                self.clear_terminal(1.5)
                return "T"
            else:
                self.turn ^= 1
                self.time += 1
                return "S"

        elif request == "W" and player.num_wall != 0 and self.is_putting_wall_possilble:
            center_x, center_y, direction = self.put_valid_wall(player)
            if center_x == -1:
                self.is_putting_wall_possilble = False
                return self.play()
            else:
                player.num_wall -= 1
                if direction == 'H':
                    self.update_entries_wall_addition(center_x, center_y - 1, 'H')
                    self.update_entries_wall_addition(center_x, center_y + 1, 'H')
                else:
                    self.update_entries_wall_addition(center_x - 1, center_y, 'V')
                    self.update_entries_wall_addition(center_x + 1, center_y, 'V')
                self.table.table[center_x][center_y].center_activation(direction)
                if direction == 'H':
                    self.table.table[center_x][center_y - 1].wall_activation()
                    self.table.table[center_x][center_y + 1].wall_activation()
                else:
                    self.table.table[center_x - 1][center_y].wall_activation()
                    self.table.table[center_x + 1][center_y].wall_activation()
                self.table.print_table()
                self.turn ^= 1
                self.time += 1
                return "S"

        elif request == "Q":
            print("[bold red1]exiting the game ![/bold red1]")
            self.clear_terminal(1.5)
            return "Q"
        else:
            print(f"[bold red1]sorry {player.name} , your choice doesn't match any of the given options ![/bold red1]")
            return self.play()


game = Game(1, "player_1", "player_2")
exit_code = ""
while exit_code not in ["T", "Q"]:
    exit_code = game.play()


