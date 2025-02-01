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

    # Check if a review for this task by this reviewer already exists
    existing_review = Review.query.filter_by(task_id=task_id, reviewer_id=reviewer_id).first()
    if existing_review:
      return jsonify({'message': 'You have already reviewed this task'}), 400

    new_review = Review(task_id=task_id, reviewer_id=reviewer_id, reviewee_id=task.client_id, rating=rating, review_text=review_text)
    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review submitted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error submitting review', 'error': str(e)}), 500

@reviews_bp.route('/task/<int:task_id>', methods=['GET'])  # Get reviews for a task
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
        }
        review_list.append(review_data)
    return jsonify(review_list), 200

@reviews_bp.route('/user/<int:user_id>', methods=['GET']) # Get reviews for a user (as reviewee)
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
        }
        review_list.append(review_data)
    return jsonify(review_list), 200