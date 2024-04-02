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
  
  def is_valid(x, y):
    return 0 <= x < size and 0 <= y < size
  
  def eval_line(x, y, dx, dy):
    score = 0
    x_count = -1
    o_count = -1
    while is_valid(x, y):
      if board.board[x, y] == 1:
        x_count += 1
        score += 10 ** x_count
        if o_count >= 0:
          o_count = -1
      elif board.board[x, y] == -1:
        o_count += 1
        score += 10 ** o_count
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

