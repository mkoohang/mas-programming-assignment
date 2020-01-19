from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from functools import wraps
import jwt
import bcrypt
import datetime
import os

app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('DEBUG')
app.config['TESTING'] = os.environ.get('TESTING')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')
app.config['NPS_API_KEY'] = os.environ.get('NPS_API_KEY')
mongo = PyMongo(app)


# Token verification decorator. This checks to see if the token passed to the endpoint is valid
# and is applied to the endpoints that require login before access.
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers and request.headers["Authorization"]:
            token = request.headers["Authorization"]
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"])
            except:
                return jsonify({"message": "Token is invalid!"}), 401
        else:
            return jsonify({"message": "Token is missing!"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@app.route('/rest/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'username' in data and 'password' in data:
        users = mongo.db.users
        login_user = users.find_one({'username': data['username']})

        if login_user:
            if bcrypt.checkpw(data['password'].encode('utf-8'), login_user['password']):
                token = jwt.encode({"user": data["username"], "exp": datetime.datetime.utcnow() +
                                        datetime.timedelta(hours=24)}, app.config["SECRET_KEY"])
                return jsonify({"message": "Login succesful!", "token": token.decode('utf-8')})
            else:
                return jsonify({"message": "Incorrect password! Please try again."}), 401

        return jsonify({"message": "User '" + data["username"] + "' does not exist!"}), 401
    else:
        return jsonify({"message": "Username or password missing!"}), 401


@app.route('/rest/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'username' in data and 'password' in data:
        users = mongo.db.users
        existing_user = users.find_one({'username': data['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': data['username'], 'password': hashpass, 'wishlist': []})
            token = jwt.encode({"user": data["username"], "exp": datetime.datetime.utcnow() +
                                        datetime.timedelta(hours=24)}, app.config["SECRET_KEY"])
            return jsonify({"message": "New user '" + data["username"] + "' created!", "token": token.decode('utf-8')})

        return jsonify({"message": "User '" + data["username"] + "' already exists!"}), 401
    else:
        return jsonify({"message": "Username or password missing!"}), 401


@app.route('/rest/allparks')
@token_required
def allparks():
    parks = mongo.db.parks.find()
    result = []
    for park in parks:
        park['_id'] = str(park['_id'])
        result.append(park)
    return jsonify({"parks": result})


if __name__ == '__main__':
    app.run()
