from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
with app.app_context():
    db.create_all()
posts = [
    {
        'author': 'Pratik Patnaik',
        'title': 'Blog Post 1',
        'content': 'First Blog Post Ever!',
        'date_posted': 'June 17th, 2024'
    },
    {
        'author': 'Aryaman Das',
        'title': 'Blog Post 2',
        'content': 'Second Blog Post',
        'date_posted': 'June 18th, 2024'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About Page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed_pswd
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now Login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful Login! Please check Login details', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET'])
@login_required
def account():
    return render_template('account.html', title='Account')