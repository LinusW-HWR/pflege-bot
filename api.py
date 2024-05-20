from flask import Blueprint, jsonify, request
from flask_socketio import emit
from navigator import navigate_to_room


api_blueprint = Blueprint('api', __name__)

# Sample list of requests
reqs = [{
            "id": 2,
            "name": "Helga",
            "room": 2,
            "type": "delivery",
            "medicine": "painkiller",
            "status": "done"
        },
        {
            "id": 1,
            "name": "Berta",
            "room": 1,
            "type": "collection",
            "status": "pending"
        }]

@api_blueprint.route('/', methods=['GET'])
def get_requests():
    return jsonify(reqs)

@api_blueprint.route('/request', methods=['PUT', "GET"])
def add_request():
    if request.method == "PUT":
        data = request.json
        new_request = {
            "id": len(reqs) + 1,
            "name": data['name'],
            "room": data['room'],
            "type": data['type'],
            "status": "pending"
        }
        reqs.insert(0, new_request)
        

        emit('new_request', new_request, namespace="/", broadcast=True)
        print("success")
        print(reqs)
        return jsonify({"message": "Request added successfully"}), 201

    if request.method == "GET":
        # Find the request with the specified ID
        req_id = int(request.args.get("id"))
        for r in reqs:
            if r['id'] == req_id:
                return jsonify(r)
        return jsonify({"error": "Request not found"}), 404
    

@api_blueprint.route('/update_req', methods=['POST'])
def update_req():
    req_id = int(request.args.get("id"))
    for r in reqs:
        if r["id"] == req_id:
            for key, value in request.args.items():
                if key == "id":
                    continue
                r[key] = value
                emit('new_request', r, namespace="/", broadcast=True)
                return jsonify({"message": "Req updated successfully!"}), 201

        

@api_blueprint.route('/send_robot', methods=['PUT'])
def send_robot():
    room_id = int(request.args.get("room_id"))
    
    navigate_to_room(room_id)
    
    return jsonify({"message": "Robot has arrived"}), 200