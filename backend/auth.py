# backend/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Partner

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json or request.form
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        eth_wallet = data.get('eth_wallet', '')
        sol_wallet = data.get('sol_wallet', '')

        if not name or not email or not password:
            return jsonify({'error': 'Заповніть усі обов’язкові поля.'}), 400

        if Partner.query.filter_by(email=email).first():
            return jsonify({'error': 'Email вже зареєстровано.'}), 400

        new_partner = Partner(
            name=name,
            email=email,
            password=generate_password_hash(password),
            eth_wallet=eth_wallet,
            sol_wallet=sol_wallet
        )
        db.session.add(new_partner)
        db.session.commit()
        return jsonify({'message': 'Реєстрація успішна!'}), 201

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json or request.form
        email = data.get('email')
        password = data.get('password')
        partner = Partner.query.filter_by(email=email).first()

        if partner and check_password_hash(partner.password, password):
            session['partner_id'] = partner.id
            return jsonify({'message': 'Вхід успішний!', 'redirect': url_for('dashboard.dashboard')}), 200
        return jsonify({'error': 'Невірний логін або пароль.'}), 401

    return render_template('login.html')
