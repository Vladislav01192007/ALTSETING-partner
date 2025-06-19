# backend/app.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from auth import auth_bp
from dashboard import dashboard_bp
import os

app = Flask(__name__)
app.secret_key = os.getenv('YOUR_SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///partners.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'partner_id' in session:
        partner = db.session.get(Partner, session['partner_id'])
        return render_template('dashboard.html', partner=partner)
    return redirect(url_for('login'))

@app.route('/confirm/<int:id>')
def confirm(id):
    partner = db.session.get(Partner, id)
    if not partner:
        return 'Партнер не знайдений.', 404
    partner.confirmed = True
    db.session.commit()
    return f"Партнера {partner.email} підтверджено."

if __name__ == '__main__':
    if not os.path.exists('partners.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
else:
    if not os.path.exists('partners.db'):
        with app.app_context():
            db.create_all()
