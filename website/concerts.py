from flask import Blueprint, render_template, request, redirect, url_for
from .models import Concert
from .forms import ConcertForm
from . import db, app
import os
from werkzeug.utils import secure_filename


bp = Blueprint('concert',__name__,url_prefix='/concerts')

@bp.route('/<id>')
def show(id):
    concert = Concert.query.filter_by(id=id).first()

    #cform = CommentForm()
    
    return render_template("concerts/event-details.html",concert=concert)#,form=cform)

@bp.route("/create",methods = ["GET","POST"])
#@login_required
def create():
    print(f"Event creation method type: {request.method}")
    form = ConcertForm()
    #if form.validate_on_submit():
    if request.method == "POST":
        db_file_path=check_upload_file(form)
        concert = Concert(
                event_name=form.event_name.data,
                event_description=form.event_description.data,
                event_date=form.event_date.data,
                event_genre=form.genre.data,
                event_venue=form.venue.data,
                ticket_count=form.ticket_count.data,
                ticket_price=form.ticket_price.data,
                event_image=db_file_path)
        db.session.add(concert)
        db.session.commit()

        # Get newly created concert ID
        event_id = db.session.execute(f"SELECT * FROM concerts WHERE event_name='{form.event_name.data}'").first()[0]
        print(f"Event id: {event_id}")

        print("Concert created successfully.")

        #@return redirect(url_for(f'concert.{event_id}'))
        return redirect(url_for('concert.show',id=event_id))

        #return redirect(url_for('concert.create'))
        #return render_template('concerts/show.html')
    #return render_template('concerts/create.html',form=form)
    print("Loaded form")
    return render_template('concerts/event-creation.html',form=form)

def check_upload_file(form):
    fp = form.event_image.data
    filename = fp.filename

    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))

    db_upload_path = '/static/image/'+secure_filename(filename)

    fp.save(upload_path)
    return db_upload_path

