import os
from pathlib import Path

from dotenv import load_dotenv


_BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(_BASE_DIR / '.env')

class Config:
    """
    Basic config
    """
    # Application config
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = _BASE_DIR
    STATIC_DIR = BASE_DIR / 'statics'

    DEBUG = os.getenv("DEBUG", "False").upper() == "TRUE"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if not DEBUG else "DEBUG")

    API_AUTH_KEY = os.getenv("API_AUTH_KEY", None)

    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    STATIC_URL = f"{BASE_URL}/statics"

    BARK_ENDPOINT = os.getenv("BARK_ENDPOINT", "https://api.day.app")
    BARK_APIKEY = os.getenv("BARK_APIKEY", None)
    BARK_ENCRYPT_KEY = os.getenv("BARK_ENCRYPT_KEY", None)

    SIGN_SECRET = os.getenv("SIGN_SECRET", None)
    SIGN_EXPIRE = int(os.getenv("SIGN_EXPIRE", 1000))

