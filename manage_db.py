
import os
import requests
from app import mongo


def reset_park_collection():
    key = os.environ.get('NPS_API_KEY')
    url = "https://developer.nps.gov/api/v1/parks"
    result = requests.get(url, params={"limit": 100, "fields": "images", "api_key": key})
    data = result.json()['data']
    new_park = {}
    new_park_list = []
    for park in data:
        new_park['name'] = park['name']
        new_park['description'] = park['description']
        new_park['state'] = park['states']
        if park['images']:
            new_park['image'] = park['images'][0]['url']
        if park['latLong']:
            lat, lon = split_lat_long(park['latLong'])
            new_park['lat'] = lat
            new_park['lon'] = lon
        new_park['starCount'] = 0
        new_park_list.append(new_park)
        new_park = {}
    parks = mongo.db.parks
    parks.delete_many({})
    parks.insert_many(new_park_list)


def split_lat_long(latlong: str) -> tuple:
    data = latlong.split(',')
    data[0] = data[0][4:]
    data[1] = data[1][6:]
    return float(data[0]), float(data[1])


if __name__ == '__main__':
    reset_park_collection()
