import random
import sys


class TicTacToe:
    player_x = 1
    player_o = 0

    def __init__(self):
        self.current_game_state = 0
        self.transposition_table = {}
        self.current_player_move = self.player_x
        self.mini_max(self.current_game_state, 0, self.current_player_move)

    @staticmethod
    def win(game_state):
        return any((game_state & mask) == mask for mask in [0o007, 0o070, 0o700, 0o111, 0o222, 0o444, 0o421, 0o124])

    def win_o(self, game_state):
        return self.win(game_state)

    def win_x(self, game_state):
        return self.win(game_state >> 9)

    @staticmethod
    def filled(game_state):
        return (((game_state >> 9) | game_state) & 0o777) == 0o777

    def end_state(self, game_state):
        return self.win_o(game_state) or self.win_x(game_state) or self.filled(game_state)

    def evaluation(self, game_state, depth):
        if self.win_o(game_state):
            return depth - 10
        elif self.win_x(game_state):
            return 10 - depth
        return 0

    @staticmethod
    def do_ply(game_state, ply):
        return game_state | ply

    @staticmethod
    def generate_plies(game_state, player):
        plies = [1 << (i + player * 9) for i in range(9) if not (((game_state >> 9) | game_state) & (1 << i))]
        random.shuffle(plies)
        return plies

    def mini_max(self, game_state, depth, player):

        best_ply = None

        if self.end_state(game_state):
            return None, self.evaluation(game_state, depth)

        if player == self.player_x:  # X is maximising player
            best_value = -sys.maxsize - 1

            for ply in self.generate_plies(game_state, self.player_x):
                next_game_state = self.do_ply(game_state, ply)
                if next_game_state not in self.transposition_table:
                    next_ply, next_value = self.mini_max(next_game_state, depth + 1, self.player_o)
                    self.transposition_table[next_game_state] = next_value
                else:
                    next_value = self.transposition_table[next_game_state]

                if next_value > best_value:
                    best_value = next_value
                    best_ply = ply
        else:
            best_value = sys.maxsize

            for ply in self.generate_plies(game_state, self.player_o):
                next_game_state = self.do_ply(game_state, ply)
                if next_game_state not in self.transposition_table:
                    next_ply, next_value = self.mini_max(next_game_state, depth + 1, self.player_x)
                    self.transposition_table[next_game_state] = next_value
                else:
                    next_value = self.transposition_table[next_game_state]

                if next_value < best_value:
                    best_value = next_value
                    best_ply = ply

        return best_ply, best_value

    def refresh_board(self):
        for i in range(9):
            if (self.current_game_state & (1 << i)) != 0:
                print('o', end='')
            elif (self.current_game_state & (1 << (i + 9))) != 0:
                print('x', end='')
            else:
                print('-', end='')
            if i % 3 == 2:
                print()
        print()

    def next_move(self):
        if self.current_player_move == self.player_x:
            ply = self.mini_max(self.current_game_state, 0, self.current_player_move)[0]
        else:
            ply = 1 << (int(input('enter move 0-8: ')) + self.current_player_move * 9)
        self.current_game_state = self.do_ply(self.current_game_state, ply)
        self.current_player_move ^= 1
        self.refresh_board()

    def reset(self):
        self.current_game_state = 0
        self.current_player_move = self.player_x


if __name__ == '__main__':
    playerSide = 0

    game = TicTacToe()
    while True:
        while not game.end_state(game.current_game_state):
            game.next_move()
        game.reset()
