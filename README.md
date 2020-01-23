# National Parks API 🌲
This is a backend API for accessing and favoriting national parks from the National Park Services API.

## Features ⭐️
- User accounts
- JWT Token Authentication
- National Park Service API Integration
- Favoriting and unfavoriting parks
- Wish lists for keeping track of favorite parks

## Tech Stack 🐍
- Flask (Python)
- MongoDB

## Run ⬆️

### Live
The app is currently running live at https://powerful-wildwood-07865.herokuapp.com. You can use a REST client such as [Postman](https://www.getpostman.com/)
to make HTTP requests or write scripts in your language of choice. Instructions for access are listed under 'Instructions'.

### Local
Running this app with a local MongoDB database is quite difficult, so all you'll have to do 
is connect to the live database we are running rather than create your own. We provide the URI
to it in an environment variable below.

To run this app locally, you need to follow these steps:
1. Make sure you have [Python 3](https://www.python.org/downloads/) installed
2. Download or clone the repository
3. `cd` in to the repository and create a virtual environment `python3 -m venv ./venv`
4. Activate the virtual environment `source ./venv/bin/activate`
5. Install the required packages `pip install -r requirements.txt`
6. Export the following environment variables in your terminal or change the values in the `create_app()` function in the app.py file from `os.environ.get()` to the values listed here. These values are 
included in the write up for the assignment rather than this README for security purposes. 
Please refer to my written submission for the values of these environment variables. 
	1. Example for how to export: type `export MONGODB_URI=valueinwriteup`. Repeat this process for all 6 variables shown below and replace 'somevalue' with the value given in the write up submission. DO NOT put quotes around the value.
	2. Example for replacing values in 'app.py': Change `application.config['MONGO_URI'] = os.environ.get('MONGODB_URI')` to `application.config['MONGO_URI'] = "valueinwriteup"`. MAKE SURE to include the quotes around the value so that it's a string.
	3. Repeat either of these processes for each of the variables below.
		1. MONGODB_URI=?
		2. FLASK_ENV=?
		3. DEBUG=?
		4. TESTING=?
		5. SECRET_KEY=?
		6. NPS_API_KEY=?
7. Run the app in the terminal `python app.py`

The app should now be running. Follow the rest of the instructions to interact with it.

## Instructions 📜
1. Register with the API through the `rest/register` endpoint
2. Login to the API through the `rest/login` endpoint
3. Use the API token returned to you from the login or registration endpoint to access 
all other endpoints

## Endpoints ⚡️

- LIVE base_url = https://powerful-wildwood-07865.herokuapp.com
- LOCAL base_url = (check your terminal when you do step #7 in the 'Run' section to see what
address the app is running on; it's most likely 127.0.0.1:5000)

### Registration 📝
**POST** `{base_url}/rest/register`
- This is where you can register users with the service.
- Body
```
{
	"username": "michael",
	"password": "password"
}
```
 - Return
```
{
    "message": "New user 'michael' created!",
    "token": "eyJ0eXAiOiJKV1Qi2CJhbGciOi9IUzI1NiJ9.eyJ0c2VyIjoibWljaGFl1CIsImV4c2I6MTU3OTKwMPUxOX0.cXy8y9qXtQ48j88oTLJ-dr5LAcA-vwwpATb5mcdw-DY"
}
```

### Login ⌨️
**POST** `{base_url}/rest/login`
- This is where you can log in to the service.
- Body
```
{
	"username": "michael",
	"password": "password"
}
```

 - Return
```
{
    "message": "Login successful!",
    "token": "eyJ0eXAiOiJKV1Qi2CJhbGciOi9IUzI1NiJ9.eyJ0c2VyIjoibWljaGFl1CIsImV4c2I6MTU3OTKwMPUxOX0.cXy8y9qXtQ48j88oTLJ-dr5LAcA-vwwpATb5mcdw-DY"
}
```

### All Parks 🏞
**GET** `{base_url}/rest/allparks`
- This is where you can view all parks.
- Headers
```
Authorization: eyJ0eXAiOiJKV1Qi2CJhbGciOi9IUzI1NiJ9.eyJ0c2VyIjoibWljaGFl1CIsImV4c2I6MTU3OTKwMPUxOX0.cXy8y9qXtQ48j88oTLJ-dr5LAcA-vwwpATb5mcdw-DY
```
 - Return
```
{
    "parks": [
        {
            "_id": "5e23f4e7318123e9fe6712e6",
            "description": "Salt River Bay National Historical Park and Ecological Preserve uniquely documents the human and natural Caribbean world from the earliest indigenous settlements in the central Caribbean to their clash with seven different colonial European powers to the present day.",
            "favCount": 0,
            "image": "https://www.nps.gov/common/uploads/structured_data/D0B758DC-1DD8-B71B-0B463C640F211F0A.jpg",
            "lat": 17.77908602,
            "lon": -64.75519348,
            "name": "Salt River Bay",
            "state": "VI"
        },
        {
            "_id": "5e23f4e7318123e9fe6712d3",
            "description": "Discover the history of all the peoples of Natchez, Mississippi, from European settlement, African enslavement, the American cotton economy, to the Civil Rights struggle on the lower Mississippi River.",
            "favCount": 0,
            "image": "https://www.nps.gov/common/uploads/structured_data/3C81B011-1DD8-B71B-0BCDE1769DEF9DCF.jpg",
            "lat": 31.54697621,
            "lon": -91.39040665,
            "name": "Natchez",
            "state": "MS"
        }
        .
        .
        .
    ]
}
```

### Favorite Park ➕🏞
**POST** `{base_url}/rest/favorite`
- This is where you can favorite a park.
- Body
```
{
	"park_id": "5e23f4e7318123e9fe6712a0"
}
```
- Headers
```
Authorization: eyJ0eXAiOiJKV1Qi2CJhbGciOi9IUzI1NiJ9.eyJ0c2VyIjoibWljaGFl1CIsImV4c2I6MTU3OTKwMPUxOX0.cXy8y9qXtQ48j88oTLJ-dr5LAcA-vwwpATb5mcdw-DY
```
 - Return
```
{
    "message": "This park was successfully favorited.",
    "park": {
        "_id": "5e23f4e7318123e9fe6712a0",
        "description": "Almost 70 miles (113 km) west of Key West lies the remote Dry Tortugas National Park. This 100-square mile park is mostly open water with seven small islands.  Accessible only by boat or seaplane, the park is known the world over as the home of magnificent Fort Jefferson, picturesque blue waters, superlative coral reefs and marine life, and the vast assortment of bird life that frequents the area.",
        "favCount": 1,
        "image": "https://www.nps.gov/common/uploads/structured_data/3C80FF02-1DD8-B71B-0B39AC51BF7B2FA2.jpg",
        "lat": 24.628741,
        "lon": -82.87319,
        "name": "Dry Tortugas",
        "state": "FL"
    },
    "wishlist": [
        {
            "_id": "5e23f4e7318123e9fe6712a0",
            "description": "Almost 70 miles (113 km) west of Key West lies the remote Dry Tortugas National Park. This 100-square mile park is mostly open water with seven small islands.  Accessible only by boat or seaplane, the park is known the world over as the home of magnificent Fort Jefferson, picturesque blue waters, superlative coral reefs and marine life, and the vast assortment of bird life that frequents the area.",
            "favCount": 1,
            "image": "https://www.nps.gov/common/uploads/structured_data/3C80FF02-1DD8-B71B-0B39AC51BF7B2FA2.jpg",
            "lat": 24.628741,
            "lon": -82.87319,
            "name": "Dry Tortugas",
            "state": "FL"
        }
    ]
}
```

### Unfavorite Park ➖🏞
**POST** `{base_url}/rest/unfavorite`
- This is where you can unfavorite a park.
- Body
```
{
    "park_id": "5e23f4e7318123e9fe6712a0"
}
```
- Headers
```
Authorization: eyJ0eXAiOiJKV1Qi2CJhbGciOi9IUzI1NiJ9.eyJ0c2VyIjoibWljaGFl1CIsImV4c2I6MTU3OTKwMPUxOX0.cXy8y9qXtQ48j88oTLJ-dr5LAcA-vwwpATb5mcdw-DY
```
 - Return
```
{
    "message": "This park was successfully unfavorited.",
    "park": {
        "_id": "5e23f4e7318123e9fe6712a0",
        "description": "Almost 70 miles (113 km) west of Key West lies the remote Dry Tortugas National Park. This 100-square mile park is mostly open water with seven small islands.  Accessible only by boat or seaplane, the park is known the world over as the home of magnificent Fort Jefferson, picturesque blue waters, superlative coral reefs and marine life, and the vast assortment of bird life that frequents the area.",
        "favCount": 0,
        "image": "https://www.nps.gov/common/uploads/structured_data/3C80FF02-1DD8-B71B-0B39AC51BF7B2FA2.jpg",
        "lat": 24.628741,
        "lon": -82.87319,
        "name": "Dry Tortugas",
        "state": "FL"
    },
    "wishlist": []
}
```

### User 👨🏼‍💻
**GET** `{base_url}/rest/user`
 - This is where you can view user info, including wish lists.
- Headers
```
Authorization: eyJ0eXAiOiJKV1Qi2CJhbGciOi9IUzI1NiJ9.eyJ0c2VyIjoibWljaGFl1CIsImV4c2I6MTU3OTKwMPUxOX0.cXy8y9qXtQ48j88oTLJ-dr5LAcA-vwwpATb5mcdw-DY
```
 - Return
```
{
    "_id": "5e23f86c98d1847d7705c178",
    "password": "$2b$12$/0Pgf3VzGbh/NvLNmOLeEungcLR5w6wE.wixMck6CLH6kh7cGrmqy",
    "username": "michael",
    "wishlist": [
        {
            "_id": "5e23f4e7318123e9fe6712a0",
            "description": "Almost 70 miles (113 km) west of Key West lies the remote Dry Tortugas National Park. This 100-square mile park is mostly open water with seven small islands.  Accessible only by boat or seaplane, the park is known the world over as the home of magnificent Fort Jefferson, picturesque blue waters, superlative coral reefs and marine life, and the vast assortment of bird life that frequents the area.",
            "favCount": 1,
            "image": "https://www.nps.gov/common/uploads/structured_data/3C80FF02-1DD8-B71B-0B39AC51BF7B2FA2.jpg",
            "lat": 24.628741,
            "lon": -82.87319,
            "name": "Dry Tortugas",
            "state": "FL"
        }
    ]
}
```
