import base64
from pathlib import Path

import aiofiles
import aiofiles.os

from config import CONFIG


ICON_DIR = Path(CONFIG.STATIC_DIR) / "icons"

ICON_DIR.mkdir(parents=True, exist_ok=True)

async def get_all() -> list[str]:
    files = await aiofiles.os.listdir(ICON_DIR)
    icons = []
    for file in files:
        if file.endswith(".png"):
            icons.append(file[:-4])
    return icons


async def add_icon(name: str, data: str):
    data = base64.b64decode(data)
    async with aiofiles.open(ICON_DIR / f"{name}.png", "wb") as f:
        await f.write(data)


async def delete_icon(name: str):
    if (ICON_DIR / f"{name}.png").exists():
        await aiofiles.os.remove(ICON_DIR / f"{name}.png")

images_cache = []

async def get_image_url(image: str) -> str | None:
    global images_cache
    if image in images_cache:
        return f"{CONFIG.STATIC_URL}/{image}.png"

    images_cache = await get_all()
    if image in images_cache:
        return f"{CONFIG.STATIC_URL}/{image}.png"

    return None


async def main():
    print(await get_all())
    await add_icon("test", "")
    print(await get_all())
    await delete_icon("test")
    print(await get_all())
    await delete_icon("test")
    print(await get_all())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
