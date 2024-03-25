import logging
import os
from typing import Optional

from pydantic import BaseModel, ConfigDict

file_dir = os.path.split(os.path.realpath(__file__))[0]

logging.config.fileConfig(os.path.join(file_dir, 'logging.conf'),
                          disable_existing_loggers=False)

def to_upper(string: str) -> str:
    return '_'.join(word.upper() for word in string.split('_'))


class Settings(BaseModel):
    model_config = ConfigDict(
        extra='ignore',
        alias_generator=to_upper
    )

    app_name: str = "Awesome API"
    app_desc: str = ""
    base_url_ws: str = ""
    camunda_url: str = ""
    app_process: str = ""
    jwt_secret: str = ""
    jwt_alg: str = "HS256"
    jwt_expire_minute: Optional[int] = None
    jwt_settings: dict = {}
    default_dn: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt_settings = {
            "secret": self.jwt_secret,
            "alg": self.jwt_alg,
            "expire_minute": self.jwt_expire_minute,
        }


class SettingsApp(Settings):
    people_url: str = ""
    people_key: str = ""
    followme_url: str = ""
    followme_key: str = ""
    ugov_pf: str = ""
    ugov_pf_token: str = ""
    mongo_url: str = ""
    mongo_user: str = ""
    mongo_pass: str = ""
    mongo_db: str = ""
    mongo_replica: str = ""
    server_datetime_mask: str = ""
    server_date_mask: str = ""
    ui_datetime_mask: str = ""
    ui_date_mask: str = ""
    time_zone: str = ""

    def get_sevice_dict(self, service_name):
        res = {}
        data = self.dict()
        for item in self.dict():
            if service_name in item:
                key = item.split("_")[1]
                res[key] = data[item]
        return res