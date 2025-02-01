from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'user_type': user.user_type,
        'bio': user.bio,
        'contact_info': user.contact_info,
        'profile_picture': user.profile_picture,
        'registration_date': user.registration_date.isoformat() if user.registration_date else None,
    }

    return jsonify(user_data), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):  # Get a specific user's profile (publicly viewable)
    user = User.query.get_or_404(user_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'user_type': user.user_type,
        'bio': user.bio,
        'contact_info': user.contact_info,
        'profile_picture': user.profile_picture,
        'registration_date': user.registration_date.isoformat() if user.registration_date else None,
    }
    return jsonify(user_data), 200

@users_bp.route('/profile', methods=['PUT'])  # Update current user's profile
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    data = request.get_json()

    user.bio = data.get('bio', user.bio)
    user.contact_info = data.get('contact_info', user.contact_info)
    # ... update other fields as needed

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating profile', 'error': str(e)}), 500