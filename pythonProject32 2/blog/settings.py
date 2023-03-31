import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



SECRET_KEY = os.urandom(36)
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')


class Config:
    FLASK_APP = 'app.py'
    FLASK_ENV = 'development'
    SECRET_KEY = 'anykey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_FILE_UPLOADER = 'upload'

    # configuration of mail
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'salomat423@gmail.com'
    MAIL_PASSWORD = '221502Ernur@'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    FLASK_ADMIN_SWATCH = 'flatly'  # lumen cyborg flatly