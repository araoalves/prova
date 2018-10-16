from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
import xlsxwriter

from app.models.tabels import User, Course, Student, Address
from app.models.forms import LoginForm, CreateCourse, CreateStudent, AddressForm

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
    if request.method == "POST" and form.validate():
        course = Course(codigo=form.codigo.data, 
            course=form.course.data, workload=form.workload.data)
        db.session.add(course)
        db.session.commit()
        flash('Curso cadastrado com sucesso.', 'success')
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
    if request.method == "POST" and form.validate():
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


@app.route("/pdf", methods=["GET"])
@login_required
def pdf():
    '''
    Funcionalidade para gerar o PDF com as informações dos cursos
    '''
    courses = Course.query.order_by(Course.course).all()
    return render_template("course/pdf.html", courses=courses)
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
    if request.method == "POST" and form.validate():
        course = Course.query.filter_by(id=form.course_id.data).first()
        student = Student(cpd=form.cpd.data, name=form.name.data, cpf=form.cpf.data, email=form.email.data, phone=form.phone.data, student_id=course)
        db.session.add(student)
        address = Address(cep=form.address.cep.data, state=form.address.state.data,
            city=form.address.city.data, street=form.address.street.data, bairro=form.address.bairro.data, address_id=student)
        db.session.add(address)
        db.session.commit()
        flash('Aluno cadastrado com sucesso.', 'success')
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
    form2 = AddressForm()
    form.course_id.choices = [(course.id, course.course) for course in Course.query.order_by(Course.course).all()]
    student = Student.query.filter_by(id=id).first_or_404()
    if request.method == "POST":
        student.cpd = form.cpd.data
        student.name = form.name.data
        student.cpf = form.cpf.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.student_address[0].cep = form2.cep.data
        student.student_address[0].state = form2.state.data
        student.student_address[0].city = form2.city.data
        student.student_address[0].bairro = form2.bairro.data
        student.student_address[0].street = form2.street.data
        db.session.add(student)
        db.session.commit()
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

#################
#RELATÓRIO
@app.route("/relatorio", methods=["GET"])
@login_required
def report():
    '''
    Funcionalidade para listar os cursos e os seus respectivos alunos
    '''
    courses = Course.query.order_by(Course.course).all()
    total_course = len(courses)
    return render_template("report/report.html", courses=courses, total_course=total_course)


@app.route("/relatorio/pdf", methods=["GET"])
@login_required
def report_pdf():
    '''
    Funcionalidade para gerar PDF do relatório
    '''
    courses = Course.query.order_by(Course.course).all()
    total_course = len(courses)
    return render_template("report/pdf.html", courses=courses, total_course=total_course)


@app.route("/report/excel")
@login_required
def report_excel():
    '''
    Funcionalidade para gerar arquivo excel do relatório
    '''
    # cria o arquivo em excel
    workbook = xlsxwriter.Workbook('RelatorioCursos.xlsx')
    worksheet = workbook.add_worksheet()

    #Adicione um formato em negrito para usar no cabeçalho.
    bold = workbook.add_format({'bold': True})
    #Cabeçalho da tabela
    worksheet.write('A1', 'Curso', bold)
    worksheet.write('B1', 'Aluno', bold)
    worksheet.write('C1', 'CPD', bold)
    worksheet.write('D1', 'CPF', bold)
    worksheet.write('E1', 'Telefone', bold)
    worksheet.write('F1', 'E-mail', bold)
    worksheet.write('G1', 'Estado', bold)
    worksheet.write('H1', 'Cidade', bold)
    worksheet.write('I1', 'Data de Cadastro', bold)

    #Dados que serão escritos na planilha
    courses = Course.query.order_by(Course.course).all()
    total_course = len(courses)

    # percorre as celulas e inseri os dados
    row = 1
    for x in range(total_course):
        students = len(courses[x].student_course)
        for y in range(students):
            col = 0
            worksheet.write(row, col, courses[x].course)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].name)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].cpd)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].cpf)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].phone)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].email)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].student_address[0].state)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].student_address[0].city)
            col+=1
            worksheet.write(row, col, courses[x].student_course[y].created)
        
            row += 1

    workbook.close()
    flash('Arquivo Excel gerado com sucesso.', 'success')
    return redirect(url_for('report'))