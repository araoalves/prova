from flask_wtf import FlaskForm
from app import db
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, FormField
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

#Formulario de endereço
class AddressForm(FlaskForm):
    cep = StringField('cep', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    street = StringField('street', validators=[DataRequired()])
    bairro = StringField('bairro', validators=[DataRequired()])

#Formulario de telefone
class PhoneForm(FlaskForm):
    phone = StringField('phone', validators=[DataRequired()])

#Formulario de cadastro de alunos
class CreateStudent(FlaskForm):
    course_id = SelectField('courses', choices=[], validators=[DataRequired()])
    cpd = IntegerField('cpd', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    cpf = StringField('cpf', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    phone = StringField('phone')
    address = FormField(AddressForm)
