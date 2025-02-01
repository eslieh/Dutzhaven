from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Message, User, db

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/send/<int:receiver_id>', methods=['POST'])
@jwt_required()
def send_message(receiver_id):
    sender_id = get_jwt_identity()
    receiver = User.query.get_or_404(receiver_id)

    data = request.get_json()
    message_text = data.get('message_text')

    if not message_text:
        return jsonify({'message': 'Message text is required'}), 400

    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message_text=message_text)
    try:
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error sending message', 'error': str(e)}), 500

@messages_bp.route('/', methods=['GET'])  # Get all messages for the logged-in user
@jwt_required()
def get_messages():
    user_id = get_jwt_identity()
    messages = Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).order_by(Message.timestamp).all()
    message_list = []
    for message in messages:
        message_data = {
            'id': message.id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'message_text': message.message_text,
            'timestamp': message.timestamp.isoformat() if message.timestamp else None,
        }
        message_list.append(message_data)
    return jsonify(message_list), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    user_id = get_jwt_identity()
    if message.sender_id != user_id:
        return jsonify({'message': 'You are not authorized to delete this message'}), 403

    try:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting message', 'error': str(e)}), 500