from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from models import db, Application
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail = Mail(app)

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/api/submit-application', methods=['POST'])
def submit_app():
    data = request.get_json()
    app_record = Application(**data)
    db.session.add(app_record)
    db.session.commit()

    msg = Message(
        subject="Нова партнерська заявка",
        recipients=[app.config['MAIL_USERNAME']],
    )
    msg.body = render_template('email_new_application.html', app=app_record)
    mail.send(msg)

    return jsonify({'status': 'ok'}), 200

@app.route('/api/confirm/<int:app_id>', methods=['POST'])
def confirm_app(app_id):
    app_rec = Application.query.get_or_404(app_id)
    app_rec.confirmed = True
    db.session.commit()
    return jsonify({'status': 'confirmed'}), 200

@app.route('/api/check-status/<int:app_id>', methods=['GET'])
def check_status(app_id):
    app_rec = Application.query.get_or_404(app_id)
    return jsonify({'confirmed': app_rec.confirmed}), 200

if __name__ == '__main__':
    app.run(debug=True)
