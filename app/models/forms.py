from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email

#Formulario de Login
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')

#Formulario de cadastro de cursos
class CreateCourse(FlaskForm):
    codigo = StringField('codigo', validators=[DataRequired()])
    course = StringField('course', validators=[DataRequired()])
    workload = IntegerField('workload', validators=[DataRequired()])

#Formulario de cadastro de alunos
class CreateStudent(FlaskForm):
    cpd = IntegerField('cpd', validators=[DataRequired()])
    nome = StringField('nome', validators=[DataRequired()])
    cpf = StringField('cpf', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])