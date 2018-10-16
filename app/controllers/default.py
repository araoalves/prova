from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager

from app.models.tabels import User, Course, Student, Address
from app.models.forms import LoginForm, CreateCourse, CreateStudent

###################
#LOGIN
#carrega o usuario logado e retorna as informações dele
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Funcionalidade login que faz a validação de usuarios cadastrados no sistema e
    impede acesso de usuarios não autorizados.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user is not None) and (user.password == form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Usuário %s logado!' %user.username, 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha invalidos!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    '''
    Funcionalidade para deslogar o usuario do sistema
    '''
    logout_user()
    flash('Sessão encerrada.', 'info')
    return redirect("login")

#FIM LOGIN
##################

##################
#INDEX

@app.route("/index")
@login_required
def index():
    #retorna para a pagina principal do sistema
    return render_template('index.html')

#FIM INDEX
##################

##################
#CURSO
@app.route("/cursos", methods=["GET", "POST"])
@login_required
def course():
    '''
    funcionalidade para listar os cursos cadastrados no sistema e carregar o formulario de cadastro
    '''
    form = CreateCourse()
    if form.validate_on_submit():
        course = Course(codigo=form.codigo.data, 
            course=form.course.data, workload=form.workload.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('course'))
    courses = Course.query.order_by(Course.course).all()
    return render_template("course/course.html", courses=courses, form=form)


@app.route("/cursos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_course(id):
    '''
    Funcionalidade para editar o curso escolhido pegando pelo ID do curso
    '''
    form = CreateCourse()
    course = Course.query.filter_by(id=id).first_or_404()
    if request.method == "POST":
        course.codigo = form.codigo.data
        course.course = form.course.data
        course.workload = form.workload.data
        db.session.add(course)
        db.session.commit()
        flash('Curso editado com sucesso.', 'success')
        return redirect(url_for('course'))
    return render_template("course/edit.html", course=course, form=form)


@app.route("/cursos/excluir/<int:id>", methods=["GET", "DELETE"])
@login_required
def excluir_course(id):
    '''
    Funcionalidade para excluir o curso escolhido pegando o curso pelo ID
    '''
    course = Course.query.filter_by(id=id).first_or_404()
    if not course.student_course:
        db.session.delete(course)
        db.session.commit()
        flash('Curso excluído com sucesso.', 'success')
    else:
        flash('Impossível excluir, curso possui alunos relacionados.', 'warning')
    return redirect(url_for('course'))


@app.route("/pdf/<int:id>", methods=["GET"])
@login_required
def pdf(id):
    '''
    Funcionalidade para gerar o PDF com as informações dos cursos
    '''
    course = Course.query.filter_by(id=id).first_or_404()
    return render_template("course/pdf.html", course=course)

#FIM CURSO
##################

##################
#ALUNO
@app.route("/alunos", methods=["GET", "POST"])
@login_required
def student():
    '''
    Funcionalidade para listar todos os alunos cadastrados e
    carregar o formulario para cadastrar novos alunos no sistema.
    '''
    form = CreateStudent()
    form.course_id.choices = [(course.id, course.course) for course in Course.query.order_by(Course.course).all()]
    if request.method == "POST":
        course = Course.query.filter_by(id=form.course_id.data).first()
        student = Student(cpd=form.cpd.data, name=form.name.data, cpf=form.cpf.data, email=form.email.data, phone=form.phone.data, student_id=course)
        db.session.add(student)
        address = Address(cep=form.address.cep.data, state=form.address.state.data,
            city=form.address.city.data, street=form.address.street.data, bairro=form.address.bairro.data, address_id=student)
        db.session.add(address)
        db.session.commit()
        return redirect(url_for('student'))
    students = Student.query.order_by(Student.name).all()
    return render_template("student/student.html", students=students, form=form)


@app.route("/alunos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_student(id):
    '''
    Funcionalidade para editar o aluno escolhido pegando pelo ID do aluno
    '''
    form = CreateStudent()
    form.course_id.choices = [(course.id, course.course) for course in Course.query.order_by(Course.course).all()]
    student = Student.query.filter_by(id=id).first_or_404()
    if request.method == "POST":
        student.cpd = form.cpd.data
        student.name = form.name.data
        student.cpf = form.cpf.data
        student.email = form.email.data
        student.phone = form.phone.data
        # student.student_address[0].cep = form.cep
        # student.student_address[0].state = form.state.data
        # student.student_address[0].city = form.city.data
        # student.student_address[0].bairro = form.bairro.data
        # student.student_address[0].street = form.street.data
        print(student)
        # db.session.add(student)
        # db.session.commit()
        flash('Aluno editado com sucesso.', 'success')
        return redirect(url_for('student'))
    return render_template("student/edit.html", student=student, form=form)


@app.route("/alunos/excluir/<int:id>", methods=["GET", "DELETE"])
@login_required
def excluir_student(id):
    '''
    Funcionalidade para excluir o aluno escolhido pegando o aluno pelo ID
    '''
    student = Student.query.filter_by(id=id).first_or_404()
    address = Address.query.filter_by(id=student.student_address[0].id).first()
    db.session.delete(student)
    db.session.delete(address)
    db.session.commit()
    flash('Aluno excluído com sucesso.', 'success')
    return redirect(url_for('student'))


@app.route("/relatorio", methods=["GET", "POST"])
@login_required
def report():
    return render_template("report/report.html")