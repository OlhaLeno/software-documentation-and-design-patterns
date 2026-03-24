import csv
import json
from interfaces import IOutputStrategy

class DataProcessor:
    def __init__(self, strategy: IOutputStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: IOutputStrategy):
        """Allows changing the strategy at runtime"""
        self._strategy = strategy

    def process(self, input_path: str, output_path: str):
        data = []
        
        try:
            with open(input_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data.append(row)
            print(f"Read {len(data)} rows from {input_path}")
        except FileNotFoundError:
            print("Error: Input file not found!")
            return

        with open(output_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to file {output_path}")

        self._strategy.output(data)