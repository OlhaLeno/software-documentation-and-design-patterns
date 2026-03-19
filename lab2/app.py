from flask import Flask
from core.models import db

from routes import content_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netflix.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'netflix-secret-key-english'

db.init_app(app)

app.register_blueprint(content_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)