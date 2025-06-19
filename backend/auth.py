from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Partner

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
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

