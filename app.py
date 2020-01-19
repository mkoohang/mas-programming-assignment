from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo, ObjectId
from functools import wraps
import jwt
import bcrypt
import datetime
import os


def create_app():
    application = Flask(__name__)
    application.config['DEBUG'] = os.environ.get('DEBUG')
    application.config['TESTING'] = os.environ.get('TESTING')
    application.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')
    application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    application.config['MONGO_URI'] = os.environ.get('MONGODB_URI')
    application.config['NPS_API_KEY'] = os.environ.get('NPS_API_KEY')
    return application


app = create_app()
mongo = PyMongo(app)


# Token verification decorator. This checks to see if the token passed to the endpoint is valid
# and is applied to the endpoints that require tokens to access.
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


@app.route('/rest/allparks', methods=['GET'])
@token_required
def allparks():
    parks = mongo.db.parks.find()
    result = []
    for park in parks:
        park['_id'] = str(park['_id'])
        result.append(park)
    return jsonify({"parks": result})


@app.route('/rest/favorite', methods=['POST'])
@token_required
def favorite():
    data = request.get_json()
    if 'park_id' in data:
        parks = mongo.db.parks
        park = parks.find_one({'_id': ObjectId(data['park_id'])})
        if park:
            username = jwt.decode(request.headers["Authorization"], app.config["SECRET_KEY"])['user']
            users = mongo.db.users
            user = users.find_one({'username': username})
            if str(park['_id']) not in user['wishlist']:
                users.update_one(
                    {'username': username},
                    {'$push': {'wishlist': str(park['_id'])}}
                )
                parks.update_one(
                    {'_id': ObjectId(data['park_id'])},
                    {'$set': {'favCount': park['favCount'] + 1}}
                )
                user = users.find_one({'username': username})
                favorited_park = parks.find_one({'_id': ObjectId(data['park_id'])})

                wishlist_parks = []
                for park_id in user['wishlist']:
                    park = parks.find_one({'_id': ObjectId(park_id)})
                    park['_id'] = str(park['_id'])
                    wishlist_parks.append(park)
                user['wishlist'] = wishlist_parks

                favorited_park['_id'] = str(park['_id'])
                return jsonify({"message": "This park was successfully favorited.", "park": favorited_park,
                                "wishlist": user['wishlist']})

            else:
                return jsonify({"message": "This park is already in your favorites."}), 401
        else:
            return jsonify({"message": "No park with that id exists."}), 401
    else:
        return jsonify({"message": "Park id missing!"}), 401


@app.route('/rest/unfavorite', methods=['POST'])
@token_required
def unfavorite():
    data = request.get_json()
    if 'park_id' in data:
        parks = mongo.db.parks
        park = parks.find_one({'_id': ObjectId(data['park_id'])})
        if park:
            username = jwt.decode(request.headers["Authorization"], app.config["SECRET_KEY"])['user']
            users = mongo.db.users
            user = users.find_one({'username': username})
            if str(park['_id']) in user['wishlist']:
                users.update_one(
                    {'username': username},
                    {'$pull': {'wishlist': str(park['_id'])}}
                )
                parks.update_one(
                    {'_id': ObjectId(data['park_id'])},
                    {'$set': {'favCount': park['favCount'] - 1}}
                )
                user = users.find_one({'username': username})
                unfavorited_park = parks.find_one({'_id': ObjectId(data['park_id'])})

                wishlist_parks = []
                for park_id in user['wishlist']:
                    park = parks.find_one({'_id': ObjectId(park_id)})
                    park['_id'] = str(park['_id'])
                    wishlist_parks.append(park)
                user['wishlist'] = wishlist_parks

                unfavorited_park['_id'] = str(park['_id'])
                return jsonify({"message": "This park was successfully unfavorited.", "park": unfavorited_park,
                                "wishlist": user['wishlist']})

            else:
                return jsonify({"message": "This park is not in your favorites."}), 401
        else:
            return jsonify({"message": "No park with that id exists."}), 401
    else:
        return jsonify({"message": "Park id missing!"}), 401


@app.route('/rest/user', methods=['GET'])
@token_required
def user():
    username = jwt.decode(request.headers["Authorization"], app.config["SECRET_KEY"])['user']
    users = mongo.db.users
    user = users.find_one({'username': username})
    if user:
        user['_id'] = str(user['_id'])
        user['password'] = user['password'].decode('utf-8')
        parks = mongo.db.parks
        wishlist_parks = []
        for park_id in user['wishlist']:
            park = parks.find_one({'_id': ObjectId(park_id)})
            park['_id'] = str(park['_id'])
            wishlist_parks.append(park)
        user['wishlist'] = wishlist_parks
        return jsonify(user)
    return jsonify({"message": "User does not exist!"}), 401


if __name__ == '__main__':
    app.run()
