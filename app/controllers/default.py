from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db, login_manager

from app.models.tabels import User
from app.models.forms import LoginForm

#carrega o usuario logado e retorna as informações dele
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is not None:
            login_user(user)
            flash("Login Valido!")
            return redirect(url_for('index'))
        else:
            flash("Login Invalido!")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Sessão encerrada.")
    return redirect("login")


@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/cursos")
def course():
    return render_template("course.html")


@app.route("/alunos")
def student():
    return render_template("student.html")