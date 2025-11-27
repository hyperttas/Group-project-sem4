from fastapi import FastAPI, HTTPException
from crypto_utils import generate_cert_and_key

app = FastAPI()

REGISTRATION_TOKEN = "ABCD1234"


@app.post("/register")
async def register(data: dict):
    if data.get("registration_token") != REGISTRATION_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    cert, key = generate_cert_and_key(common_name="node1")

    return {
        "certificate": cert,
        "private_key": key,
        "ca_cert": open("ca.crt").read()
    }
