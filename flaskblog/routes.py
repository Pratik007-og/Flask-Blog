from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Successfully Logged In!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful Login! Please check Login details', 'danger')
    return render_template('login.html', title='Login', form=form)