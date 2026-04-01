from datetime import datetime
from core.models import Movie, Serial, Content
from core.interfaces import IContentRepository, IFileService

class ContentManagerService:
    def __init__(self, repo: IContentRepository, file_service: IFileService = None):
        self.repo = repo
        self.file_service = file_service

    def process_import(self, file_path: str):
        data = self.file_service.get_data_from_file(file_path)
        
        for row in data:
            row = {k.strip(): v for k, v in row.items() if k is not None}
            
            if 'type' not in row:
                continue

            release_date = None
            raw_date = row.get('releaseDate')
            if raw_date:
                try:
                    release_date = datetime.strptime(raw_date.strip(), '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    release_date = None

            if row['type'].strip() == 'movie':
                obj = Movie(
                    title=row.get('title'),
                    description=row.get('description'),
                    releaseDate=release_date,
                    rating=float(row.get('rating', 0)) if row.get('rating') else None,
                    genre=row.get('genre'),
                    director=row.get('director'),
                    duration=int(row.get('duration', 0)) if row.get('duration') else 0
                )
            else:
                obj = Serial(
                    title=row.get('title'),
                    description=row.get('description'),
                    releaseDate=release_date,
                    rating=float(row.get('rating', 0)) if row.get('rating') else None,
                    genre=row.get('genre'),
                    director=row.get('director'),
                    seasonsCount=int(row.get('seasonsCount', 0)) if row.get('seasonsCount') else 0,
                    episodesCount=int(row.get('episodesCount', 0)) if row.get('episodesCount') else 0
                )
            
            self.repo.add(obj)
            
        self.repo.commit()

    def get_all_content(self):
        """Business logic data validation"""
        return Content.query.all()

    def remove_content(self, content_id: int):
        """Business logic for removing data)"""
        item = Content.query.get(content_id)
        if item:
            from core.models import db
            db.session.delete(item)
            db.session.commit()