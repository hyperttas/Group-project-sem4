import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("unique-token")
controller = "172.18.0.1"

s = requests.Session()
res = s.post(f"https://{controller}/register", json={"token": token})

