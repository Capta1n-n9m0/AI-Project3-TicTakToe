import numpy as np
from dataclasses import dataclass

CELLS_TO_TEXT: dict[int, str] = {
  -1: "O",
  0: "-",
  1: "X"
}

TEXT_TO_CELLS: dict[str, int] = {
  "O": -1,
  "-": 0,
  "X": 1
}

@dataclass
class Move:
  symbol: int
  moveX: int
  moveY: int
  score: int

class Board:
  def __init__(self, size: int):
    self.size: int = size
    self.board = np.zeros((size, size), dtype=int)
    
  @classmethod
  def from_string(cls, string: str):
    rows = string.strip().split("\n")
    size = len(rows)
    board = cls(size)
    for i, line in enumerate(rows):
      for j, cell in enumerate(line):
        board.board[i][j] = TEXT_TO_CELLS[cell]
    return board
  
  def copy(self):
    new_board = Board(self.size)
    new_board.board = self.board.copy()
    return new_board
  
  def fill_from_moves_dict(self, moves: dict[tuple[int, int], int]):
    for (x, y), symbol in moves.items():
      self.board[x, y] = symbol

  def is_in_range(self, x: int, y: int) -> bool:
    return 0 <= x < self.size and 0 <= y < self.size

  def is_valid_move(self, x: int, y: int) -> bool:
    return self.is_in_range(x, y) and self.board[x, y] == 0
    
  def winner(self, target: int):
    size = self.size
    
    # Check rows
    for i in range(size):
      x_count = 0
      o_count = 0
      for j in range(size):
        if self.board[i, j] == 1:
          x_count += 1
          o_count = 0
        elif self.board[i, j] == -1:
          o_count += 1
          x_count = 0
        else:
          x_count = 0
          o_count = 0
        if x_count == target:
          return 1
        if o_count == target:
          return -1
    
    # Check columns
    for j in range(size):
      x_count = 0
      o_count = 0
      for i in range(size):
        if self.board[i, j] == 1:
          x_count += 1
          o_count = 0
        elif self.board[i, j] == -1:
          o_count += 1
          x_count = 0
        else:
          x_count = 0
          o_count = 0
        if x_count == target:
          return 1
        if o_count == target:
          return -1
    
    # Check diagonals
    for i in range(size):
      x_count = 0
      o_count = 0
      for j in range(size):
        if i + j < size:
          if self.board[i + j, j] == 1:
            x_count += 1
            o_count = 0
          elif self.board[i + j, j] == -1:
            o_count += 1
            x_count = 0
          else:
            x_count = 0
            o_count = 0
          if x_count == target:
            return 1
          if o_count == target:
            return -1
    for i in range(size):
      x_count = 0
      o_count = 0
      for j in range(size):
        if i + j < size:
          if self.board[j, i + j] == 1:
            x_count += 1
            o_count = 0
          elif self.board[j, i + j] == -1:
            o_count += 1
            x_count = 0
          else:
            x_count = 0
            o_count = 0
          if x_count == target:
            return 1
          if o_count == target:
            return -1
    for i in range(size):
      x_count = 0
      o_count = 0
      for j in range(size):
        if i + j < size:
          if self.board[i + j, size - j - 1] == 1:
            x_count += 1
            o_count = 0
          elif self.board[i + j, size - j - 1] == -1:
            o_count += 1
            x_count = 0
          else:
            x_count = 0
            o_count = 0
          if x_count == target:
            return 1
          if o_count == target:
            return -1
    for i in range(size):
      x_count = 0
      o_count = 0
      for j in range(size):
        if i + j < size:
          if self.board[j, size - i - j - 1] == 1:
            x_count += 1
            o_count = 0
          elif self.board[j, size - i - j - 1] == -1:
            o_count += 1
            x_count = 0
          else:
            x_count = 0
            o_count = 0
          if x_count == target:
            return 1
          if o_count == target:
            return -1
    return 0

  def generate_moves(self, symbol: int, target: int) -> list[Move]:
    n = self.size
    move_list: list[Move] = []
    current_move: Board

    if self.winner(target) != 0:
      return move_list
    
    a = b = n//2
    low_row = 0 if 0 > a else a
    low_column = 0 if 0 > b else b - 1
    high_row = n - 1 if (a + 1) >= n else a + 1
    high_column = n - 1 if (b + 1) >= n else b + 1
    
    while low_row > 0 - n and low_column > 0 - n:
      for i in range(low_column + 1, high_column + 1):
        if i < n and low_row >= 0:
          if self.board[low_row, i] == 0:
            current_move = self.copy()
            current_move.board[low_row, i] = symbol
            move_score = chain_evaluation(current_move)
            move_list.append(Move(symbol, low_row, i, move_score))
      low_row -= 1
      
      for i in range(low_row + 2, high_row + 1):
        if i < n and high_column < n:
          if self.board[i, high_column] == 0:
            current_move = self.copy()
            current_move.board[i, high_column] = symbol
            move_score = chain_evaluation(current_move)
            move_list.append(Move(symbol, i, high_column, move_score))
      high_column += 1
      
      for i in range(high_column - 2, low_column - 1, -1):
        if i >= 0 and high_row < n:
          if self.board[high_row, i] == 0:
            current_move = self.copy()
            current_move.board[high_row, i] = symbol
            move_score = chain_evaluation(current_move)
            move_list.append(Move(symbol, high_row, i, move_score))
      high_row += 1
      
      for i in range(high_row - 2, low_row, -1):
        if i >= 0 and low_column >= 0:
          if self.board[i, low_column] == 0:
            current_move = self.copy()
            current_move.board[i, low_column] = symbol
            move_score = chain_evaluation(current_move)
            move_list.append(Move(symbol, i, low_column, move_score))
      low_column -= 1
      
    return move_list
  
  def is_full(self) -> bool:
    return np.all(self.board != 0)
    
  def make_move(self, x: int, y: int, symbol: int):
    self.board[x, y] = symbol
  
  def __str__(self):
    result = ""
    tile_width = len(str(self.size - 1))
    result += " " * tile_width + " "
    for i in range(self.size):
      result += f"{i:>{tile_width}} "
    result += "\n"
    for i in range(self.size):
      result += f"{i:>{tile_width}} "
      for j in range(self.size):
        result += f"{CELLS_TO_TEXT[self.board[i, j]]:>{tile_width}} "
      result += "\n"
    return result

def chain_evaluation(board: Board) -> int:
  size = board.size
  
  def eval_line(x, y, dx, dy):
    score = 0
    x_count = -1
    o_count = -1
    while board.is_in_range(x, y):
      if board.board[x, y] == 1:
        x_count += 1
        score += 10 ** x_count
        if o_count >= 0:
          o_count = -1
      elif board.board[x, y] == -1:
        o_count += 1
        score -= 10 ** o_count
        if x_count >= 0:
          x_count = -1
      else:
        o_count = -1
        x_count = -1
      x += dx
      y += dy
    return score
  
  total_score = 0
  for i in range(size):
    total_score += eval_line(i, 0, 0, 1)
    total_score += eval_line(0, i, 1, 0)
    
    total_score += eval_line(0, i, 1, 1)
    total_score += eval_line(i, 0, 1, 1)
    
    total_score += eval_line(0, i, 1, -1)
    total_score += eval_line(i, size - 1, 1, -1)
  
  return total_score


def minmax(board: Board, depth: int, symbol: int, target: int, alpha: int = -10_000_000, beta: int = 10_000_000) -> Move:
  if depth == 0:
    score = chain_evaluation(board)
    return Move(symbol, -1, -1, score)
  
  next_moves = board.generate_moves(symbol, target)
  
  if not next_moves:
    score = chain_evaluation(board)
    return Move(symbol, -1, -1, score)
  
  best_move = Move(symbol, -1, -1, -1000000)
  
  for move in next_moves:
    board.make_move(move.moveX, move.moveY, symbol)
    
    if symbol == 1:
      score = minmax(board, depth - 1, -1, alpha, beta).score
      if score > alpha:
        alpha = score
        best_move = move
    else:
      score = minmax(board, depth - 1, 1, alpha, beta).score
      if score < beta:
        beta = score
        best_move = move
    
    board.make_move(move.moveX, move.moveY, 0)
    
    if alpha >= beta:
      break
  
  return best_move


