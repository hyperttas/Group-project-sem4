import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("unique-token")

s = requests.Session()
res = s.post("https://controller/enroll", json={"token": token})

