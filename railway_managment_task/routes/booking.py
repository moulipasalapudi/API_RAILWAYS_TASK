from flask import Blueprint,request,jsonify,current_app
#importing functions that supports authentication 
from flask_jwt_extended import jwt_required,get_jwt_identity

booking_bp=Blueprint('booking',__name__)
# creating an endpoint for checking availability
@booking_bp.route('/check_availability',methods=['POST'])
def check_availability():
    data =request.get_json()
    source=data.get('source')
    destination=data.get('destination')
    mysql=current_app.mysql
    cursor= mysql.connection.cursor()
    cursor.execute("SELECT * FROM trains WHERE source=%s AND destination =%s",(source,destination))
    trains=cursor.fetchall()
    cursor.close()
    return jsonify(trains=trains),200
# creating  an endpoint for booking seat
@booking_bp.route('/book_seat',methods=["POST"])
@jwt_required()
def book_seat():
    current_user=get_jwt_identity()
    data=request.get_json()
    train_id=data.get('train_id')
    mysql=current_app.mysql
    cursor = mysql.connection.cursor()
    #Blocks to handle race condition and proper booking
    try:
        cursor.execute("SELECT total_seats, booked_seats FROM trains WHERE id = %s FOR UPDATE", (train_id,))
        train = cursor.fetchone()

        if not train:
            return jsonify(message="Train Unavailable"), 404

        if train['booked_seats'] < train['total_seats']:
            cursor.execute("UPDATE trains SET booked_seats = booked_seats + 1 WHERE id = %s", (train_id,))
            cursor.execute("INSERT INTO bookings (user_id, train_id) VALUES (%s, %s)", (current_user['username'], train_id))
            mysql.connection.commit()
            return jsonify(message="Seat Booking Successful"), 200
        else:
            return jsonify(message="No available seats"), 400
    # Handles case when some issue occurs it rollbacks
    except Exception as e:
        mysql.connection.rollback()
        return jsonify(message="Error occurred while processing your request"), 500
    finally:
        cursor.close()
@booking_bp.route('/booking_details',methods=['GET'])
@jwt_required()
def booking_details():
    current_user=get_jwt_identity()
    booking_id=request.args.get('booking_id')
    mysql=current_app.mysql
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM bookings WHERE id = %s AND user_id = %s", (booking_id, current_user['username']))
    booking = cursor.fetchone()
    cursor.close()

    if booking:
        return jsonify(booking=booking), 200
    else:
        return jsonify(message="Booking not found"), 404