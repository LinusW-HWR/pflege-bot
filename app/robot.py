from flask import Blueprint, jsonify, request
from flask_socketio import emit
from .navigator import navigate_to_room, run_auto_collection
from .reqs import reqs

robot_blueprint = Blueprint('robot', __name__)


@robot_blueprint.route('/send', methods=['PUT'])
def send_robot():
    
    if "room" in request.args:
        room = request.args.get("room")
        navigate_to_room(room)
        return jsonify({"message": "Robot has arrived"}), 200
    
    return jsonify({"error": "An error has occured"}), 400


@robot_blueprint.route('/auto_collection', methods=['PUT'])
def start_auto_collection():
    collection_reqs = []
    rooms_too_include = []

    for req in reqs:
        if req["type"] == "collection" and req["status"] != "done":
            collection_reqs.append(req)
            rooms_too_include.append(req["room"])
            req["status"] = "in progress"

    emit('new_request',  namespace="/", broadcast=True)

    run_auto_collection(rooms_too_include)
    
    for req in collection_reqs:
        req["status"] = "done"
    
    emit('new_request',  namespace="/", broadcast=True)

    return jsonify({"message": "Autocollection complete!"}), 200