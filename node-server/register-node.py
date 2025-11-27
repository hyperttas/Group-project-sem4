import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("unique-token")
controller = os.getenv("controller")

s = requests.Session()
res = s.post(f"https://{controller}/register", json={"token": token})

