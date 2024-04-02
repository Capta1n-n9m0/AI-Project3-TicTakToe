from requests import Session as RSession, Response
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
from Board import TEXT_TO_CELLS, Board



def str_to_tuple(key: str):
  x, y = key.strip().split(',')
  return int(x), int(y)

@dataclass
class MoveData:
  modeId: int
  gameId: int
  teamId: int
  move: tuple[int, int]
  symbol: int
  moveX: int
  moveY: int
  
  @classmethod
  def from_dict(cls, data: dict):
    return cls(
      modeId=int(data.get("moveId")),
      gameId=int(data.get("gameId")),
      teamId=int(data.get("teamId")),
      move=str_to_tuple(data.get("move")),
      symbol=TEXT_TO_CELLS[data.get("symbol")],
      moveX=int(data.get("moveX")),
      moveY=int(data.get("moveY"))
    )

@dataclass
class GameData:
  gameId: int
  gameType: str
  moves: int
  boardSize: int
  target: int
  team1Id: int
  team1Name: str
  team2Id: int
  team2Name: str
  secondsPerMove: int
  status: int
  winnerTeamId: int | None
  turnTeamId: int | None
  
  @classmethod
  def from_dict(cls, data: dict):
    return cls(
      gameId=int(data.get("gameid")),
      gameType=data.get("gametype"),
      moves=int(data.get("moves")),
      boardSize=int(data.get("boardsize")),
      target=int(data.get("target")),
      team1Id=int(data.get("team1id")),
      team1Name=data.get("team1name"),
      team2Id=int(data.get("team2id")),
      team2Name=data.get("team2name"),
      secondsPerMove=int(data.get("secondspermove")),
      status=data.get("status"),
      winnerTeamId=int(data.get("winnerteamid")) if data.get("winnerteamid") is not None else None,
      turnTeamId=int(data.get("turnteamid")) if data.get("turnteamid") is not None else None
    )
  

class IHttpClient(ABC):
  r"""
  Interface for an HTTP client.
  It provides methods to make GET and POST requests.
  """
  @abstractmethod
  def get(self, url: str, **kwargs) -> Response:
    pass
  
  @abstractmethod
  def post(self, url: str, **kwargs) -> Response:
    pass
  
  @abstractmethod
  def request(self, method: str, url: str, **kwargs) -> Response:
    pass

class Session(RSession, IHttpClient):
  r"""
  Implementation of the IHttpClient interface using the requests.Session class.
  Works as a wrapper around the requests.Session class.
  """
  def request(self, method: str, url: str, **kwargs) -> Response:
    return super().request(method, url, **kwargs)
  
  def get(self, url: str, **kwargs) -> Response:
    return super().get(url, **kwargs)
  
  def post(self, url: str, **kwargs) -> Response:
    return super().post(url, **kwargs)

class HttpGameClient:
  r"""
  An abstraction of the API for the game.
  It provides methods to interact with the API.
  It requires an API key and a user ID to make requests.
  It also requires an instance of a class that implements the IHttpClient interface to make requests.
  It uses dependency injection to allow for easy testing.
  It uses the builder pattern to create the client.
  Building the client sets the headers and the endpoint.
  """
  api_key: str
  user_id: str
  sender: IHttpClient
  headers: dict[str, str]
  endpoint: str
  
  def __init__(self, sender: IHttpClient):
    r"""
    Initializes the client with the given sender.
    """
    self.sender = sender
    
  def setApiKey(self, api_key: str):
    r"""
    Sets the API key for the client.
    :param api_key:
    :return: Instance of the client
    """
    self.api_key = api_key
    return self
  
  def setUserId(self, user_id: str):
    r"""
    Sets the user ID for the client.
    :param user_id:
    :return: Instance of the client
    """
    self.user_id = user_id
    return self
  
  def build(self):
    r"""
    Builds the client by setting the headers and the endpoint.
    :raises ValueError: If the API key or the user ID is not set
    :return: Instance of the client
    """
    if self.api_key is None:
      raise ValueError("API key is not set")
    if self.user_id is None:
      raise ValueError("User ID is not set")
    
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "x-api-key": self.api_key,
      "userId": self.user_id
    }
    self.endpoint = "https://www.notexponential.com/aip2pgaming/api/index.php"
    return self
  
  def request(self, method: str, url: str, **kwargs):
    r"""
    This method is used to make requests to the API.
    It checks if the response status code is 200 and if the response contains a code.
    If the code is "FAIL", it raises an exception with the message from the response.
    
    :raises ValueError: If the response status code is not 200 or if the response contains a code with the value "FAIL"
    :return: Response object
    """
    if self.headers is None:
      raise ValueError("Headers are not set")
    
    response = self.sender.request(method, url, headers=self.headers, timeout=(7, 19), **kwargs)
    if response.status_code != 200:
      raise ValueError(f"Request failed with status code {response.status_code}")
    
    code = response.json().get("code")
    if code is None:
      raise ValueError("Response does not contain a code")
    if code == "FAIL":
      message = response.json().get("message")
      if message is None:
        raise ValueError("Failed response does not contain a message")
      raise ValueError(f"API request failed with message: {message}")
    
    return response
  
  def get(self, url: str, **kwargs) -> Response:
    return self.request("GET", url, **kwargs)
  
  def post(self, url: str, **kwargs) -> Response:
    return self.request("POST", url, **kwargs)
  
  def exampleGet(self, params: dict = None):
    r"""
    This is an example of a GET request to the API. It does not require any parameters.
    It is used to test the connection to the API. It will always raise an exception.
    :return: None
    :raises ValueError:
    """
    self.get(self.endpoint, params=params)
    
  def examplePost(self, params: dict = None, data: dict = None):
    r"""
    This is an example of a POST request to the API. It does not require any parameters.
    It is used to test the connection to the API. It will always raise an exception.
    :return: None
    :raises ValueError:
    """
    self.post(self.endpoint, params=params, data=data)
    
  def createTeam(self, team_name: str) -> int:
    r"""
    Creates a team with the given name and returns the team ID.
    :param team_name: Name of the team
    :return: ID of the created team
    """
    response = self.post(self.endpoint, data={"type": "team", "name": team_name})
    return int(response.json().get("teamId"))
  
  def addTeamMember(self, team_id: int, user_id: int):
    r"""
    Adds a user to a team.
    :param team_id:
    :param user_id:
    :return: None
    """
    self.post(self.endpoint, data={"type": "member", "teamId": team_id, "userId": user_id})
  
  def removeTeamMember(self, team_id: int, user_id: int):
    r"""
    Removes a user from a team.
    
    :param team_id: ID of the team
    :param user_id: ID of the user
    :return: None
    """
    self.post(self.endpoint, data={"type": "removeMember", "teamId": team_id, "userId": user_id})
    
  def getTeamMembers(self, team_id: int) -> list[int]:
    r"""
    Gets a list of members of a team.
    :param team_id: ID of the team
    :return: List of members
    """
    response = self.get(self.endpoint, params={"type": "team", "teamId": team_id})
    return [int(member) for member in response.json().get("userIds")]
  
  def getMyTeams(self) -> dict[int, str]:
    r"""
    Gets a list of teams the user is a member of. Should contain only one team.
    :return: List of teams
    """
    response = self.get(self.endpoint, params={"type": "myTeams"})
    result = {}
    for team in response.json().get("myTeams"):
      result.update({int(key): value for key, value in team.items()})
    return result
  
  def createGame(self, team_id_1: int, team_id_2: int, board_size: int = 20, target: int = 10) -> int:
    r"""
    Creates a game between two teams.
    The game is Tic Tac Toe with the given board size and target.
    Returns the game ID.
    :param team_id_1: ID of the first team
    :param team_id_2: ID of the second team
    :param board_size: Size of the board
    :param target: Target number of consecutive marks to win
    :return: ID of the created game
    """
    response = self.post(self.endpoint, data={
      "type": "game",
      "teamId1": team_id_1,
      "teamId2": team_id_2,
      "gameType": "TTT",  # "TTT" stands for "Tic Tac Toe
      "boardSize": board_size,
      "target": target
    })
    return int(response.json().get("gameId"))
  
  def getMyGames(self) -> dict[int, str]:
    r"""
    Gets a list of games the user is participating in.
    :return: List of games
    """
    response = self.get(self.endpoint, params={"type": "myGames"})
    result = {}
    for game in response.json().get("myGames"):
      result.update({int(key): value for key, value in game.items()})
    return result
  
  def makeMove(self, game_id: int, team_id: int, move: tuple[int, int]) -> int:
    r"""
    Makes a move in a game.
    :param game_id: ID of the game
    :param team_id: ID of the team
    :param move: Tuple of row and column
    :return: ID of the move
    :raises ValueError: If the move is invalid
    :raises ValueError: If game is not found
    :raises ValueError: If team is not in the game
    """
    response = self.post(self.endpoint, data={
      "type": "move",
      "gameId": game_id,
      "teamId": team_id,
      "move": f"{move[0]},{move[1]}"
    })
    return int(response.json().get("moveId"))
  
  def getMoves(self, game_id: int, count: int = 20) -> list[MoveData]:
    r"""
    Gets a list of moves in a game.
    :param count: Number of moves to get
    :param game_id: ID of the game
    :return: List of moves
    """
    response = self.get(self.endpoint, params={"type": "moves", "gameId": game_id, "count": count})
    result = [MoveData.from_dict(move) for move in response.json().get("moves")]
    return result
  
  def getGameDetails(self, game_id: int) -> GameData:
    r"""
    Gets the details of a game.
    :param game_id: ID of the game
    :return: Dictionary of game details
    """
    response = self.get(self.endpoint, params={"type": "gameDetails", "gameId": game_id})
    return GameData.from_dict(json.loads(response.json().get("game")))
  
  def getBoardMoves(self, game_id: int) -> dict[tuple[int, int], int]:
    r"""
    Gets the board of a game.
    :param game_id: ID of the game
    :return: Dictionary of filled cells
    """
    response = self.get(self.endpoint, params={"type": "boardMap", "gameId": game_id})
    board = response.json().get("output")
    
    return {str_to_tuple(key): TEXT_TO_CELLS[value] for key, value in board.items()}
  
  def getBoardString(self, game_id: int) -> str:
    r"""
    Gets the board of a game as a string.
    :param game_id: ID of the game
    :return: String representation of the board
    """
    response = self.get(self.endpoint, params={"type": "boardString", "gameId": game_id})
    
    return response.json().get("output")
  
  def getBoardObject(self, game_id: int) -> Board:
    r"""
    Gets the board of a game as a Board object.
    :param game_id: ID of the game
    :return: Board object
    """
    board_string = self.getBoardString(game_id)
    return Board.from_string(board_string)
  