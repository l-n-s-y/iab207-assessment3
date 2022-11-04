from flask import Blueprint,render_template, redirect, url_for
from .models import Concert
from flask_login import login_required
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    concerts = Concert.query.all()
    return render_template('/landing.html',concerts=concerts)

@bp.route('/history')
@login_required
def history():
    return render_template('/booking-history.html')

@bp.route('/redirectToEvents')
def redirectToEvents():
    return redirect(url_for('main.index') + '#events-view')

@bp.route('/login')
def login():
    return render_template('/login.html')

@bp.route('/register')
def register():
    return render_template('/signup.html')
