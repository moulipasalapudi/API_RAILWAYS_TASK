from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    mysql = current_app.mysql

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, 'user'))
        mysql.connection.commit()
        return jsonify(message='User successfully created'), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify(message='User registration failed', error=str(e)), 400
    finally:
        cursor.close()

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    mysql = current_app.mysql
    
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[2], password):  # Assuming password is in the third column
        access_token = create_access_token(identity={'username': user[1], 'role': user[3]})  # Assuming username is in the second column and role in the fourth column
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401
    
