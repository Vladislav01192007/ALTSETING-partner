import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///app.db")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.sendgrid.net")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
