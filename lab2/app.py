from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime
from core.models import db, Content, Movie, Serial
from dal.implementations import SqlAlchemyRepository, CsvFileService
from bll.import_service import ContentManagerService

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netflix.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'netflix-secret-key-english'

db.init_app(app)

repo = SqlAlchemyRepository()
file_svc = CsvFileService()
service = ContentManagerService(repo, file_svc)

def fill_item_from_form(item, form):
    item.title = form.get('title')
    item.description = form.get('description')
    item.genre = form.get('genre')
    item.director = form.get('director')
    item.rating = float(form.get('rating')) if form.get('rating') else 0.0
    
    date_str = form.get('releaseDate')
    if date_str:
        try:
            item.releaseDate = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            item.releaseDate = None

    if item.type == 'movie':
        item.duration = int(form.get('duration', 0))
    elif item.type == 'serial':
        item.seasonsCount = int(form.get('seasonsCount', 0))
        item.episodesCount = int(form.get('episodesCount', 0))

@app.route('/')
def index():
    catalog = service.get_all_content()
    return render_template('index.html', catalog=catalog, mode='list')

@app.route('/import')
def start_import():
    try:
        service.process_import('data.csv')
        flash('Data imported successfully!', 'success')
    except Exception as e:
        flash(f'Import error: {e}', 'danger')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_content():
    if request.method == 'POST':
        ctype = request.form.get('type')
        new_item = Movie() if ctype == 'movie' else Serial()
        fill_item_from_form(new_item, request.form)
        db.session.add(new_item)
        db.session.commit()
        flash(f'"{new_item.title}" successfully added!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', mode='form', item=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_content(id):
    item = Content.query.get_or_404(id)
    if request.method == 'POST':
        fill_item_from_form(item, request.form)
        db.session.commit()
        flash(f'Changes for "{item.title}" saved successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', mode='form', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_content(id):
    service.remove_content(id)
    flash('Record deleted.', 'warning')
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)