import sys
import site
import logging
from dotenv import load_dotenv
logging.basicConfig(stream=sys.stderr)
site.addsitedir("/var/www/FlaskApp/venv/lib/python3.13/site-packages")
sys.path.append("/var/www/FlaskApp/FlaskApp")
load_dotenv("/var/www/FlaskApp/FlaskApp/.env")

from app import app as application
