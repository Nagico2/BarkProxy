import sys
from pathlib import Path

from views import app
from config import CONFIG


sys.path.append(Path(__file__).resolve().parents[0].as_posix())

app.static('/statics', CONFIG.STATIC_DIR)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)