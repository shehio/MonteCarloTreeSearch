from __future__ import annotations
import numpy as np

from twoplayergame import GameState


class MonteCarloTreeSearchNode:
    def __init__(self, game_state: GameState, parent: MonteCarloTreeSearchNode, player, opponent):
        self.game_state = game_state
        self.parent = parent
        self.player = player
        self.opponent = opponent
        self.children = np.array([], dtype=MonteCarloTreeSearchNode)
        self.untried_actions = game_state.get_legal_actions(player)
        self.wins = {self.player: 0, self.opponent: 0}
        self.visits = 0

    def select(self, c) -> MonteCarloTreeSearchNode:
        leaf_node = self

        while not leaf_node.terminal:
            if not self.is_fully_expanded:
                return self.expand()
            else:
                leaf_node = self.select_child_with_max_ucb(c)

        return leaf_node

    def expand(self) -> MonteCarloTreeSearchNode:
        print(f'Expanding for {self.__repr__()}')
        action = self.untried_actions.pop()
        new_game_state = self.game_state.make_move(self.player, action)
        child_node = MonteCarloTreeSearchNode(new_game_state, self, self.opponent, self.player)
        self.children = np.append(self.children, child_node)
        print(f'Created {child_node.__repr__()}')
        return child_node

    def rollout(self) -> float:
        print(f'Rollout now for {self.__repr__()}')
        rollout_state = self.game_state
        current_player = self.player
        while not rollout_state.is_game_over:
            possible_moves = rollout_state.get_legal_actions(current_player)
            current_player = self.opponent if current_player == self.player else self.player
            move = possible_moves(np.random.randint(len(possible_moves)))
            rollout_state.make_move(current_player, move)
        print(f'The rollout result: {rollout_state.game_result}')
        return rollout_state.game_result

    def backpropagate(self, who_won):
        self.visits += 1
        self.wins[who_won] += 1
        if self.parent is not None:
            self.parent.backpropagate(who_won)

    def select_child_with_max_ucb(self, c):
        ucb_values = list(map(lambda child: MonteCarloTreeSearchNode.get_ucb(child, c), self.children))
        return self.children(np.argmax(ucb_values))

    @staticmethod
    def get_ucb(child: MonteCarloTreeSearchNode, c):
        child.win_ratio + c * np.sqrt(np.log(child.parent.visits) / child.visits)

    @property
    def win_ratio(self):
        # If the node hasn't been visited, then the win_ratio (part of ucb) is inf. This means it will be selected.
        if self.visits == 0:
            return np.inf
        return self.wins / self.visits

    @property
    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.get_legal_actions(self.player))

    @property
    def is_terminal(self):
        return self.game_state.is_game_over() is not None

    def __repr__(self):
        return f'TreeNode: {id(self)}'

    def __str__(self):
        return f'TreeNode: {id(self)}, number of visits: {self.visits}, win ratio: {self.win_ratio},' \
               f' fully expanded: {self.is_fully_expanded}, children: {self.children}'
