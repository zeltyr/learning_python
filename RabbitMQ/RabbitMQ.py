import pika
from decouple import config

name = config('name')
password = config('password')
host = config('host')
port = config('port')

# установка connection (соединения)
credentials = pika.PlainCredentials(name, password)

# ВАЖНО! Надо слушать порт 5672 (или тот, на который этот порт проброшен при запуске докера)
connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, credentials=credentials))

# создание нового channel (канала)
channel = connection.channel()

# объявляем новую queue(очередь)
channel.queue_declare(queue='hello')

# в exchange(буфер) по умлочанию (так как имени нет), шлём body(сообщение) с routing_key(ключом маршрутизации) 'hello' 
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")

# закрываем соединение
connection.close()