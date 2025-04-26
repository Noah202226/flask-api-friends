from app import app, db
from flask import request, jsonify
from models import Friend

# Get all friends
@app.route('/api/friends', methods=['GET'])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)

@app.route('/api/friends', methods=['POST'])
def create_friends():
    
    try:
        data = request.json

        required_fields = ['name', 'role', 'description','gender']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        name = data.get('name')
        role = data.get('role')
        description = data.get('description')
        gender = data.get('gender')

        if gender == 'male': 
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == 'female':
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_friend = Friend(name=name, role=role, description = description, gender = gender, img_url = img_url)

        db.session.add(new_friend)
        db.session.commit()

        return jsonify({"msg": "Friend created successfully"}), 201
   
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error":str(ex)}), 500
   
@app.route('/api/friends/<int:friend_id>', methods=['DELETE'])
def delete_friend(friend_id):
    try:
        friend = Friend.query.get_or_404(friend_id)
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg": "Friend deleted successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 500