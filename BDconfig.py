from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Manual para configuração de BD https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# SQLALCHEMY_DATABASE_URI The database URI that should be used for the connection. Examples:
# mysql://username:password@server/db
# sqlite:////tmp/test.db

# criar uma instancia flask com o nome app
app = Flask(__name__)
#the line app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IndustriaFeliz.db' in Python typically sets up the database URI (Uniform Resource Identifier) for a Flask application that uses SQLAlchemy, a popular ORM (Object-Relational Mapping) library. Here's what each part of it means:
#app.config: This refers to the configuration object of a Flask application. It's where you can store various configuration settings for your Flask app.
#['SQLALCHEMY_DATABASE_URI']: This specifies a configuration key within the app.config dictionary. SQLAlchemy uses this key to know where the database is located.
# "= 'sqlite:///IndustriaFeliz.db':" This assigns a value to the SQLALCHEMY_DATABASE_URI configuration key. In this case, it's setting the URI for the SQLite database named IndustriaFeliz.db.

# "sqlite:///:" a base de dados será SQLite,  as três (///) determinam um caminho de arquivo "Relativo".
# "IndustriaFeliz.db:" - Nome da Base de Dados SQLite.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IndustriaFeliz.db'
db = SQLAlchemy(app)

# ==== Cadastros Gerais ====

# Cadastros Gerais - Unidades Federativas

#DB_COUNTRY = Tabela de dados contendo o nome dos países
class DB_COUNTRY(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


#DB_ESTATE = Tabela de dados contendo o nome dos estados
#link com: BD_COUNTRY
class DB_ESTATE(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_BD_COUNTRY = db.Column(db.Integer, nullable=False)
    NAME = db.Column(db.String(200), nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


#DB_CITY = Tabela de dados contendo o nome das cidades e código do estado 
#link com: BD_ESTATE
class DB_CITY(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_BD_ESTATE = db.Column(db.Integer, nullable=False)
    NAME = db.Column(db.String(200), nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Cadastros Gerais - Unidades de Medidas

#DB_MEASURES = Tabela de dados contendo as medidas e suas abreviações 
class DB_MEASURES(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    ABREVIATION = db.Column(db.String(10), nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Cadastros Gerais - Grupos

#DB_GROUP = Tabela de dados contendo os grupos de produtos
class DB_GROUP(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Cadastros Gerais - Tipos de Produtos

#DB_PRODUCT_TYPE = Tabela de dados contendo os grupos de produtos 
class DB_PRODUCT_TYPE(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    ABREVIATION = db.Column(db.String(10), nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# ==== Cadastros de Entidades ====

# Cadastros de Entidades - Encargos

#DB_JOB = Tabela de dados contento as funções e seus respectivos salarios
class DB_JOB(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    RENT = db.Column(db.Float, nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Cadastros de Entidades - Colaboradores

#DB_WORKERS = Tabela de dados contendo os colaboradores
class DB_WORKERS(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    ID_BD_JOB = db.Column(db.Integer, nullable=False)
    ID_BD_COUNTRY = db.Column(db.Integer, nullable=False)
    ID_BD_ESTATE = db.Column(db.Integer, nullable=False)
    ID_BD_CITY = db.Column(db.Integer, nullable=False)
    DISTRICT = db.Column(db.String(200), nullable=False)
    ROAD = db.Column(db.String(200), nullable=False)
    NUMBER = db.Column(db.Integer, nullable=False)
    COMPLEMENT = db.Column(db.String(200), nullable=False)
    CEP = db.Column(db.String(9), nullable=False)
    BORN_DATE = db.Column(db.Date, nullable=False)
    ADMISSION_DATE = db.Column(db.Date, nullable=False)
    EMAIL = db.Column(db.String(200), nullable=True)
    PHONE = db.Column(db.String(200), nullable=True)
    CPF = db.Column(db.String(14), nullable=False)
    RG = db.Column(db.String(20), nullable=True)
    PIS = db.Column(db.String(14), nullable=False)
    ACTIVE = db.Column(db.Integer, nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Cadastros de Entidades - Fornecedores

#DB_SUPPLIER = Tabela de dados contendo os fornecedores
class DB_SUPPLIER(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    ID_BD_COUNTRY = db.Column(db.Integer, nullable=False)
    ID_BD_ESTATE = db.Column(db.Integer, nullable=False)
    ID_BD_CITY = db.Column(db.Integer, nullable=False)
    DISTRICT = db.Column(db.String(200), nullable=False)
    ROAD = db.Column(db.String(200), nullable=False)
    NUMBER = db.Column(db.Integer, nullable=False)
    COMPLEMENT = db.Column(db.String(200), nullable=False)
    CEP = db.Column(db.String(9), nullable=False)
    EMAIL = db.Column(db.String(200), nullable=True)
    PHONE = db.Column(db.String(200), nullable=True)
    CNPJ = db.Column(db.String(18), nullable=False)
    ACTIVE = db.Column(db.Integer, nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# ==== Cadastros de Materiais ====

# Cadastros de Materiais - Matéria Prima

#DB_MP = Tabela de dados contendo o registro das matérias primas
class DB_MP(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    ID_BD_MEASURES = db.Column(db.Integer, nullable=False)
    IPI = db.Column(db.Float, default=0.0)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Cadastros de Materiais - Material de Consumo

#DB_MC = Tabela de dados contendo o registro dos materiais de consumo
class DB_MC(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(200), nullable=False)
    ID_BD_MEASURES = db.Column(db.Integer, nullable=False)
    IPI = db.Column(db.Float, default=0.0)
    DIFAL = db.Column(db.Float, default=0.0)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Cadastros de Materiais - Produtos

#DB_PROD = Tabela de dados contendo os produtos
class DB_PROD(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    COD = db.Column(db.String(20), nullable=True)    
    NAME = db.Column(db.String(200), nullable=False)
    ID_BD_GROUP = db.Column(db.Integer, nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


#DB_PROD_MO = Tabela de dados contendo os produtos
class DB_PROD_MO(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_BD_PROD = db.Column(db.Integer, nullable=False)
    NAME = db.Column(db.String(200), nullable=False)
    WORKERS_QUANTITY = db.Column(db.Integer, nullable=False)
    LOT_AMMOUNT = db.Column(db.Integer, nullable=False)
    TIME_TO_PRODUCE = db.Column(db.Integer, nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


#DB_PROD_MP = Tabela de dados da Matéria Prima por produto
class DB_PROD_MP(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_BD_PROD = db.Column(db.Integer, nullable=False)
    ID_BD_MP = db.Column(db.Integer, nullable=False)
    QUANTITY = db.Column(db.Float, nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


#DB_PROD_MC = Tabela de dados dos Materiais de Consumo por produto
class DB_PROD_MC(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_BD_PROD = db.Column(db.Integer, nullable=False)
    ID_BD_MC = db.Column(db.Integer, nullable=False)
    QUANTITY = db.Column(db.Float, nullable=False)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# ==== Movimentações ====

# Movimentações - Compras
#DB_PURCHASES = Tabela de dados das compras realizadas
class DB_PURCHASES(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_BD_PRODUCT_TYPE = db.Column(db.Integer, nullable=False)
    ID_BD_PROD = db.Column(db.Integer, nullable=False)
    ID_BD_SUPPLIER = db.Column(db.Integer, nullable=False)
    NF_DATA = db.Column(db.Date, nullable=False)
    NF_NUMBER = db.Column(db.String(11), nullable=False)
    PRICE = db.Column(db.Float, nullable=False)
    QUANTITY = db.Column(db.Float, nullable=False)
    TRANSPORT_COST = db.Column(db.Float, default=0)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



# === fim das criações de tabelas da Base de dados ===

# Create database tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
