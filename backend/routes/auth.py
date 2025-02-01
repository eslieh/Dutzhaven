from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not all([username, email, password, user_type]):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, email=email, password_hash=hashed_password, user_type=user_type)

    try:
        db.session.add(new_user)
        db.session.commit()

        # Return the newly created user data (optional but good practice)
        user_data = {
            'id': new_user.id,  # Or new_user.user_id if you have that
            'username': new_user.username,
            'email': new_user.email,
            'user_type': new_user.user_type
        }
        return jsonify({'message': 'User registered successfully', 'user': user_data}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error registering user', 'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)  # Or user.user_id
        # Include user details in the response (recommended)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type
        }
        return jsonify({'access_token': access_token, 'user': user_data}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@auth_bp.route('/check', methods=['GET'])
@jwt_required()
def check_token():
    current_user_id = get_jwt_identity()  # Get the user's ID from the token
    user = User.query.get(current_user_id) # Fetch user details from the database
    if user:
       user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type
        }
       return jsonify({'message': 'Token is valid', 'user': user_data}), 200
    return jsonify({'message': 'User not found'}), 404  # Or handle as needed

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a real application, consider adding the token to a blacklist for immediate invalidation.
    return jsonify({'message': 'Logged out successfully'}), 200  # Frontend should clear the token