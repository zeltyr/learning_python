import pika
from decouple import config


def send(queue_header, routing_key, fio=''):

    name = config('name')
    password = config('password')
    host = config('host')
    port = config('port')

    # queue_header = 'registration'
    # routing_key = 'registration'

    credentials = pika.PlainCredentials(name, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, port, credentials=credentials))

    channel = connection.channel()

    channel.queue_declare(queue=queue_header)
    channel.basic_publish(exchange='',
                          routing_key=routing_key,
                          body=fio)

    connection.close()

def recive(queue_header):

    name = config('name')
    password = config('password')
    host = config('host')
    port = config('port')

    credentials = pika.PlainCredentials(name, password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, port, credentials=credentials))

    channel = connection.channel()

    for method_frame, body in channel.consume(queue_header):
        
        body_message = body
        channel.basic_ack(method_frame.delivery_tag)

        if method_frame.delivery_tag == 1:
            break
    
    requeued_message = channel.cancel()
    print('Requeued %i messages' % requeued_message)
   
    channel.close()
    connection.close()
    
    return body_message