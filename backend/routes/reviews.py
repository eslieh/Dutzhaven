from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Review, Task, db

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/create/<int:task_id>', methods=['POST'])
@jwt_required()
def create_review(task_id):
    reviewer_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)

    data = request.get_json()
    rating = data.get('rating')
    review_text = data.get('review_text')

    if not all([rating, review_text]):
        return jsonify({'message': 'Missing required fields'}), 400

    if not isinstance(rating, int) or not 1 <= rating <= 5: # Validate rating
      return jsonify({'message': 'Rating must be an integer between 1 and 5'}), 400

    existing_review = Review.query.filter_by(task_id=task_id, reviewer_id=reviewer_id).first()
    if existing_review:
      return jsonify({'message': 'You have already reviewed this task'}), 400

    new_review = Review(task_id=task_id, reviewer_id=reviewer_id, reviewee_id=task.client_id, rating=rating, review_text=review_text)
    try:
        db.session.add(new_review)
        db.session.commit()

        review_data = { # Return review data on successful creation
            'id': new_review.id,
            'task_id': new_review.task_id,
            'reviewer_id': new_review.reviewer_id,
            'reviewee_id': new_review.reviewee_id,
            'rating': new_review.rating,
            'review_text': new_review.review_text,
            'timestamp': new_review.timestamp.isoformat() if new_review.timestamp else None,
            'reviewer': { # Include reviewer details
                'id': new_review.reviewer.id,
                'username': new_review.reviewer.username,
                # ... other reviewer details
            } if new_review.reviewer else None,
        }

        return jsonify({'message': 'Review submitted successfully', 'review': review_data}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error submitting review', 'error': str(e)}), 500

@reviews_bp.route('/task/<int:task_id>', methods=['GET'])
def get_reviews_for_task(task_id):
    reviews = Review.query.filter_by(task_id=task_id).all()
    review_list = []
    for review in reviews:
        review_data = {
            'id': review.id,
            'task_id': review.task_id,
            'reviewer_id': review.reviewer_id,
            'reviewee_id': review.reviewee_id,
            'rating': review.rating,
            'review_text': review.review_text,
            'timestamp': review.timestamp.isoformat() if review.timestamp else None,
            'reviewer': { # Include reviewer details
                'id': review.reviewer.id,
                'username': review.reviewer.username,
                # ... other reviewer details
            } if review.reviewer else None,
        }
        review_list.append(review_data)
    return jsonify(review_list), 200

@reviews_bp.route('/user/<int:user_id>', methods=['GET'])
def get_reviews_for_user(user_id):
    reviews = Review.query.filter_by(reviewee_id=user_id).all()
    review_list = []
    for review in reviews:
        review_data = {
            'id': review.id,
            'task_id': review.task_id,
            'reviewer_id': review.reviewer_id,
            'reviewee_id': review.reviewee_id,
            'rating': review.rating,
            'review_text': review.review_text,
            'timestamp': review.timestamp.isoformat() if review.timestamp else None,
            'reviewer': { # Include reviewer details
                'id': review.reviewer.id,
                'username': review.reviewer.username,
                # ... other reviewer details
            } if review.reviewer else None,
        }
        review_list.append(review_data)
    return jsonify(review_list), 200