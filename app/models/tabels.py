from app import db
from datetime import datetime

#Classes dos modelos das tabelas
class Course(db.Model):
    __tablename__ = "cursos" #muda o nome da tabela

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullabel=False)
    workload = db.Column(db.Integer, nullabel=False)
    create = db.Column(db.DateTime, nullabel=False, default=datetime.utcnow)

    # def __init__(self, name, workload):
    #     self.name = name
    #     self.workload = workload

    def __repr__(self):
        return "<Course %r>" %self.name

class Student(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullabel=False)
    cpf = db.Column(db.Integer, unique=True, nullabel=False)
    phone = db.Column(db.Integer, nullabel=False)
    email = db.Column(db.String(100), unique=True, nullabel=False)

    # def __init__(self, name, cpf, phone, email):
    #     self.name = name
    #     self.cpf = cpf
    #     self.phone = phone
    #     self.email = email

    def __repr__(self):
        return "<Student %r>" %self.name