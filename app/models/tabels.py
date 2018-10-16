from app import db
from datetime import datetime

#Classe do modelo da tabela de cursos
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(6), unique=True, nullable=False)
    course = db.Column(db.String(80), nullable=False)
    workload = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())

    #relaciona com a tabela de alunos
    student_course = db.relationship('Student', backref='student_id')

    #retorna nomes dos cursos nas consultas ao BD
    def __repr__(self):
        return "<Course %r>" %self.course

#Classe do modela da tabela de alunos
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpd = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    #relaciona a classe de alunos com a de endereço
    student_address = db.relationship('Address', backref='address_id')

    #retorna o nome dos estudantes nas consultas ao BD
    def __repr__(self):
        return "<Student %r>" %self.name

#Classe de modelo de tabela do Endereço
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(8), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    #retorna a lista dos id de endereços
    def __repr__(self):
        return "<Address %r>" %self.id

#Classe do Modelo de usuario do sistema
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

    #propriedades para que a validação de login funcione corretamente
    '''
    verifica se usuario está autenticado
    '''
    @property
    def is_authenticated(self):
        return True

    '''
    verifica se o usuario está ativo no sistema
    '''
    @property
    def is_active(self):
        return True

    '''
    verifica se o usuario esta como anônimo no sietma ou logado com usuario
    '''
    @property
    def is_anonymous(self):
        return False

    '''
    pega o ID do usuario com a sessão ativa
    '''
    def get_id(self):
        return str(self.id)
