from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager

from app.models.tabels import User, Course, Student, Address, Phone
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
    return render_template("course.html", courses=courses, form=form)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_course(id):
    '''
    Funcionalidade para editar o curso escolhido pegando pelo ID
    '''
    pass


@app.route("/excluir/<int:id>", methods=["GET", "DELETE"])
@login_required
def excluir_course(id):
    '''
    Funcionalidade para excluir o curso escolhido pegando o curso pelo ID
    '''
    course = Course.query.filter_by(id=id).first_or_404()
    db.session.delete(course)
    db.session.commit()
    flash('Curso excluído com sucesso.', 'success')
    return redirect(url_for('course'))

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
    print("1")
    if request.method == "POST":
        print("2")
        course_id = Course.query.filter_by(id=form.course_id.data).first()
        student = Student(course_id=form.course_id.data, cpd=form.cpd.data, name=form.name.data, cpf=form.cpf.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        phone = Phone(phone=form.phone.phone.data, student_id=student.id)
        address = Address(student_id=student.id, cep=form.address.cep.data, state=form.address.state.data,
            city=form.address.city.data, street=form.address.street.data, bairro=form.address.bairro.data)
        db.session.add(phone)
        db.session.add(address)
        db.session.commit()
    students = Student.query.order_by(Student.name).all()
    return render_template("student.html", students=students, form=form)


# @app.route("/editar/<int:id>", methods=["GET", "POST"])
# @login_required
# def editar(id):
#     pass

# @app.route("/excluir/<int:id>", methods=["GET", "DELETE"])
# @login_required
# def excluir_course(id):
#     '''
#     Funcionalidade para excluir o curso escolhido pegando o curso pelo ID
#     '''
#     course = Course.query.filter_by(id=id).first()
#     db.session.delete(course)
#     db.session.commit()
#     flash('Curso excluído com sucesso.', 'success')
#     return redirect(url_for('course'))