from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required, logout_user, current_user
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)


# this is the hint for a login function
next_page = ""
@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    global next_page
    if request.method == "GET":
        next_page = request.args.get("next")
    print('In Login View function')
    login_form = LoginForm()
    error=None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        stored_user = User.query.filter_by(username=user_name).first()
        if not stored_user or not check_password_hash(stored_user.password_hash, password): # takes the hash and password
            error='Invalid Username/Password'
        if not error:
            login_user(stored_user)
            # next_page = request.args.get('next') #this gives the url from where the login page was accessed
            # print(next_page)
            if not next_page or next_page == "/login":
                next_page = "/"
            # print(f"Username: {current_user.username} logged in")
            if not next_page or not next_page.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(next_page)
        else:
            flash(error)
    # return render_template('user.html', form=login_form, heading='Login')
    return render_template('login.html', form=login_form, heading='Login')

@bp.route('/register',methods=['GET','POST'])
def register():
    register_form = RegisterForm()
    error = None
    print("Register form")
    if request.method == "POST":
        if register_form.validate_on_submit():
            print("VALIDATED")

        user_name = register_form.user_name.data
        email = register_form.email_id.data
        password = register_form.password.data
        contact_number = register_form.contact_number.data
        user_exists = User.query.filter_by(username=user_name).first()
        if user_exists:
            error="User already exists"
            flash(error)
            return redirect(url_for('auth.register',error=error))

        password_hash = generate_password_hash(password)

        new_user = User(username=user_name,password_hash=password_hash,email=email,contact_number=contact_number)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully","success")
        print(f"User {user_name} created sucessfully.")
        login_user(new_user)

        return redirect(url_for('main.index'))

    # return render_template('user.html',form=register_form,heading='Register')
    return render_template('signup.html',form=register_form,heading='Register')

@bp.route('/logout',methods=['GET'])
# @login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))