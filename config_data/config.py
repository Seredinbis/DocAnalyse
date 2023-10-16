from dataclasses import dataclass
from environs import Env


@dataclass()
class DataBase:
    token: str       # токен для телеграмм бот


@dataclass
class Config:
    data_base: DataBase


def load_config(path) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(data_base=DataBase(token=env('DB_URL')))