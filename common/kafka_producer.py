from kafka import KafkaProducer
from time import sleep


class kafkaProducer(object):
    def __init__(self, bootstrap_servers: str) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda m: str(m).encode()
            )
        self.topic = None

    def set_topic(self, topic: str) -> None:
        self.topic = topic

    def send_msg(self, message: str, **kwargs) -> None:
        if self.topic is None:
            raise RuntimeError(f"send message to kafka must after call set_topic function to setup topic value.")
        self.producer.send(self.topic, message)
        if "delay" in kwargs.keys():
            sleep(kwargs.get("delay"))
        else:
            sleep(0.1)

