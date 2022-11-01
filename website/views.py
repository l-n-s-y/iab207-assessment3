from flask import Blueprint,render_template
from .models import Concert
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    concerts = Concert.query.all()
    return render_template('index.html',concerts=concerts)
