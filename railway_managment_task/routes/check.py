from flask import Blueprint, jsonify, current_app

check_bp = Blueprint('check', __name__)

@check_bp.route('/check_db', methods=['GET'])
def check_db():
    mysql = current_app.mysql
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        return jsonify(tables=tables), 200
    except Exception as e:
        return jsonify(message="Error connecting to the database", error=str(e)), 500
