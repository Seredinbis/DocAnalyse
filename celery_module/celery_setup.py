import os
import logging

from config_data.config import load_config
from celery import Celery

abspath = os.path.abspath('.env')
config = load_config(abspath)
rabbit_user = config.rabbit.rab_user
rabbit_password = config.rabbit.rab_password
rabbit_ip = config.rabbit.rab_ip
rabbit_port = config.rabbit.rab_port
db_url = config.data_base.token

# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# настройка обработчика и форматировщика
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)

app = Celery('celery_setup', broker=f'amqp://guest:guest@{rabbit_ip}:{rabbit_port}//')

app.autodiscover_tasks(['celery_module.tasks'])
