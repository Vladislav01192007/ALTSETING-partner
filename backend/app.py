from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///partners.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if Partner.query.filter_by(email=email).first():
            return 'Email вже зареєстровано.'

        new_partner = Partner(name=name, email=email, password=password)
        db.session.add(new_partner)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        partner = Partner.query.filter_by(email=email).first()

        if partner and check_password_hash(partner.password, password):
            session['partner_id'] = partner.id
            return redirect(url_for('dashboard'))
        return 'Невірний логін або пароль.'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'partner_id' in session:
        partner = Partner.query.get(session['partner_id'])
        return render_template('dashboard.html', partner=partner)
    return redirect(url_for('login'))

@app.route('/confirm/<int:id>')
def confirm(id):
    partner = Partner.query.get_or_404(id)
    partner.confirmed = True
    db.session.commit()
    return f"Партнера {partner.email} підтверджено."

if __name__ == '__main__':
    if not os.path.exists('partners.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

