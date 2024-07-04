from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['ADMIN_API_KEY'] = os.getenv('ADMIN_API_KEY')
mysql = MySQL(app)
app.mysql = mysql  # Make mysql accessible in app context
jwt = JWTManager(app)

from routes.user import user_bp
from routes.admin import admin_bp
from routes.booking import booking_bp
from routes.check import check_bp  
#registring blueprints

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(booking_bp, url_prefix='/booking')
app.register_blueprint(check_bp, url_prefix='/check')  
@app.route('/')
def index():
    return "Welcome to my Flask app!"

if __name__ == '__main__':
    app.run(debug=True)
