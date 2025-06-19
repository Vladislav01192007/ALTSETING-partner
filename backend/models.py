from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    eth_wallet = db.Column(db.String(42))  # Ethereum адреса
    sol_wallet = db.Column(db.String(44))  # Solana адреса
