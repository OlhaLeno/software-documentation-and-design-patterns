import os
from dotenv import load_dotenv
from processor import DataProcessor
from strategies import ConsoleOutputStrategy, RedisOutputStrategy, KafkaOutputStrategy, FirebaseOutputStrategy

def get_strategy_from_config():
    """Factory method to select a strategy based on configuration"""
    strategy_name = os.getenv('OUTPUT_STRATEGY', 'console').lower()

    if strategy_name == 'redis':
        return RedisOutputStrategy(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            key=os.getenv('REDIS_KEY', 'nypd_shootings')
        )
    elif strategy_name == 'kafka':
        return KafkaOutputStrategy(
            servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            topic=os.getenv('KAFKA_TOPIC', 'nypd_shootings_topic')
        )
    elif strategy_name == 'firebase':
        return FirebaseOutputStrategy(
            cred_path=os.getenv('FIREBASE_CREDENTIALS', 'firebase-key.json'),
            collection_name=os.getenv('FIREBASE_COLLECTION', 'nypd_shootings')
        )
    else:
        return ConsoleOutputStrategy()

if __name__ == "__main__":
    load_dotenv()
    
    input_file = os.getenv('DATASET_PATH', 'data/NYPD_Shooting_Incident_Data.csv')
    output_file = os.getenv('OUTPUT_FILE_PATH', 'data/output_data.json')

    active_strategy = get_strategy_from_config()

    processor = DataProcessor(active_strategy)
    
    processor.process(input_file, output_file)