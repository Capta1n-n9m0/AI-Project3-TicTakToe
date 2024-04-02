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

