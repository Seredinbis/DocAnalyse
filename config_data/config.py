from dataclasses import dataclass
from environs import Env


@dataclass()
class DataBase:
    db_host: str
    db_ip: str
    db_name: str
    db_port: str
    db_pass: str
    db_name: str
    db_user: str
    token: str


@dataclass()
class Rabbit:
    rab_ip: str
    rab_port: int
    rab_user: str
    rab_password: str


@dataclass
class DocumentsPath:
    path: str


@dataclass
class Config:
    data_base: DataBase
    rabbit: Rabbit
    doc_path: DocumentsPath


def load_config(path) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(data_base=DataBase(token=env('DB_URL'), db_host=env('DB_HOST'), db_ip=env('DB_IP'), db_port=env('DB_PORT'),
                                     db_name=env('DB_NAME'), db_user=env('DB_USER'), db_pass=env('DB_PASSWORD')),
                  rabbit=Rabbit(rab_ip=env('RABBIT_IP'), rab_port=env('RABBIT_PORT'),
                                rab_user=env('RABBIT_USER'), rab_password=env('RABBIT_PASSWORD')),
                  doc_path=DocumentsPath(path=env('DOC_PATH')))
