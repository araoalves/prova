#Debug True faz o servidor reiniciar a cada alteração no código
DEBUG = True

#Caminho onde se encontra o BD e configurações do BD
SQLALCHEMY_DATABASE_URI = 'sqlite:///../storage.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

#Chave de segurança da aplicação
SECRET_KEY = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'