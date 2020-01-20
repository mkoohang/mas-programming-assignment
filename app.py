import os
import jwt
import bcrypt
import datetime
from functools import wraps
from flask_pymongo import PyMongo, ObjectId
from flask import Flask, jsonify, request, render_template


def create_app() -> Flask:
    '''
    # Configures application and returns it.
    :return:
    '''
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


def token_required(f):
    '''
    # Token verification decorator. This checks to see if the token passed to the endpoint is valid
    # and is applied to the endpoints that require authentication for access.
    :param f:
    :return:
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        # Authorization in headers and is not blank.
        if "Authorization" in request.headers and request.headers["Authorization"]:
            token = request.headers["Authorization"]
            # Try extracting data from the token. If it fails, return an error message.
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"])
            except:
                return jsonify({"message": "Token is invalid!"}), 401
        else:
            return jsonify({"message": "Token is missing!"}), 401

        return f(*args, **kwargs)

    return decorated


# Landing page that links to the GitHub repository.
@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


# Endpoint for logging into the API.
@app.route('/rest/login', methods=['POST'])
def login():
    data = request.get_json()
    # Check if the username and password are in the data.
    if 'username' in data and 'password' in data:
        # Grab the users collection from the Mongo database.
        users = mongo.db.users
        # Query the user with the username provided in the data.
        login_user = users.find_one({'username': data['username']})

        # If the user exists.
        if login_user:
            # Check the password provided with the hashed password in the database.
            if bcrypt.checkpw(data['password'].encode('utf-8'), login_user['password']):
                # Generate a new JWT token that lasts for 24 hours.
                token = jwt.encode({"user": data["username"], "exp": datetime.datetime.utcnow() +
                                        datetime.timedelta(hours=24)}, app.config["SECRET_KEY"])
                return jsonify({"message": "Login succesful!", "token": token.decode('utf-8')})
            else:
                return jsonify({"message": "Incorrect password! Please try again."}), 401

        return jsonify({"message": "User '" + data["username"] + "' does not exist!"}), 401
    else:
        return jsonify({"message": "Username or password missing!"}), 401


# Endpoint for registering with the API.
@app.route('/rest/register', methods=['POST'])
def register():
    data = request.get_json()
    # Check if the username and password are in the data.
    if 'username' in data and 'password' in data:
        # Grab the users collection from the Mongo database.
        users = mongo.db.users
        # Query the user with the username provided in the data.
        existing_user = users.find_one({'username': data['username']})

        # Check if the user with the username provided does not exist in the database.
        if existing_user is None:
            # Create a new hashed password.
            hashpass = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            # Insert the new user into the database.
            users.insert({'username': data['username'], 'password': hashpass, 'wishlist': []})
            # Generate a JWT token to return to the user.
            token = jwt.encode({"user": data["username"], "exp": datetime.datetime.utcnow() +
                                        datetime.timedelta(hours=24)}, app.config["SECRET_KEY"])
            return jsonify({"message": "New user '" + data["username"] + "' created!", "token": token.decode('utf-8')})

        return jsonify({"message": "User '" + data["username"] + "' already exists!"}), 401
    else:
        return jsonify({"message": "Username or password missing!"}), 401


# Endpoint for accessing all parks in the database.
@app.route('/rest/allparks', methods=['GET'])
@token_required
def allparks():
    # Get all the parks in the database.
    parks = mongo.db.parks.find()
    result = []
    # Sort through each park, cast its object id to a string, and append it to the resulting list.
    for park in parks:
        park['_id'] = str(park['_id'])
        result.append(park)
    return jsonify({"parks": result})


# Endpoint for favoriting a particular park.
@app.route('/rest/favorite', methods=['POST'])
@token_required
def favorite():
    data = request.get_json()
    # Check if the park_id was provided in the request.
    if 'park_id' in data:
        # Grab the parks collection from the database.
        parks = mongo.db.parks
        # Query the park with the given park_id.
        park = parks.find_one({'_id': ObjectId(data['park_id'])})
        # If the park is in the database.
        if park:
            # Get the username of the user from the JWT token.
            username = jwt.decode(request.headers["Authorization"], app.config["SECRET_KEY"])['user']
            users = mongo.db.users
            # Query the user with that username from the database.
            user = users.find_one({'username': username})
            # Check if the park_id of that park is not in the wishlist of the user.
            if str(park['_id']) not in user['wishlist']:
                # Add the park_id to the user's wishlist.
                users.update_one(
                    {'username': username},
                    {'$push': {'wishlist': str(park['_id'])}}
                )
                # Increment the favorite count of the park.
                parks.update_one(
                    {'_id': ObjectId(data['park_id'])},
                    {'$set': {'favCount': park['favCount'] + 1}}
                )
                # Retrieve the new user data.
                user = users.find_one({'username': username})
                # Retrieve the new park data.
                favorited_park = parks.find_one({'_id': ObjectId(data['park_id'])})

                # Generate the wishlist of parks for the user to be returned in the message.
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


# Endpoint for unfavoriting a particular park.
@app.route('/rest/unfavorite', methods=['POST'])
@token_required
def unfavorite():
    data = request.get_json()
    # Check if the park_id was provided in the request.
    if 'park_id' in data:
        # Grab the parks collection from the database.
        parks = mongo.db.parks
        # Query the park with the given park_id.
        park = parks.find_one({'_id': ObjectId(data['park_id'])})
        # If the park is in the database.
        if park:
            # Get the username of the user from the JWT token.
            username = jwt.decode(request.headers["Authorization"], app.config["SECRET_KEY"])['user']
            users = mongo.db.users
            # Query the user with that username from the database.
            user = users.find_one({'username': username})
            # Check if the park_id of that park is in the wishlist of the user.
            if str(park['_id']) in user['wishlist']:
                # Add the park_id to the user's wishlist.
                users.update_one(
                    {'username': username},
                    {'$pull': {'wishlist': str(park['_id'])}}
                )
                # Decrement the favorite count of the park.
                parks.update_one(
                    {'_id': ObjectId(data['park_id'])},
                    {'$set': {'favCount': park['favCount'] - 1}}
                )
                # Retrieve the new user data.
                user = users.find_one({'username': username})
                # Retrieve the new park data.
                unfavorited_park = parks.find_one({'_id': ObjectId(data['park_id'])})

                # Generate the wishlist of parks for the user to be returned in the message.
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


# Endpoint for viewing user data, including the wishlist.
@app.route('/rest/user', methods=['GET'])
@token_required
def user():
    # Decode the username from the JWT token
    username = jwt.decode(request.headers["Authorization"], app.config["SECRET_KEY"])['user']
    # Retrieve the user from the database.
    users = mongo.db.users
    user = users.find_one({'username': username})
    # If the user exists in the database
    if user:
        # Format user data and wishlist for display.
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
