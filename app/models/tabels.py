from app import db
from datetime import datetime

#Classes dos modelos das tabelas
class Course(db.Model):
    __tablename__ = "cursos" #muda o nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    workload = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    #retorna nomes dos cursos nas consultas ao BD
    def __repr__(self):
        return "<Course %r>" %self.name

#Classe do modela da tabela de alunos
class Student(db.Model):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    #relaciona com a tabela de cursos
    course = db.relationship('Course', foreign_keys=course_id)

    #retorna o nome dos estudantes nas consultas ao BD
    def __repr__(self):
        return "<Student %r>" %self.name

#Classe de modelo de tabela do Endereço
class Address(db.Model):
    __tablename__ = "endereco"
    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('alunos.id'))
    #relaciona a classe Address ao id do aluno
    student = db.relationship('Student', foreign_keys=student_id)

    #retorna a lista dos id de endereços
    def __repr__(self):
        return "<Address %r>" %self.id

#Classe do modela da tabela de telefone
class Phone(db.Model):
    __tablename__ = "telefone"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('alunos.id'))
    #relaciona a classe Phone ao id do aluno
    student = db.relationship('Student', foreign_keys=student_id)

    #retorna a lista de telefones
    def __repr__(self):
        return "<Phone %r>" %self.phone