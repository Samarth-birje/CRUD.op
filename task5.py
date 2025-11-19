from flask import Flask, request, jsonify

app = Flask(__name__)
users = {
    1: {"username": "alice", "email":"Samarth67@gmail.com"},
    2: {"username": "bandi", "email":"Bandi@gmail.com"},
}
next_user_id = 3

@app.route('/users', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json()

    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"message":"missing required fields(username, email)"}), 400
    
    new_user_id = next_user_id

    users[new_user_id] = {
        "username": data["username"],
        "email": data["email"]
    }

    next_user_id +=1

    return jsonify({
        "id": new_user_id,
        "username": users[new_user_id]["username"],
        "email": users[new_user_id]["email"]
    }),201

@app.route('/users', methods=['GET'])
def get_all_users():
    user_list = []
    for user_id, user_data in users.items():
        user_list.append({"id": user_id, **user_data})

    return jsonify(user_list)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        user_data = users[user_id]
       
        return jsonify({"id": user_id, **user_data})
    else:
        
        return jsonify({"message": "User not found"}), 404
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"message": "Missing required fields for update (username, email)"}), 400

    users[user_id]["username"] = data["username"]
    users[user_id]["email"] = data["email"]
    return jsonify({"id": user_id, **users[user_id]})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
      
        del users[user_id]
      
        return '', 204
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
  
    app.run(debug=True)