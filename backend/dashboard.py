# backend/dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from models import Partner

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'partner_id' in session:
        partner = db.session.get(Partner, session['partner_id'])
        return render_template('dashboard.html', partner=partner)
    return redirect(url_for('auth.login'))
