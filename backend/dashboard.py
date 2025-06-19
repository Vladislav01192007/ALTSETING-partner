from flask import Flask
from models import db
from auth import auth_bp
from dashboard import dashboard_bp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///partners.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    return "<h2>Вітаємо у партнерській системі ALTSETING. Перейдіть до /register або /login</h2>"

if __name__ == '__main__':
    if not os.path.exists('partners.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

