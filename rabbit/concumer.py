import pika
import os
import logging

from config_data.config import load_config
from celery_module.tasks import doc_analyse

abspath = os.path.abspath('.env')
config = load_config(abspath)
rabbit_ip = config.rabbit.rab_ip
rabbit_port = config.rabbit.rab_port

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


# Функция обработки полученного сообщения
def callback(channel, method, properties, body):
    try:
        logger.info('вход в целери')
        doc_analyse.delay(body)
        logger.info('такска выполнена')
        return {'таска': 'такса'}
    except BaseException as ex:
        logger.exception(f'{ex}ошибка')


def concumer_connect():
    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_ip, port=rabbit_port))
    channel = connection.channel()
    # Объявляем очередь, в которую будем отправлять сообщения
    channel.queue_declare(queue='doc_analyse')

    # Подписываемся на очередь и указываем функцию обработки сообщений
    channel.basic_consume(queue='doc_analyse', on_message_callback=callback, auto_ack=True, consumer_tag='lonely')

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
