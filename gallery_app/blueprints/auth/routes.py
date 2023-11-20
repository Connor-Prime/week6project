from flask import Blueprint, render_template, request, redirect, flash
from flask_jwt_extended import current_user
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

# internal imports
from gallery_app.models import User, db, Album
from gallery_app.forms import RegisterForm, LoginForm
from sqlalchemy import select


auth = Blueprint('auth',__name__, template_folder='auth_templates')

# Creates sign up page
@auth.route('/signup', methods=['GET','POST'])
def signup():
    
    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        username = registerform.username.data
        email = registerform.username.data
        password=registerform.password.data

        print(email, password, username)

        if User.query.filter(username==username).first():
            flash("Username already exists. Please try again.", category='warning')
            return redirect('/signup')
        if User.query.filter(email==email).first():
            flash("That email has already been registered. Please try again.", category='warning')
            return redirect('/signup')
    
        user = User(username, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f"You have successfully registered user {username}", category='success')
        return redirect('/signin')

    # if request is not post

    return render_template('signup.html', form=registerform)
    
    # creates sign in page
@auth.route('/signin', methods=['GET', 'POST'])

def signin():
    login_form = LoginForm()

    if request.method=='POST' and login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        print("Login Info:",email, password)

        user = User.query.filter(email==email).first()

        if user and check_password_hash(user.password , password):

            login_user(user)

            flash(f"Successfully logged in {email}. Welcome to your homepage {user.username}.", category='success')
            return redirect('/')
        
        else:
            flash("Invalid Email or Password, Please Try Again", category='warning')
            return redirect('/signin')
        


    return render_template('signin.html', form=login_form )

@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')