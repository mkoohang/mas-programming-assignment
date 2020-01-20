
import os
import requests
from app import mongo


# Resets parks data in database.
def reset_park_collection():
    key = os.environ.get('NPS_API_KEY')
    url = "https://developer.nps.gov/api/v1/parks"
    result = requests.get(url, params={"limit": 120, "fields": "images", "api_key": key})
    data = result.json()['data']
    new_park_list = []
    for park in data:
        new_park = {}
        if park['latLong']:
            lat, lon = split_lat_long(park['latLong'])
            new_park['lat'] = lat
            new_park['lon'] = lon
        else:
            continue
        if park['images']:
            new_park['image'] = park['images'][0]['url']
        else:
            continue
        new_park['name'] = park['name']
        new_park['description'] = park['description']
        new_park['state'] = park['states']
        new_park['favCount'] = 0
        new_park_list.append(new_park)
    parks = mongo.db.parks
    parks.delete_many({})
    parks.insert_many(new_park_list)


# Resets user accounts in database.
def reset_user_collection():
    users = mongo.db.users
    users.delete_many({})


# Parses the latitude and longitude from the National Park Service API.
def split_lat_long(latlong: str) -> tuple:
    data = latlong.split(',')
    data[0] = data[0][4:]
    data[1] = data[1][6:]
    return float(data[0]), float(data[1])


if __name__ == '__main__':
    reset_park_collection()
    reset_user_collection()
