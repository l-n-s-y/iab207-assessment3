import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Concert, Ticket, Comment
from .forms import ConcertForm, TicketPurchaseForm, CommentForm
from flask_login import login_required, current_user
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
    available_tickets = db.session.execute(f"SELECT ticket_count FROM concerts WHERE id='{id}'").first()
    if not available_tickets:
        sold_out = True
    else:
        print(f"Sold: {sold_tickets}")
        print(f"Available: {available_tickets[0]}")
        if (sold_tickets >= available_tickets[0]):
            sold_out = True
            print("Sold out")
    
    return render_template("concerts/event-details.html",concert=concert,ticket_form=ticket_form,sold_out=sold_out,comment_form=comment_form)

@bp.route("/create",methods = ["GET","POST"])
@login_required
def create():
    print("CREATING")
    form = ConcertForm()
    if form.validate_on_submit():
        #if request.method == "POST":
        # event_name = form.event_name.data
        print("Validated")
        db_file_path=get_upload_file_path(form)
        concert = Concert(
                event_creator=current_user.username,
                event_name=form.event_name.data,
                event_description=form.event_description.data,
                event_date=form.event_date.data,
                event_genre=form.genre.data,
                event_venue=form.venue.data,
                ticket_count=form.ticket_count.data,
                ticket_price=form.ticket_price.data,
                event_status=form.status.data,
                event_image=db_file_path)
        db.session.add(concert)
        db.session.commit()
        print("Concert added")

        # Get newly created concert ID
        # event_id = db.session.execute(f"SELECT * FROM concerts WHERE event_name='{form.event_name.data}'").first()[0]
        event_id = Concert.query.filter_by(event_name=form.event_name.data).all()[-1].id

        return redirect(url_for('concert.show',id=event_id))

    return render_template('concerts/event-creation.html',form=form)

@bp.route('/update/<id>',methods=["GET","POST"])
@login_required
def update(id):
    form = ConcertForm()
    print("UPDATING")
    if form.validate_on_submit():
        print("VALIDATED")
        if request.form['submit'] == "Update Event":
            update_event = Concert.query.filter_by(id=id).first()

            db_file_path=get_upload_file_path(form)
            
            update_event.event_creator=current_user.username
            update_event.event_name=form.event_name.data
            update_event.event_description=form.event_description.data
            update_event.event_date=form.event_date.data
            update_event.event_genre=form.genre.data
            update_event.event_venue=form.venue.data
            update_event.ticket_count=form.ticket_count.data
            update_event.ticket_price=form.ticket_price.data
            update_event.event_image=db_file_path
            
            db.session.commit()


            return redirect(url_for('concert.show',id=update_event.id))
        if request.form['submit'] == "Delete Event":
            Concert.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(url_for('main.index'))

    # existing_concert = db.session.execute(f"SELECT * FROM concerts WHERE id='{id}'").first()
    existing_concert = Concert.query.filter_by(id=id).first()
    return render_template('concerts/event-creation.html',form=form,update=True,concert=existing_concert)

def get_upload_file_path(form):
    fp = form.event_image.data
    filename = "event_image_"+str(form.event_name.data)+"."+(fp.filename.split(".")[-1])

    BASE_PATH = os.path.dirname(__file__)


    if os.name == "nt":
        upload_path = os.path.join('static','assets','img','event_images',secure_filename(filename))
        db_upload_path = '\\static\\assets\\img\\event_images\\'+secure_filename(filename)
    else:
        upload_path = os.path.join(BASE_PATH,'static','assets','img','event_images',secure_filename(filename))
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
    form = CommentForm()
    concert = Concert.query.filter_by(id=id).first()
    if form.validate_on_submit():
        comment = Comment(
            event_id=id,
            comment_owner=current_user.username,
            comment=form.comment.data
        )
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('concerts.event-details',id=concert))