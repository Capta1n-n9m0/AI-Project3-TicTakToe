import sys
import dotenv
import os
from HttpGameClient import HttpGameClient

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


def main(argv: list[str]) -> None:
  api_key, user_id = getApiCredentials()
  
  with HttpGameClient(api_key, user_id) as client:
    try:
      print(client.exampleGet(params={"type": "help"}))
    except ValueError as e:
      print(e, file=sys.stderr)
    try:
      print(client.examplePost())
    except ValueError as e:
      print(e, file=sys.stderr)
    # print(client.createTeam("Test Team"))
    # print(client.addTeamMember(1, 1))
    # print(client.removeTeamMember(1, 1))
    # print(client.getTeamMembers(1))
    # print(client.getMyTeams())


if __name__ == "__main__":
  dotenv.load_dotenv()
  main(sys.argv)
