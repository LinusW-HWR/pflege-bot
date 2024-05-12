from flask import Blueprint, jsonify, request
from flask_socketio import emit

api_blueprint = Blueprint('api', __name__)

# Sample list of requests
requests = []

@api_blueprint.route('/', methods=['GET'])
def get_requests():
    return jsonify(requests)

@api_blueprint.route('/request', methods=['PUT'])
def add_request():
    data = request.json
    new_request = {
        "id": len(requests) + 1,
        "name": data['name'],
        "room": data['room'],
        "type": data['type'],
        "status": "in progress"
    }
    requests.insert(0, new_request)
    

    emit('new_request', new_request, namespace="/", broadcast=True)
    print("success")
    print(requests)
    return jsonify({"message": "Request added successfully"}), 201

@api_blueprint.route('/send_robot', methods=['PUT'])
def send_robot():
    req_id = request.args.get("id")
    print(f"Sending robot: {req_id}")
    return jsonify({"message": "Robot send successfully"}), 200