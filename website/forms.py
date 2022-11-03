
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
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

ALLOWED_EXTENSIONS = ['png','jpg']

GENRES = [
        ('Alternative','Alternative'),
        ('Pop','Pop'),
        ('Indie','Indie'),
        ('Rock','Rock'),
        ('Soul','Soul')
        ]
# Create new Concert Events
class ConcertForm(FlaskForm):
    event_name = StringField("Concert Name",validators=[InputRequired()])
    event_description = TextAreaField("Event Description",validators=[InputRequired()])
    event_date = DateField("Event Date",validators=[InputRequired()])

    #genre = StringField("Genre",validators=[InputRequired()])
    genre = SelectField("Genre",validators=[InputRequired()],choices=[(genre[0],genre[1]) for genre in GENRES])
    #genre.choices = [for genre in GENRES]

    venue = StringField("Venue Location",validators=[InputRequired()])
    ticket_count = IntegerField("Ticket Count",validators=[InputRequired()])
    ticket_price = StringField("Ticket Price",validators=[InputRequired()])
    event_image = FileField("Event Image",validators=[
        FileRequired(message="Image is required"),
        FileAllowed(ALLOWED_EXTENSIONS,message="Image must be png or jpg")])

    submit = SubmitField("Submit")

class TicketPurchaseForm(FlaskForm):
    ticket_quantity = IntegerField("Ticket Quantity",validators=[InputRequired()])

    submit = SubmitField("Submit")
