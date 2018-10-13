from flask import render_template, flash
from flask_login import login_user
from app import app

from app.models.tabels import User
from app.models.forms import LoginForm

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.data.password:
            login_user(user)
            flash("Login Valido!")
        else:
            flash("Login Invalido!")
    return render_template('login.html', form=form)


@app.route("/index")
def index():
    return render_template('index.html')