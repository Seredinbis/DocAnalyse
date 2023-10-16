import pika
import os
import logging

from config_data.config import load_config

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


def doc_analyse_queue(doc_id):
    try:
        logger.info(f'enter to queu {doc_id}')
        # Устанавливаем соединение с сервером RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_ip, port=rabbit_port))
        channel = connection.channel()

        # Объявляем очередь, в которую будем отправлять сообщения
        channel.queue_declare(queue='doc_analyse')

        # Отправляем сообщение в очередь
        channel.basic_publish(exchange='', routing_key='doc_analyse', body=doc_id)

        logger.info(f" [x] Sent {doc_id}")

        connection.close()
    except ConnectionError:
        logger.exception("Ошибка")
