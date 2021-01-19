from typing import Optional

from pydantic import BaseSettings, PrivateAttr
import logging
import os

file_dir = os.path.split(os.path.realpath(__file__))[0]

logging.config.fileConfig(os.path.join(file_dir, 'logging.conf'), disable_existing_loggers=False)


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    app_desc: str = ""
    app_version: str = ""
    base_url_ws: str = ""
    jwt_secret: str = ""
    jwt_alg: str = "HS256"
    jwt_expire_minute: Optional[int] = None
    _jwt_settings: dict = PrivateAttr()
    default_dn: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._jwt_settings = {
            "secret": self.jwt_secret,
            "alg": self.jwt_alg,
            "expire_minute": self.jwt_expire_minute,
        }

    class Config:
        env_file = ".env"
