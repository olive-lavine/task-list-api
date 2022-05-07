from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("bp", __name__, url_prefix="/tasks")

def error_message(message, status_code):
        abort(make_response(jsonify(dict(details=message)), status_code))

def make_task_safely(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def get_task_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)

    task = Task.query.get(id)

    if task:
        return task
    
    error_message(f"No task with id {id} found", 404)

@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()

    task = make_task_safely(request_body)

    db.session.add(task)
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    result_list = [task.to_dict() for task in tasks]

    return jsonify(result_list)

@tasks_bp.route("/<id>", methods=["Get"])
def read_task_by_id(id):
    task = get_task_record_by_id(id)
    return jsonify({"task":task.to_dict()})