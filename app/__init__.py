from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

#criando uma instancia do flask
app = Flask(__name__)
app.config.from_object('config')

#Instancia do gerenciador de BD para migrações
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#intancia do BD para comandos script
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#intsncia do gerenciador de Login
login_manager = LoginManager()
login_manager.init_app(app)

#importando dos meus modulos models e controllers
from app.models import tabels
from app.controllers import default