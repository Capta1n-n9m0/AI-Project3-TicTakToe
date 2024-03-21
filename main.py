import sys
import dotenv
import os

"""
Communication with the API is done through HTTP REST requests.
API requires an API key and a user ID to authenticate the user.
They are set as environment variables AI_API_KEY and AI_USER_ID.
You can set them in the .env file in the root directory of the project or in the environment variables of your system.
"""

def main(argv: list[str]) -> None:
    API_KEY = os.getenv("AI_API_KEY")
    if API_KEY is None:
        print("API_KEY is not set")
        sys.exit(1)
    USER_ID = os.getenv("AI_USER_ID")
    if USER_ID is None:
        print("USER_ID is not set")
        sys.exit(1)
    print(f"API_KEY: {API_KEY}")
    print(f"USER_ID: {USER_ID}")
    print(argv)
    

if __name__ == "__main__":
    dotenv.load_dotenv()
    main(sys.argv)
    