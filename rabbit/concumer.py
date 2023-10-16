import pika

# Устанавливаем соединение с сервером RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))
channel = connection.channel()

# Объявляем очередь, из которой будем получать сообщения
channel.queue_declare(queue='hello')


# Функция обработки полученного сообщения
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# Подписываемся на очередь и указываем функцию обработки сообщений
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()