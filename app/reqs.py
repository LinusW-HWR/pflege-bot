from flask import Blueprint, jsonify, request
from flask_socketio import emit


reqs_blueprint = Blueprint('request', __name__)

reqs = [{
            "id": 2,
            "name": "Helga",
            "room": "Raum 1",
            "type": "delivery",
            "medicine": "painkiller",
            "status": "done"
        },
        {
            "id": 1,
            "name": "Berta",
            "room": "Raum 2",
            "type": "collection",
            "status": "pending"
        }]


@reqs_blueprint.route('/', methods=['GET'])
def get_requests():
    if "id" in request.args:
        req_id = int(request.args.get("id"))
        for r in reqs:
            if r['id'] == req_id:
                return jsonify(r)
        return jsonify({"error": "Request not found"}), 404
    
    return jsonify(reqs), 200


@reqs_blueprint.route('/add', methods=['PUT'])
def add_request():
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
    return jsonify({"message": "Request added successfully"}), 201
    

@reqs_blueprint.route('/update', methods=['PUT'])
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
    return jsonify({"error": "Request not found"}), 404