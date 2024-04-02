import numpy as np

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

