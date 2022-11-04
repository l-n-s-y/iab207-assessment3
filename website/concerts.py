import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Concert, Ticket, Comment
from .forms import ConcertForm, TicketPurchaseForm, CommentForm
from flask_login import login_required
from . import db, app
import os
from werkzeug.utils import secure_filename


bp = Blueprint('concert',__name__,url_prefix='/concerts')

@bp.route('/<id>', methods=["GET","POST"])
def show(id):
    concert = Concert.query.filter_by(id=id).first()

    ticket_form = TicketPurchaseForm()
    comment_form = CommentForm()
    if ticket_form.validate_on_submit():
        print("VALIDATED")
        current_user = "CURRENT USER"
        for i in range(int(ticket_form.ticket_quantity.data)):
            ticket = Ticket(
                event_id=id,
                ticket_owner=current_user, # REPLACE
                )
            db.session.add(ticket)
            db.session.commit()

        ticket_id = db.session.execute(f"SELECT id FROM tickets WHERE event_id='{id}' AND ticket_owner='{current_user}'").all()[-1][0]

        return redirect(url_for('concert.ticketview',id=ticket_id))

    sold_out = False
    sold_tickets = len(db.session.execute(f"SELECT * FROM tickets WHERE event_id='{id}'").all())
    available_tickets = db.session.execute(f"SELECT ticket_count FROM concerts WHERE id='{id}'").first()[0]
    print(f"Sold: {sold_tickets}")
    print(f"Available: {available_tickets}")
    if (sold_tickets >= available_tickets):
        sold_out = True
        print("Sold out")
    
    return render_template("concerts/event-details.html",concert=concert,ticket_form=ticket_form,sold_out=sold_out,comment_form=comment_form)

event_id = None
@bp.route("/create",methods = ["GET","POST"])
@login_required
def create():
    print(f"Event creation method type: {request.method}")
    form = ConcertForm()
    if form.validate_on_submit():
        #if request.method == "POST":
        event_name = form.event_name.data
        db_file_path=check_upload_file(form)
        concert = Concert(
                event_creator=current_user.username,
                event_name=event_name,
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
        event_id = db.session.execute(f"SELECT * FROM concerts WHERE event_name='{event_name}'").first()[0]

        return redirect(url_for('concert.show',id=event_id))
    return render_template('concerts/event-creation.html',form=form)

def check_upload_file(form):
    fp = form.event_image.data
    filename = "event_image_"+str(event_id)+"."+(fp.filename.split(".")[-1])

    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(BASE_PATH,'static/assets/img/event_images',secure_filename(filename))

    db_upload_path = '/static/assets/img/event_images/'+secure_filename(filename)

    fp.save(upload_path)
    return db_upload_path


@bp.route('/ticket-<id>')
def ticketview(id):
    ticket = Ticket.query.filter_by(id=id).first()
    concert = Concert.query.filter_by(id=ticket.event_id).first()

    return render_template('concerts/ticket-view.html',ticket=ticket,concert=concert)

@bp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
  #here the form is created  form = CommentForm()
  form = CommentForm()
  concert_obj = Concert.query.filter_by(id=id).first()
  if form.validate_on_submit():	#this is true only in case of POST method
    comment = Comment(
        concert_id=id,
        text=form.comment.data,
        user_id="CURRENT USER" # REPLACE
        )
    db.session.add(comment)
    db.session.commit()
    print("The following comment has been posted:", form.text.data)
  # notice the signature of url_for
  return redirect(url_for('concerts.event-details',id=id))