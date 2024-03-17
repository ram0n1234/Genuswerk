import os

# Zugriff auf OS-Variablen von Azure App Service
# Quelle: https://learn.microsoft.com/en-us/azure/app-service/configure-language-python
sql_user = os.environ['sql_user']
sql_pass = os.environ['sql_pass']
sql_host = os.environ['sql_host']

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vNn^D=k8slkjef-f9vjv97r3jfs@#°n'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{sql_user}:{sql_pass}@{sql_host}:3306/genusswerk"
    SQLALCHEMY_TRACK_MODIFICATIONS = False