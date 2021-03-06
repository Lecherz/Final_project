from flask import json
import pika
import time
import logging
import warnings
import pymongo

# configure logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning) 



# connection configurations
connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbitmq', port=5672))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    #connect to db rs1
    myclient = pymongo.MongoClient('mongodb://%s:%s/' % ('rs1','27041'))
    db_1 = myclient["List_user"]
    mycol = db_1["User"]

    message = body.decode("utf-8") 
    logging.info('receive messages:' + message)
    time.sleep(body.count(b'.'))
    #check_mes And record data
    print(body)
    chkinf = json.loads(body)
    insrt = mycol.insert_one(chkinf)
    print(insrt)
    myclient.close()
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
