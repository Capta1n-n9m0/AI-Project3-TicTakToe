import sys
import dotenv
import os
import requests

"""
Communication with the API is done through HTTP REST requests.
API requires an API key and a user ID to authenticate the user.
They are set as environment variables AI_API_KEY and AI_USER_ID.
You can set them in the .env file in the root directory of the project or in the environment variables of your system.
"""


def main(argv: list[str]) -> None:
  API_KEY = os.getenv("AI_API_KEY")
  if API_KEY is None:
    raise ValueError("API_KEY is not set")
  USER_ID = os.getenv("AI_USER_ID")
  if USER_ID is None:
    raise ValueError("USER_ID is not set")
  with requests.Session() as session:
    
    """
    Mod Security filters User Agent of the requests package, so we need to change it to a browser's user agent
    """
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    })
    session.headers.update({
        "x-api-key": API_KEY,
        "userId": USER_ID
      })
    response = session.get("https://www.notexponential.com/aip2pgaming/api/index.php")
    print(response.request.headers)
    print(response.request.url)
    print(response.reason)
    print(response.text)
    print(response.status_code)
    print(response.headers)


if __name__ == "__main__":
  dotenv.load_dotenv()
  main(sys.argv)
