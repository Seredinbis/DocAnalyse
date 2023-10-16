import os

from config_data.config import load_config
from celery import Celery
from sql.psql import DocumentText, engine
from celery.backends.database import DatabaseBackend


abspath = os.path.abspath('.env')
config = load_config(abspath)
rabbit_user = config.rabbit.rab_user
rabbit_password = config.rabbit.rab_password
rabbit_ip = config.rabbit.rab_ip
rabbit_port = config.rabbit.rab_port
db_url = config.data_base.token


app = Celery('my_app', broker=f'amqp://{rabbit_user}:{rabbit_password}@{rabbit_ip}:{rabbit_port}//',
             backend=db_url)

backend = DatabaseBackend(app=app, engine=engine, taskmodel=DocumentText)
