from flask import flash
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import form

from Flask_Web import get_data as gd

from Flask_Web.forms import LoginForm
from Flask_Web.forms import RegistrationForm
from Flask_Web.forms import UpdateAccountForm

from Flask_Web import db
from Flask_Web import app
from Flask_Web import bcrypt

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

import os
import secrets
import sqlite3

from PIL import Image
from Flask_Web.models import User, Post



posts = [
    {
        'author'      : 'Corey Schafer'      ,
        'title'       : 'Blog Post 1'        ,
        'content'     : 'First Post Content' ,
        'date_posted' : 'April 20, 2018' 
    }
    ,
    {
        'author'      : 'Jane Doe'            ,
        'title'       : 'Blog Post 2'         ,
        'content'     : 'Second Post Content' ,
        'date_posted' : 'April 21, 2018' 
    }
]


@app.route("/")
@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        languages = []

        with open('stock_number.csv', encoding="utf-8") as f: 
            slist = f.readlines() 
            for lst in slist: 
                s = lst.split(',') 
                
                # languages.append('{}'.format(s[0].strip()))
                # languages.append('{}'.format(str(s[1].strip())))
                languages.append('{} {}'.format(s[0].strip(),str(s[1].strip())))
                
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
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
            flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125,125)
    I = Image.open(form_picture)
    I.thumbnail(output_size)
    I.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been update!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/stock", methods=['GET', 'POST'])
def stock():
    if request.method == 'GET':
        conn = sqlite3.connect("stock.db")
        cursor = conn.cursor()
        sql="SELECT * FROM stock"
        cursor.execute(sql)
        content = cursor.fetchall()

        field_name = [i[0] for i in cursor.description]
        return render_template('stock.html', labels=field_name, content=content)
    
    return render_template('home.html')
