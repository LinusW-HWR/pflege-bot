from flask import Blueprint, jsonify, request
from .navigator import navigate_to_room


robot_blueprint = Blueprint('robot', __name__)


@robot_blueprint.route('/send', methods=['PUT'])
def send_robot():
    
    if "room_id" in request.args:
        room_id = int(request.args.get("room_id"))
        navigate_to_room(room_id)
        return jsonify({"message": "Robot has arrived"}), 200
    
    return jsonify({"error": "An error has occured"}), 400
