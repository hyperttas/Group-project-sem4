from minio import Minio
import os
from dotenv import load_dotenv
import urllib3

load_dotenv()

MINIO_URL = os.environ.get("MINIO_URL")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

httpClient = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs='./certs/minio/minio.crt')

client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=True,
    http_client=httpClient
)

pool = None
