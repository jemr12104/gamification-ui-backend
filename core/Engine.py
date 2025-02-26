from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from data.Connection import db, init_app
from data.Dbhandler import User, Reward, format_user

app = Flask(__name__)
CORS(app)
init_app(app)

app.config["JWT_SECRET_KEY"] = "supersecretkey"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

ADMIN_USERS = {"admin": "password123"}

@app.route('/')
def home():
    return jsonify({"message": "Gamification API is running"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    if username in ADMIN_USERS and ADMIN_USERS[username] == password:
        return jsonify(access_token=create_access_token(identity=username)), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([format_user(user) for user in users])

@app.route('/rewards', methods=['GET', 'POST'])
@jwt_required()
def rewards():
    if request.method == 'GET':
        rewards = Reward.query.all()
        return jsonify([{"id": r.id, "name": r.name, "xp_cost": r.xp_cost} for r in rewards])

    if request.method == 'POST':
        auth_header = request.headers.get("Authorization", "No Authorization header found")
        print("Authorization Header:", auth_header)  # Debugging

        try:
            current_user = get_jwt_identity()
            print("Current User:", current_user)  # Debugging
        except Exception as e:
            print("JWT Error:", str(e))  # Debugging
            return jsonify({"error": "Invalid or expired token"}), 401

        if current_user != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()
        print("Received data:", data)  # Debugging

        if not data or "name" not in data or "xp_cost" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        new_reward = Reward(name=data["name"], xp_cost=data["xp_cost"])
        db.session.add(new_reward)
        db.session.commit()
        return jsonify({"message": "Reward added successfully"}), 201
@app.route('/users/<int:user_id>/xp', methods=['PUT'])
@jwt_required()
def update_xp(user_id):
    current_user = get_jwt_identity()
    if current_user != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if 'xp' not in data:
        return jsonify({"error": "XP value is required"}), 400

    user.xp += data['xp']
    
    if user.xp >= 100:  # Asegurar que se sube de nivel
        user.level += 1
        user.xp = 0  

    db.session.commit()
    return jsonify({
        "message": "XP updated successfully",
        "id": user.id,
        "name": user.name,
        "xp": user.xp,
        "level": user.level
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
