from kafka import KafkaConsumer, consumer
import json


class MessageConsumer:

    def activate_listener(self, broker, topic, group_id):
        consumer = KafkaConsumer(bootstrap_servers=broker,
                                 group_id=group_id,
                                 consumer_timeout_ms=30000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                 )
        print("Dang lang nghe")
        consumer.subscribe(topics=topic)
        try:
            message = consumer.poll(1.0)
            print(message)

            if message:
                print("Lang nghe thanh cong")
                consumer.commit()
                self.process_msg(message)
                return message
        except Exception as e:
            print(e, flush=True)

    def process_msg(self, msg):
        print(msg)
