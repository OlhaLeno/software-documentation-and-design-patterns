import json
from interfaces import IOutputStrategy

class ConsoleOutputStrategy(IOutputStrategy):
    def output(self, data):
        print("--- Outputting to Console ---")
        for row in data[:5]:
            print(row)
        print(f"... and {len(data) - 5} more records.")

class RedisOutputStrategy(IOutputStrategy):
    def __init__(self, host: str, port: int, key: str):
        import redis
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.key = key

    def output(self, data):
        print(f"--- Sending data to Redis (key: {self.key}) ---")
        pipe = self.client.pipeline()
        for row in data:
            pipe.rpush(self.key, json.dumps(row))
        pipe.execute()
        print("Successfully sent to Redis.")

class KafkaOutputStrategy(IOutputStrategy):
    def __init__(self, servers: str, topic: str):
        from kafka import KafkaProducer
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def output(self, data):
        print(f"--- Sending data to Kafka (topic: {self.topic}) ---")
        for row in data:
            self.producer.send(self.topic, row)
        self.producer.flush()
        print("Successfully sent to Kafka.")