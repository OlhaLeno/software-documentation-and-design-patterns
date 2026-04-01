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

class FirebaseOutputStrategy(IOutputStrategy):
    def __init__(self, cred_path: str, collection_name: str):
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
        self.collection_name = collection_name

    def output(self, data):
        from google.api_core.exceptions import ResourceExhausted, RetryError 

        print(f"--- Sending data to Firebase Firestore (collection: {self.collection_name}) ---")
        collection_ref = self.db.collection(self.collection_name)
        
        batch = self.db.batch()
        total_written = 0
        batch_count = 0
        
        print(f"Uploading {len(data)} records in batches... Please wait.")
        
        try:
            for row in data:
                doc_ref = collection_ref.document()
                batch.set(doc_ref, row)
                batch_count += 1
                
                if batch_count == 400:
                    batch.commit()
                    total_written += batch_count
                    print(f"Uploaded {total_written} records...")
                    batch = self.db.batch()
                    batch_count = 0
            
            if batch_count > 0:
                batch.commit()
                total_written += batch_count
                
            print(f"Successfully sent {total_written} records to Firebase Firestore.")
            
        except (ResourceExhausted, RetryError):
            print(f"\nWarning: Reached the daily Firebase limit (20,000 records) or timeout!")
            print(f"{total_written} records were successfully saved to the cloud during this run.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")