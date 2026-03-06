import csv
from core.interfaces import IContentRepository, IFileService
from core.models import db

class SqlAlchemyRepository(IContentRepository):
    def add(self, entity):
        db.session.add(entity)
    
    def commit(self):
        db.session.commit()

class CsvFileService(IFileService):
    def get_data_from_file(self, path):
        with open(path, mode='r', encoding='utf-8') as f:
            line = f.readline()
            if not line.startswith('sep='):
                f.seek(0)
            
            reader = csv.DictReader(f, skipinitialspace=True)
            return list(reader)