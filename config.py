from dataclasses import dataclass
from environs import Env


@dataclass
class Token:
    token: str

@dataclass
class Config:
    tg_bot: Token


def load_config(path: str | None=None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=Token(token=env('TOKEN')))

#----------------------------------------------------------------

@dataclass
class DB_config:
    db_config: str


def load_db_config(path: str | None=None) -> DB_config:
    env = Env()
    env.read_env(path)
    return DB_config(db_config=env('DB_URL'))