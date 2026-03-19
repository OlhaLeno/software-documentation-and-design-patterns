import csv
from core.interfaces import IContentRepository, IFileService
from core.models import Content, db

class SqlAlchemyRepository(IContentRepository):
    def add(self, entity):
        db.session.add(entity)
    
    def commit(self):
        db.session.commit()
    
    def get_all(self):
        return Content.query.all()

    def get_by_id(self, content_id):
        return Content.query.get(content_id)

    def delete(self, entity):
        db.session.delete(entity)
        
class CsvFileService(IFileService):
    def get_data_from_file(self, path):
        with open(path, mode='r', encoding='utf-8') as f:
            line = f.readline()
            if not line.startswith('sep='):
                f.seek(0)
            
            reader = csv.DictReader(f, skipinitialspace=True)
            return list(reader)