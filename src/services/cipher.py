import base64
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from loguru import logger

from utils import generate_hex_string


class Cipher:
    def __init__(self, key: str | None):
        if key is None:
            logger.trace("Disabled cipher")
            self.key = None
        else:
            logger.trace("Enabled cipher")
            self.key = key.encode()

    def encrypt(self, data: str) -> str:
        if self.key is None:
            return data

        iv_str = generate_hex_string(16)
        iv = iv_str.encode()

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        ciphertext = base64.b64encode(ciphertext_bytes).decode()

        logger.trace(f"Encrypt: {data} -({iv_str})-> {ciphertext}")

        encrypted_data = {
            'ciphertext': ciphertext,
            'iv': iv_str
        }

        return json.dumps(encrypted_data)
