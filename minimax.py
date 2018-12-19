import random
import sys

player_x = 1
player_o = 0


def win_o(game_state):
    return ((game_state & 0o007) == 0o007 or
            (game_state & 0o070) == 0o070 or
            (game_state & 0o700) == 0o700 or
            (game_state & 0o111) == 0o111 or
            (game_state & 0o222) == 0o222 or
            (game_state & 0o444) == 0o444 or
            (game_state & 0o421) == 0o421 or
            (game_state & 0o124) == 0o124)


def win_x(game_state):
    return ((game_state & 0o007000) == 0o007000 or
            (game_state & 0o070000) == 0o070000 or
            (game_state & 0o700000) == 0o700000 or
            (game_state & 0o111000) == 0o111000 or
            (game_state & 0o222000) == 0o222000 or
            (game_state & 0o444000) == 0o444000 or
            (game_state & 0o421000) == 0o421000 or
            (game_state & 0o124000) == 0o124000)


def filled(game_state):
    return (((game_state >> 9) | game_state) & 0o777) == 0o777


def end_state(game_state):
    return win_o(game_state) or win_x(game_state) or filled(game_state)


def evaluation(game_state, depth):
    if win_o(game_state):
        return depth - 10
    elif win_x(game_state):
        return 10 - depth
    else:
        return 0


def do_ply(game_state, ply):
    return game_state | ply


def generate_plies(game_state, plies, player):
    for i in range(9):
        if not (((game_state >> 9) | game_state) & (1 << i)):
            plies.append(1 << (i + player * 9))


transposition_table = {}


def mini_max(game_state, depth, maximising_player):
    possible_plies = []

    best_ply = None

    if end_state(game_state):
        return None, evaluation(game_state, depth)

    if maximising_player:  # X is maximising player
        best_value = -sys.maxsize - 1
        generate_plies(game_state, possible_plies, player_x)

        random.shuffle(possible_plies)

        for i in possible_plies:
            next_game_state = do_ply(game_state, i)
            if next_game_state not in transposition_table:
                next_ply, next_value = mini_max(next_game_state, depth + 1, not maximising_player)
                transposition_table[next_game_state] = next_value

            else:
                next_value = transposition_table[next_game_state]

            if next_value > best_value:
                best_value = next_value
                best_ply = i
    else:
        best_value = sys.maxsize
        generate_plies(game_state, possible_plies, player_o)

        random.shuffle(possible_plies)

        for i in possible_plies:
            next_game_state = do_ply(game_state, i)
            if next_game_state not in transposition_table:
                next_ply, next_value = mini_max(next_game_state, depth + 1, not maximising_player)
                transposition_table[next_game_state] = next_value

            else:
                next_value = transposition_table[next_game_state]

            if next_value < best_value:
                best_value = next_value
                best_ply = i

    return best_ply, best_value


def refresh_board(game_state):
    for i in range(9):
        if (game_state & (1 << i)) != 0:
            print('o', end='')
        elif (game_state & (1 << (i + 9))) != 0:
            print('x', end='')
        else:
            print('-', end='')
        if i % 3 == 2:
            print()
    print()


if __name__ == '__main__':
    playerSide = 0
    game_state = 0
    depth = 0
    i = 0
    while not end_state(game_state):
        i += 1
        print('Turn %d' % i)
        ply, value = mini_max(game_state, depth, playerSide ^ 1)
        playerSide = playerSide ^ 1
        game_state = do_ply(game_state, ply)
        refresh_board(game_state)
