from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Bid, Task, db

bids_bp = Blueprint('bids', __name__, url_prefix='/bids')

@bids_bp.route('/create/<int:task_id>', methods=['POST'])
@jwt_required()
def create_bid(task_id):
    freelancer_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)  # Check if task exists

    data = request.get_json()
    proposal_text = data.get('proposal_text')
    price = data.get('price')

    if not all([proposal_text, price]):
        return jsonify({'message': 'Missing required fields'}), 400

    if not isinstance(price, (int, float)): # Price should be a number
        return jsonify({'message': 'Price must be a number'}), 400

    existing_bid = Bid.query.filter_by(task_id=task_id, freelancer_id=freelancer_id).first()
    if existing_bid:
        return jsonify({'message': 'You have already submitted a bid for this task'}), 400

    new_bid = Bid(task_id=task_id, freelancer_id=freelancer_id, proposal_text=proposal_text, price=price)
    try:
        db.session.add(new_bid)
        db.session.commit()
        return jsonify({'message': 'Bid submitted successfully', 'bid_id': new_bid.id}), 201  # Return bid ID
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error submitting bid', 'error': str(e)}), 500

@bids_bp.route('/task/<int:task_id>', methods=['GET'])
def get_bids_for_task(task_id):
    bids = Bid.query.filter_by(task_id=task_id).all()
    bid_list = []
    for bid in bids:
        bid_data = {
            'id': bid.id,
            'task_id': bid.task_id,
            'freelancer_id': bid.freelancer_id,
            'proposal_text': bid.proposal_text,
            'price': bid.price,
            'submitted_at': bid.submitted_at.isoformat() if bid.submitted_at else None,
            'freelancer': {  # Include freelancer details (if available)
                'id': bid.freelancer.id, # Assuming you have a relationship with the User model
                'username': bid.freelancer.username,
                # ... other freelancer details
            } if bid.freelancer else None,
        }
        bid_list.append(bid_data)
    return jsonify(bid_list), 200

@bids_bp.route('/<int:bid_id>', methods=['PUT'])
@jwt_required()
def update_bid(bid_id):
    bid = Bid.query.get_or_404(bid_id)
    freelancer_id = get_jwt_identity()
    if bid.freelancer_id != freelancer_id:
        return jsonify({'message': 'You are not authorized to update this bid'}), 403

    data = request.get_json()
    proposal_text = data.get('proposal_text')
    price = data.get('price')

    if proposal_text is None and price is None: # Check if any fields are being updated
        return jsonify({'message': 'No fields to update'}), 400

    if proposal_text is not None:
        bid.proposal_text = proposal_text
    if price is not None:
        bid.price = price


    try:
        db.session.commit()
        return jsonify({'message': 'Bid updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating bid', 'error': str(e)}), 500

@bids_bp.route('/<int:bid_id>', methods=['DELETE'])
@jwt_required()
def delete_bid(bid_id):
    bid = Bid.query.get_or_404(bid_id)
    freelancer_id = get_jwt_identity()
    if bid.freelancer_id != freelancer_id:
        return jsonify({'message': 'You are not authorized to delete this bid'}), 403
    try:
        db.session.delete(bid)
        db.session.commit()
        return jsonify({'message': 'Bid deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting bid', 'error': str(e)}), 500