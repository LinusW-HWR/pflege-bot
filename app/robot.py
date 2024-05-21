from flask import Blueprint, jsonify, request
from .navigator import navigate_to_room

robot_blueprint = Blueprint('robot', __name__)


@robot_blueprint.route('/send', methods=['PUT'])
def send_robot():
    
    if "room" in request.args:
        room = request.args.get("room")
        navigate_to_room(room)
        return jsonify({"message": "Robot has arrived"}), 200
    
    return jsonify({"error": "An error has occured"}), 400
