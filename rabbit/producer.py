import pika

# Устанавливаем соединение с сервером RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))
channel = connection.channel()

# Объявляем очередь, в которую будем отправлять сообщения
channel.queue_declare(queue='hello')

# Отправляем сообщение в очередь
channel.basic_publish(exchange='', routing_key='hello', body='Hello, World!')

print(" [x] Sent 'Hello, World!'")
connection.close()