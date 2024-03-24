import os

from config_data.config import load_config
from celery import Celery

abspath = os.path.abspath('.env')
config = load_config(abspath)
rabbit_user = config.rabbit.rab_user
rabbit_password = config.rabbit.rab_password
rabbit_ip = config.rabbit.rab_ip
rabbit_port = config.rabbit.rab_port
db_url = config.data_base.token

app = Celery('celery_setup', broker=f'amqp://guest:guest@{rabbit_ip}:{rabbit_port}//')

app.autodiscover_tasks(['celery_module.tasks'])
