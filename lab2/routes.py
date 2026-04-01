import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from datetime import datetime
from core.models import db, Content, Movie, Serial
from dal.implementations import SqlAlchemyRepository, CsvFileService
from bll.import_service import ContentManagerService

content_bp = Blueprint('content', __name__)

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
        item.duration = int(form.get('duration') or 0)
    elif item.type == 'serial':
        item.seasonsCount = int(form.get('seasonsCount') or 0)
        item.episodesCount = int(form.get('episodesCount') or 0)


@content_bp.route('/')
def index():
    catalog = service.get_all_content()
    return render_template('index.html', catalog=catalog)

@content_bp.route('/import', methods=['POST'])
def start_import():
    file = request.files.get('file')
    if file and file.filename.endswith('.csv'):
        path = os.path.join(os.getcwd(), 'data.csv')
        file.save(path)
        try:
            db.session.execute(db.delete(Movie))
            db.session.execute(db.delete(Serial))
            db.session.execute(db.delete(Content))
            db.session.commit()
            service.process_import(path)
            flash('Data imported successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Import error: {e}', 'danger')
        finally:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except PermissionError:
                    pass
    else:
        flash('Please upload a valid CSV file.', 'warning')

    return redirect(url_for('content.index'))

@content_bp.route('/add', methods=['GET', 'POST'])
def add_content():
    if request.method == 'POST':
        ctype = request.form.get('type')
        new_item = Movie() if ctype == 'movie' else Serial()
        
        new_item.type = ctype 
        
        fill_item_from_form(new_item, request.form)
        db.session.add(new_item)
        db.session.commit()
        flash(f'"{new_item.title}" successfully added!', 'success')
        return redirect(url_for('content.index'))
    
    return render_template('form.html', item=None)

@content_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_content(id):
    item = Content.query.get_or_404(id)
    if request.method == 'POST':
        fill_item_from_form(item, request.form)
        db.session.commit()
        flash(f'Changes for "{item.title}" saved successfully!', 'success')
        return redirect(url_for('content.index'))
    
    return render_template('form.html', item=item)

@content_bp.route('/delete/<int:id>', methods=['POST'])
def delete_content(id):
    service.remove_content(id)
    flash('Record deleted.', 'warning')
    return redirect(url_for('content.index'))