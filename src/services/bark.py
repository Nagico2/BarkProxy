import aiohttp
import json
from typing import Optional

from services.cipher import Cipher


class BarkNotifier:
    def __init__(self, end_point: str, api_key: str, encryption_key: Optional[str] = None):
        self.api_key = api_key
        self.end_point = end_point
        if not self.end_point.startswith("http"):
            self.end_point = f"http://{self.end_point}"

        if not self.end_point.endswith("/"):
            self.end_point = f"{self.end_point}/"

        self.url_endpoint = f"{self.end_point}{self.api_key}"
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        self.session = None

        self.cipher = Cipher(encryption_key)

    async def __aenter__(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.session is not None:
            await self.session.close()

    class NotificationLevel:
        CRITICAL = "critical"
        ACTIVE = "active"
        TIME_SENSITIVE = "timeSensitive"
        PASSIVE = "passive"

    async def send(
        self,
        title: str,
        body: str,
        subtitle: Optional[str] = None,
        level: Optional[str] = NotificationLevel.ACTIVE,
        auto_copy: Optional[bool] = None,
        copy: Optional[str] = None,
        icon: Optional[str] = None,
        image: Optional[str] = None,
        group: Optional[str] = None,
        is_archive: Optional[bool] = None,
        url: Optional[str] = None
    ):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        data = {
            "title": title,
            "body": body,
            "subtitle": subtitle,
            "level": level,
            "autoCopy": 1 if auto_copy else 0 if auto_copy is not None else None,
            "copy": copy,
            "icon": icon,
            "image": image,
            "group": group,
            "isArchive": 1 if is_archive else 0 if is_archive is not None else None,
            "url": url
        }

        # Remove keys with None values
        data = {k: v for k, v in data.items() if v is not None}
        data_str = json.dumps(data)

        encrypted_data = self.cipher.encrypt(data_str)

        async with self.session.post(self.url_endpoint, headers=self.headers, data=encrypted_data) as response:
            response_data = await response.text()
            print(response_data)
