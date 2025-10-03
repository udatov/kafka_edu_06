from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'kafka-0:9092,kafka-1:9092,kafka-2:9092',
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['module_6'])

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue
    print(f"Received message: {msg.value().decode('utf-8')}")
    break

consumer.close()
