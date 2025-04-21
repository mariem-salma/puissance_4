import random

def random_ai_move(game):
    valid_moves = [col for col in range(7) if game.board[0][col] == 0]
    return random.choice(valid_moves) if valid_moves else 0

