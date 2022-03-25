import pika, sys, os, json
import app.mongoDB as mongoDB
from decouple import config

name = config('name')
password = config('password')
host = config('host')
port = config('port')

def callback(ch, method, properties, body):
   
    body_str = body.decode("utf-8")[:4000]
    templates = json.loads(body_str)
    
    users_collection = mongoDB.init_collection('users')
    result = mongoDB.find_document(users_collection, templates)
    
    if result == None:
        mongoDB.insert_document(users_collection, templates)

def main():

    # установка connection (соединения)
    credentials = pika.PlainCredentials(name, password)

    # ВАЖНО! Надо слушать порт 5672 (или тот, на который этот порт проброшен при запуске докера)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, port, credentials=credentials))

    # создание нового channel (канала)
    channel = connection.channel()

    channel.queue_declare(queue='fio')

    channel.basic_consume(
        queue='fio', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
