from functools import partial
import logging
import numpy as np
import random
import sys

from gamestate import GameState
from montecarlotreesearch import MonteCarloTreeSearch
from player import Player


def partial_mcts(number_of_simulation, game_state):
    return MonteCarloTreeSearch.get_best_move(game_state, number_of_simulation)


if __name__ == '__main__':
    # https://docs.python.org/3/library/logging.html#levels
    logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)

    simulation_count = 100
    p1 = Player('P1', partial(partial_mcts, simulation_count))
    p2 = Player('P2', lambda game_state: random.choice(game_state.get_valid_moves()))
    players = [p1, p2]

    board_size = 3
    game = GameState(np.array([p1, p2]), turn=1, game_board=np.zeros((board_size, board_size)))
    logging.debug(game)

    i = 0
    while not game.is_game_over:
        player = players[i % 2]
        logging.info(f'\n{player}\'s turn')
        game = game.make_move(player.get_move(game))
        print(game)
        i = i + 1

    print(f'\n{game.winner} won in {i} turns.')
