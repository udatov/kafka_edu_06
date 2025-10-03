from confluent_kafka import Producer
import json

conf = {
    'bootstrap.servers': 'kafka-0:9092,kafka-1:9092,kafka-2:9092',
    'client.id': 'python-producer'
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


message = {'id': '1', 'username': 'Ivan', 'registered': True}
producer.produce('module_6', value=json.dumps(message), key='user1', callback=delivery_report)
producer.flush()
