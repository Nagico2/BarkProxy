import time
import hmac
import base64
import hashlib
import secrets
import urllib.parse

from sanic import Unauthorized

from loguru import logger


from config import CONFIG

def get_sign(timestamp: int, secret: str) -> str:
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return sign


def check_sign(timestamp: int, sign: str | None):
    if sign is None:
        raise Unauthorized("Invalid sign, sign is none")
    cur = round(time.time() * 1000)
    if abs(cur - timestamp) > CONFIG.SIGN_EXPIRE:
        raise Unauthorized("Invalid sign, timestamp expired")

    correct_sign = get_sign(timestamp, CONFIG.SIGN_SECRET)

    logger.trace(f"Check sign: {timestamp}, {sign}, {correct_sign}")
    if sign != correct_sign:
        raise Unauthorized("Invalid sign, sign not match")


def generate_hex_string(length: int) -> str:
    return secrets.token_hex(length // 2)
