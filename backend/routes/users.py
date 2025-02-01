from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)  # Use get_or_404 for consistency

    user_data = format_user_data(user) # Use helper function

    return jsonify(user_data), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id) # Use get_or_404 for consistency
    user_data = format_user_data(user) # Use helper function
    return jsonify(user_data), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    data = request.get_json()

    # Update only the fields that are present in the request
    if 'bio' in data:
        user.bio = data['bio']
    if 'contact_info' in data:
        user.contact_info = data['contact_info']
    if 'profile_picture' in data:
        # Handle profile picture update (see explanation below)
        user.profile_picture = data['profile_picture']  # Or process the uploaded file
    # ... update other fields as needed (following the same pattern)

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating profile', 'error': str(e)}), 500

def format_user_data(user): # Helper function to format user data
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'user_type': user.user_type,
        'bio': user.bio,
        'contact_info': user.contact_info,
        'profile_picture': user.profile_picture,
        'registration_date': user.registration_date.isoformat() if user.registration_date else None,
    }