from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
#from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
import pyodbc
#from os import path

#db = SQLAlchemy()
#db = MySQL()
basedir = os.path.abspath(os.path.dirname(__file__))

#DB_NAME = "database.db"

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asodkfjqoei asopdijf asdofkj'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/itemreq'

    app.config['MYSQL_HOST']='localhost'
    app.config['MYSQL_USER']='root'
    #app.config['MYSQL_PASSWORD']='arnsbat'
    app.config['MYSQL_DB']='itemreq'


    #app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploads')
    #photos = UploadSet('photos', IMAGES)
    #configure_uploads(app, photos)
    #patch_request_class(app)

    #db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #from .models import Itemsetup, Usertable, Brand, Category

    #with app.app_context():
    #    db.create_all()

    return app

def connection():
    # s = '.\VIRUSATTACK' #Your server name 
    s = 'DESKTOP-9Q762EQ\SQLEXPRESS' #Your server name 
    d = 'ItemReq' 
    u = 'aaron_fulgar' #Your login
    # p = 'admin12345' #Your login password
    p = 'admin1' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn
