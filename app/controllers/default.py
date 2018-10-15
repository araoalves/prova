from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager

from app.models.tabels import User, Course, Student, Address, Phone
from app.models.forms import LoginForm, CreateCourse, CreateStudent

#carrega o usuario logado e retorna as informações dele
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user is not None) and (user.password_hash == form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Usuário %s logado!' %user.username, 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha invalidos!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Sessão encerrada.', 'info')
    return redirect("login")


@app.route("/index")
@login_required
def index():
    return render_template('index.html')


@app.route("/cursos", methods=["GET", "POST"])
@login_required
def course():
    form = CreateCourse()
    if form.validate_on_submit():
        course = Course(codigo=form.codigo.data, 
            course=form.course.data, workload=form.workload.data)
        db.session.add(course)
        db.session.commit()
    courses = Course.query.order_by(Course.course).all()
    return render_template("course.html", courses=courses,form=form)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    pass


@app.route("/excluir/<int:id>")
@login_required
def excluir(id):
    course = Course.query.filter_by(id=id).first()
    db.session.delete(course)
    db.session.commit()
    flash('Curso excluído com sucesso.', 'success')
    return redirect(url_for('course'))


@app.route("/alunos", methods=["GET", "POST"])
@login_required
def student():
    form = CreateStudent()
    form.course_id.choices = [(course.id, course.course) for course in Course.query.order_by(Course.course).all()]
    if form.validate_on_submit():
        student = Student(course_id=form.course_id.data, cpd=form.cpd.data, name=form.name.data, cpf=form.cpf.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        phone = Phone(phone=form.phone.phone.data, student_id=student.id)
        address = Address(student_id=student.id, cep=form.address.cep.data, state=form.address.state.data,
            city=form.address.city.data, street=form.address.street.data, bairro=form.address.bairro.data)
        db.session.add(phone)
        db.session.add(address)
        db.session.commit()
    return render_template("student.html", form=form)