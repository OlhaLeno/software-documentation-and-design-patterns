import csv
import sys
import random
from faker import Faker

def generate(count=1000):
    fake = Faker()
    fieldnames = [
        'title', 'type', 'description', 'releaseDate', 
        'rating', 'genre', 'director', 'duration', 
        'seasonsCount', 'episodesCount'
    ]
    
    with open('data.csv', 'w', newline='', encoding='utf-8') as f:
        f.write('sep=,\n')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.header_written = False
        
        writer.writeheader()
        
        for _ in range(count):
            c_type = fake.random_element(['movie', 'serial'])
            
            rating_num = round(random.uniform(1.0, 9.9), 1)
            
            rating_str = f" {rating_num}"
            
            if c_type == 'movie':
                duration = random.randint(75, 165)
                seasons = 0
                episodes = 0
            else:
                duration = 0
                seasons = random.randint(1, 8)
                episodes = seasons * random.randint(4, 14) 
            
            row = {
                'title': fake.catch_phrase(),
                'type': c_type,
                'description': fake.paragraph(nb_sentences=2),
                'releaseDate': fake.date_between(start_date='-25y', end_date='today').strftime('%Y-%m-%d'),
                'rating': rating_str,
                'genre': fake.random_element(['Drama', 'Comedy', 'Action', 'Sci-Fi', 'Horror', 'Documentary']),
                'director': fake.name(),
                'duration': duration,
                'seasonsCount': seasons,
                'episodesCount': episodes
            }
            writer.writerow(row)
            
    print(f"Data updated! {count} realistic strings generated in data.csv.")
    
if __name__ == "__main__":
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    generate(num)