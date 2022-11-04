from flask import Blueprint,render_template, redirect, url_for
from .models import Concert
from flask_login import login_required
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    concerts = Concert.query.all()
    row_count = len(concerts)//4
    if (row_count == 0): row_count = 1
    print(f"Row count: {row_count}")
    return render_template('/landing.html',row_count=row_count,concerts=concerts)

@bp.route('/history')
@login_required
def history():
    return render_template('/booking-history.html')

@bp.route('/redirectToEvents')
def redirectToEvents():
    return redirect(url_for('main.index') + '#events-view')

# @bp.route('/login')
# def login():
#     return render_template('/login.html')

# @bp.route('/register')
# def register():
#     return render_template('/signup.html')
