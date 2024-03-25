import os
from functools import lru_cache

from dotenv import load_dotenv

import config

dotenv_path = f"/app/.env"
load_dotenv(dotenv_path=dotenv_path)


@lru_cache()
def get_settings():
    return config.SettingsApp(**os.environ)
