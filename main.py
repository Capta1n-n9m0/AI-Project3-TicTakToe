import sys
import dotenv
import os
import argparse
from HttpGameClient import HttpGameClient, Session
from Board import CELLS_TO_TEXT
import time

"""
Communication with the API is done through HTTP REST requests.
API requires an API key and a user ID to authenticate the user.
They are set as environment variables AI_API_KEY and AI_USER_ID.
You can set them in the .env file in the root directory of the project or in the environment variables of your system.
"""

def getApiCredentials() -> tuple[str, str]:
  api_key = os.getenv("AI_API_KEY")
  if api_key is None:
    raise ValueError("API_KEY is not set")
  user_id = os.getenv("AI_USER_ID")
  if user_id is None:
    raise ValueError("USER_ID is not set")
  return api_key, user_id

def setupArgs() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description="Tic TaK Toe AI")
  parser.add_argument(
    "operation",
    choices=[
      "team",
      "game",
    ],
    help="Operation to perform"
  )
  parser.add_argument(
    "--create",
    action="store_true",
    help="Create a team or game"
  )
  parser.add_argument(
    "--add",
    action="store_true",
    help="Add team members"
  )
  parser.add_argument(
    "--remove",
    action="store_true",
    help="Remove team members"
  )
  parser.add_argument(
    "-l",
    "--list",
    action="store_true",
    help="List teams or games"
  )
  parser.add_argument(
    "--members",
    action="store_true",
    help="List team members"
  )
  parser.add_argument(
    "--name",
    type=str,
    help="Name of the team"
  )
  parser.add_argument(
    "--team",
    nargs="*",
    type=int,
    help="ID of the team"
  )
  parser.add_argument(
    "--user",
    type=int,
    nargs="*",
    help="ID of the user"
  )
  parser.add_argument(
    "--board",
    action="store_true",
    help="Board representation"
  )
  parser.add_argument(
    "--size",
    type=int,
    help="Size of the board",
    default=20
  )
  parser.add_argument(
    "--target",
    type=int,
    help="Target number of consecutive marks to win",
    default=10
  )
  parser.add_argument(
    "--game",
    type=int,
    help="ID of the game"
  )
  parser.add_argument(
    "--moves",
    type=int,
    help="List game moves"
  )
  parser.add_argument(
    "--details",
    action="store_true",
    help="Show game details"
  )
  parser.add_argument(
    "--make-move",
    nargs=2,
    type=int,
    help="Make a move"
  )
  parser.add_argument(
    "--play",
    action="store_true",
    help="Play a game"
  )
  
  return parser

def main(argv: list[str]) -> None:
  api_key, user_id = getApiCredentials()
  parser = setupArgs()
  
  args = parser.parse_args(argv[1:])
  
  with Session() as session:
    client = (HttpGameClient(session)
              .setApiKey(api_key)
              .setUserId(user_id)
              .build())
      
    if args.operation == "team":
      if args.create:
        if args.name is None:
          raise ValueError("Name is required")
        team = client.createTeam(args.name)
        print(f"Team created: {team}")
      elif args.remove:
        if args.team is None:
          raise ValueError("Team ID is required")
        if args.user is None:
          raise ValueError("You must specify at least one user ID")
        team_id = args.team[0]
        for user_id in args.user:
          client.removeTeamMember(team_id, user_id)
        print("Teams removed")
      elif args.list:
        teams = client.getMyTeams()
        print("Teams:")
        for index, name in teams.items():
          print(f"{index} : {name}")
      elif args.add:
        if args.team is None or args.user is None:
          raise ValueError("Team ID and user ID are required")
        team_id, user_id = args.team[0], args.user[0]
        for user_id in args.user:
          client.addTeamMember(team_id, user_id)
        print("Members added")
      elif args.members:
        if args.team is None:
          raise ValueError("Team ID is required")
        team_id = args.team[0]
        members = client.getTeamMembers(team_id)
        print("Members:")
        for member in members:
          print(member)
      else:
        raise ValueError("Invalid operation")
    elif args.operation == "game":
      if args.create:
        if args.size is None or args.target is None:
          raise ValueError("Board size, size and target are required")
        if args.team is None or len(args.team) != 2:
          raise ValueError("Two team IDs are required")
        team1, team2 = args.team
        game = client.createGame(team1, team2, args.size, args.target)
        print(f"Game created: {game}")
      elif args.list:
        games = client.getMyGames()
        print("Games:")
        for index, game in games.items():
          print(f"{index} : {game}")
      elif args.board:
        if args.game is None:
          raise ValueError("Game ID is required")
        board = client.getBoardObject(args.game)
        print(board)
      elif args.moves:
        if args.game is None:
          raise ValueError("Game ID is required")
        moves = client.getMoves(args.game, args.moves)
        print("Moves:")
        for move in reversed(moves):
          print(f"Team {move.teamId} placed {CELLS_TO_TEXT[move.symbol]} at {move.moveX}, {move.moveY}")
      elif args.details:
        if args.game is None:
          raise ValueError("Game ID is required")
        details = client.getGameDetails(args.game)
        print(f"Game ID: {details.gameId}")
        print(f"Team 1: {details.team1Id}")
        print(f"Team 2: {details.team2Id}")
        print(f"Board size: {details.boardSize}")
        print(f"Seconds per move: {details.secondsPerMove}")
        print(f"Target: {details.target}")
        print(f"Winner: {details.winnerTeamId}")
        print(f"Status: {details.status}")
        print(f"Turn of: {details.turnTeamId}")
      elif args.make_move:
        if args.game is None:
          raise ValueError("Game ID is required")
        if args.team is None:
          raise ValueError("Team ID is required")
        game_id = args.game
        team_id = args.team[0]
        x, y = args.make_move
        move = client.makeMove(game_id, team_id, (x, y))
        print(f"Move made: {move}")
      elif args.play:
        if args.game is None:
          raise ValueError("Game ID is required")
        game_id = args.game
        if args.team is None:
          raise ValueError("Team ID is required")
        team_id = args.team[0]
        print(f"Game ID: {game_id}. Playing as team {team_id}")
        if_changed = True
        old_details = None
        while True:
          time.sleep(1)
          details = None
          while not details:
            try:
              details = client.getGameDetails(game_id)
            except ConnectionError:
              print("Connection error, retrying...")
              time.sleep(1)
            except TimeoutError:
              print("Timeout error, retrying...")
              time.sleep(1)
          if details != old_details:
            if_changed = True
            old_details = details
          if if_changed:
            board = client.getBoardObject(game_id)
            print(board)
          if details.winnerTeamId is not None:
            print(f"Game has ended. Winner: {details.winnerTeamId}")
            return
          if details.turnTeamId != team_id and if_changed:
            print("It's not your turn, waiting for the other team to make a move")
            if_changed = False
          elif details.turnTeamId == team_id:
            x, y = map(int, input("Enter move coordinates: ").split())
            move = client.makeMove(game_id, team_id, (x, y))
            print(f"Move made: {move}")
      else:
        raise ValueError("Invalid operation")
    else:
      raise ValueError("Invalid operation")
  
    
  
if __name__ == "__main__":
  dotenv.load_dotenv()
  main(sys.argv)
