
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, DateField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email"),
        EqualTo('email_confirmation',message="Emails should match")])
    email_confirmation = StringField("Confirm Email",validators=[InputRequired()])
    contact_number = StringField("Contact Number",validators=[InputRequired()])
    password=PasswordField("Password",validators=[InputRequired()])

    submit = SubmitField("Register")

ALLOWED_EXTENSIONS = ['png','jpg']
EVENT_STATUS = [
    ("Open","Open"),
    ("Unpublished","Unpublished"),
    ("Sold Out","Sold Out"),
    ("Cancelled","Cancelled"),
]

GENRES = [
        ('Alternative','Alternative'),
        ('Pop','Pop'),
        ('Indie','Indie'),
        ('Rock','Rock'),
        ('Soul','Soul')
        ]
# Create new Concert Events
class ConcertForm(FlaskForm):
    status = SelectField("Status",validators=[InputRequired()],choices=[(status[0],status[1]) for status in EVENT_STATUS])
    event_name = StringField("Concert Name",validators=[InputRequired()])
    event_description = TextAreaField("Event Description",validators=[InputRequired()])
    event_date = DateField("Event Date",validators=[InputRequired()])

    genre = SelectField("Genre",validators=[InputRequired()],choices=[(genre[0],genre[1]) for genre in GENRES])

    venue = StringField("Venue Location",validators=[InputRequired()])
    ticket_count = IntegerField("Ticket Count",validators=[InputRequired()])
    ticket_price = StringField("Ticket Price",validators=[InputRequired()])
    event_image = FileField("Event Image",validators=[
        FileRequired(message="Image is required"),
        FileAllowed(ALLOWED_EXTENSIONS,message="Image must be png or jpg")])

    submit = SubmitField("Submit")

# class UpdateForm(FlaskForm):
#     status = SelectField("Status",validators=[InputRequired()],choices=[(status[0],status[1]) for status in EVENT_STATUS])
#     event_name = StringField("Concert Name",validators=[InputRequired()])
#     event_description = TextAreaField("Event Description",validators=[InputRequired()])
#     event_date = DateField("Event Date",validators=[InputRequired()])

#     genre = SelectField("Genre",validators=[InputRequired()],choices=[(genre[0],genre[1]) for genre in GENRES])

#     venue = StringField("Venue Location",validators=[InputRequired()])
#     ticket_count = IntegerField("Ticket Count",validators=[InputRequired()])
#     ticket_price = StringField("Ticket Price",validators=[InputRequired()])
#     event_image = FileField("Event Image",validators=[
#         FileRequired(message="Image is required"),
#         FileAllowed(ALLOWED_EXTENSIONS,message="Image must be png or jpg")])

#     submit = SubmitField()

class TicketPurchaseForm(FlaskForm):
    ticket_quantity = IntegerField("Ticket Quantity",validators=[InputRequired()])

    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    comment = TextAreaField("Comment",validators=[InputRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search_string = StringField("Search Field", validators=[InputRequired()])
    submit = SubmitField("Submit")