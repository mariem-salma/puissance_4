import gym
from gym import spaces
import numpy as np

ROWS = 6
COLS = 7

class Puissance4Env(gym.Env):
    def __init__(self):
        super(Puissance4Env, self).__init__()
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.action_space = spaces.Discrete(COLS)  # 7 colonnes
        self.observation_space = spaces.Box(low=0, high=2, shape=(ROWS, COLS), dtype=int)
        self.current_player = 1  # 1 = IA, 2 = adversaire fictif
        self.done = False

    def reset(self, *, seed=None, options=None):
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.current_player = 1
        self.done = False
        return np.copy(self.board), {}

    def step(self, action):
        if self.done:
            return np.copy(self.board), 0, True, False, {}

        row = self.get_next_open_row(action)
        if row is None:
            # Coup invalide = grosse pénalité
            return np.copy(self.board), -10, True, False, {}

        self.board[row][action] = self.current_player
        win = self.check_winner(self.current_player)
        draw = np.all(self.board != 0)

        reward = 1 if win else 0
        self.done = win or draw

        return np.copy(self.board), reward, self.done, False, {}

    def get_next_open_row(self, col):
        for r in reversed(range(ROWS)):
            if self.board[r][col] == 0:
                return r
        return None

    def check_winner(self, player):
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c+i] == player for i in range(4)):
                    return True

        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.board[r+i][c] == player for i in range(4)):
                    return True

        # Diagonale bas-droite
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r+i][c+i] == player for i in range(4)):
                    return True

        # Diagonale haut-droite
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r-i][c+i] == player for i in range(4)):
                    return True

        return False

