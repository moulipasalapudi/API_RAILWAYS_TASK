from flask import Blueprint, request, jsonify, current_app

admin_bp = Blueprint('admin', __name__)

# Decorator to check for administrative access
def admin_required(f):
    def wrap(*args, **kwargs):
        api_key = request.headers.get('API-KEY')  # Correctly accessing headers here
        if api_key and api_key == current_app.config['ADMIN_API_KEY']:
            return f(*args, **kwargs)
        return jsonify(message="Admin access required go back"), 403
    return wrap
#creating endpoint for adding train
@admin_bp.route('/add_train', methods=['POST'])
@admin_required
def add_train():
    data = request.get_json()
    train_name = data.get('train_name')
    source = data.get('source')
    destination = data.get('destination')
    total_seats = data.get('total_seats')

    mysql = current_app.mysql
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO trains (name, source, destination, total_seats, available_seats) VALUES (%s, %s, %s, %s, %s)",
                   (train_name, source, destination, total_seats, total_seats))  # Assuming available_seats initially same as total_seats
    mysql.connection.commit()
    cursor.close()

    return jsonify(message="Train added successfully"), 201
