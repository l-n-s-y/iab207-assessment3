from flask import Blueprint,render_template, redirect, url_for, request
from .models import Concert
from flask_login import login_required
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    concerts = Concert.query.all()
    # row_count = (len(concerts)//4) + 1
    concert_count = len(concerts)

    # break_out = False
    events_present = len(concerts) > 0
    print(f"Drawing {len(concerts)} concerts")
    return render_template('/landing.html',events_present=events_present,concert_count=concert_count,concerts=concerts)

@bp.route('/history')
@login_required
def history():
    return render_template('/booking-history.html')

@bp.route('/redirectToEvents')
def redirectToEvents():
    return redirect(url_for('main.index') + '#events-view')

@bp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        conc = "%" + request.args['search'] + '%'
        concerts = Concert.query.filter(Concert.event_name.like(conc)).all()
        concert_count = len(concerts)
        events_present = len(concerts) > 0
        return render_template('/landing.html', concerts=concerts, events_present=events_present, concert_count=concert_count)
    else:
        return redirect(url_for('main.index'))
