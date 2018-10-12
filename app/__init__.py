from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#criando uma instancia do flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)

#importando do controllers o modulo default
from app.controllers import default