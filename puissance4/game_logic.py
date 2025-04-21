import tkinter as tk
from env import Puissance4Env
from stable_baselines3 import PPO

class Connect4:
    def __init__(self, root):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.winner = None
        self.env = Puissance4Env()
        self.model = PPO.load("puissance4_ppo")
        self.obs = self.env.reset()
        self.done = False



    def reset(self):
        self.__init__()

    def make_move(self, col):
        if self.winner or col < 0 or col >= 7 or self.board[0][col] != 0:
            return False
        for row in reversed(range(6)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                if self.check_win(row, col):
                    self.winner = self.current_player
                else:
                    self.current_player = 2 if self.current_player == 1 else 1
                return True
        return False

    def is_draw(self):
        return all(self.board[0][col] != 0 for col in range(7)) and self.winner is None

    def check_win(self, row, col):
        return any(
            self.count_tokens(row, col, dr, dc) >= 4
            for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]
        )

    def count_tokens(self, row, col, dr, dc):
        total = 1
        for dir in [1, -1]:
            r, c = row + dir*dr, col + dir*dc
            while 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                total += 1
                r += dir * dr
                c += dir * dc
        return total

    def handle_click(self, col):
        print(f"Clic sur colonne {col}")

