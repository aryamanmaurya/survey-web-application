from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import User
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required

app = Blueprint('main', __name__)

@app.route('/')
def landing():
    return render_template('index.html')


from flask import render_template, request, flash, redirect, url_for
from app.models import User
from werkzeug.security import generate_password_hash
from app import db

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if a user with the same username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('User with this username or email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main.register'))
        
        # Proceed with user creation if no duplicate is found
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.landing'))

