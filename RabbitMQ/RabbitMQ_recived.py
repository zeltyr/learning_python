import pika, sys, os
from decouple import config

name = config('name')
password = config('password')
host = config('host')
port = config('port')

def main():

    # установка connection (соединения)
    credentials = pika.PlainCredentials(name, password)

    # ВАЖНО! Надо слушать порт 5672 (или тот, на который этот порт проброшен при запуске докера)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, credentials=credentials))

    # создание нового channel (канала)
    channel = connection.channel() 
 
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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