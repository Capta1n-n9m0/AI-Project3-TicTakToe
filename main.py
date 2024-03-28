import sys
import dotenv
import os
import argparse

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
  parser = argparse.ArgumentParser(description="Tic Tac Toe AI")
  parser.add_argument(
    "operation",
    choices=[
      "team",
      "game",
    ],
    help="Operation to perform"
  )
  parser.add_argument(
    "-c",
    "--create",
    action="store_true",
    help="Create a team or game"
  )
  parser.add_argument(
    "-r",
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
    "-n",
    "--name",
    help="Name of the team"
  )
  parser.add_argument(
    "-t",
    "--team",
    nargs="*",
    type=int,
    help="ID of the team"
  )
  parser.add_argument(
    "-u",
    "--user",
    type=int,
    nargs="*",
    help="ID of the user"
  )
  parser.add_argument(
    "-b",
    "--board",
    type=int,
    help="Size of the board"
  )
  parser.add_argument(
    "-s",
    "--size",
    type=int,
    help="Size of the board"
  )
  parser.add_argument(
    "-g",
    "--target",
    type=int,
    help="Target number of consecutive marks to win"
  )
  return parser



def main(argv: list[str]) -> None:
  api_key, user_id = getApiCredentials()
  parser = setupArgs()
  
  args = parser.parse_args(argv[1:])
  if args.operation == "team":
    ...
  elif args.operation == "game":
    ...
  else:
    raise ValueError("Invalid operation")
  
  
  


if __name__ == "__main__":
  dotenv.load_dotenv()
  main(sys.argv)
