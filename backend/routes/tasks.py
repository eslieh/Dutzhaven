from flask import Blueprint, request, jsonify
from ..models import Task, db
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/create', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    budget = data.get('budget')
    deadline = data.get('deadline')

    if not all([title, description, category, budget, deadline]):
        return jsonify({'message': 'Missing required fields'}), 400

    new_task = Task(
        client_id=current_user_id,
        title=title,
        description=description,
        category=category,
        budget=budget,
        deadline=deadline
    )
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully', 'task_id': new_task.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating task', 'error': str(e)}), 500

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'budget': task.budget,
            'deadline': task.deadline.isoformat() if task.deadline else None,
            'status': task.status,
            'client_id': task.client_id,
        }
        task_list.append(task_data)
    return jsonify(task_list), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'category': task.category,
        'budget': task.budget,
        'deadline': task.deadline.isoformat() if task.deadline else None,
        'status': task.status,
        'client_id': task.client_id,
    }
    return jsonify(task_data), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    current_user_id = get_jwt_identity()
    if task.client_id != current_user_id:
        return jsonify({'message': 'You are not authorized to update this task'}), 403

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.category = data.get('category', task.category)
    task.budget = data.get('budget', task.budget)
    task.deadline = data.get('deadline', task.deadline)
    task.status = data.get('status', task.status)
    try:
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating task', 'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    current_user_id = get_jwt_identity()
    if task.client_id != current_user_id:
        return jsonify({'message': 'You are not authorized to delete this task'}), 403
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting task', 'error': str(e)}), 500