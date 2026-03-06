from flask import Flask
from core.models import db, Content, Movie, Serial, Season, Episode 
from dal.implementations import SqlAlchemyRepository, CsvFileService
from bll.import_service import ContentManagerService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netflix.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

repo = SqlAlchemyRepository()
file_svc = CsvFileService()

service = ContentManagerService(repo, file_svc)

@app.route('/import')
def start_import():
    """
    Presentation layer. Does not perform logic, 
    only calls the BLL service method.
    """
    try:
        service.process_import('data.csv')
        return "Import completed successfully! Check the netflix.db database."
    except Exception as e:
        return f"Error occurred during import: {str(e)}", 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    
    print("Server started. Navigate to http://127.0.0.1:5000/import to trigger the import logic.")
    app.run(debug=True)