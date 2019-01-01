import random
import sys


class TicTacToe:
    player_x = 1
    player_o = 0

    def __init__(self, ai_only=False):
        self.current_game_state = 0
        self.transposition_table = {}
        self.current_player_move = self.player_x
        self.ai_only = ai_only
        self.mini_max(self.current_game_state, 0, self.current_player_move)

    @property
    def game_state(self):
        return (lambda a: [a[i:i + 3] for i in range(0, len(a), 3)])(
                [('o' * ((self.current_game_state >> i) & 1) +
                  'x' * ((self.current_game_state >> i >> 9) & 1)).rjust(1, '-')
                 for i in range(9)])

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
    def apply_ply(game_state, ply):
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
            best_value, compare = -sys.maxsize - 1, max
        else:
            best_value, compare = sys.maxsize, min

        for ply in self.generate_plies(game_state, player):
            next_game_state = self.apply_ply(game_state, ply)
            try:
                next_value = self.transposition_table[next_game_state]
            except KeyError:
                _, next_value = self.mini_max(next_game_state, depth + 1, not player)
                self.transposition_table[next_game_state] = next_value

            if compare(next_value, best_value) == next_value:
                best_value, best_ply = next_value, ply

        return best_ply, best_value

    def display_game_state(self):
        for row in self.game_state:
            for tile in row:
                print(tile, end='')
            print()
        print()

    @staticmethod
    def make_move(space, player):
        return 1 << (space + player * 9)

    def next_move(self):
        if self.ai_only:
            ply = self.mini_max(self.current_game_state, 0, self.current_player_move)[0]
        else:
            if self.current_player_move == self.player_x:
                ply = self.mini_max(self.current_game_state, 0, self.current_player_move)[0]
            else:
                ply = self.make_move(int(input('enter move 1-9: ')) - 1, self.current_player_move)
        self.current_game_state = self.apply_ply(self.current_game_state, ply)
        self.current_player_move ^= 1

        if not self.ai_only:
            self.display_game_state()

    def get_winner(self):
        if self.win_x(self.current_game_state):
            return 'X wins'
        elif self.win_o(self.current_game_state):
            return 'O wins'
        return 'Draw'

    def reset_game(self):
        self.current_game_state = 0
        self.current_player_move = self.player_x

    def __repr__(self):
        return '{} ; current move: {}'.format(self.game_state, ('x' if self.current_player_move else 'o'))


if __name__ == '__main__':

    game = TicTacToe(ai_only=True)
    winners = {}
    while True:
        while not game.end_state(game.current_game_state):
            game.next_move()

        winner = game.get_winner()
        try:
            winners[winner] = winners[winner] + 1
        except KeyError:
            winners[winner] = 1

        print(f'\r{winners}', end=('' if game.ai_only else '\n'))

        game.reset_game()
