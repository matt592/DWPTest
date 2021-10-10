import requests
from math import sin, cos, sqrt, atan2, radians
import json

def get_city_users(city):
    url = "https://bpdts-test-app.herokuapp.com/city/" + city + "/users"
    payload = ""
    response = requests.request("GET", url, data=payload)
    return response.json()


def get_distance(target_lat, target_long, center_lat, center_long):
    # approximate radius of earth in miles
    radius = 3958.8

    lat1 = radians(target_lat)
    lon1 = radians(target_long)
    lat2 = radians(center_lat)
    lon2 = radians(center_long)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = radius * c
    return distance


def get_users_within_radius(center_lat, center_long, miles):
    url = "https://bpdts-test-app.herokuapp.com/users"
    payload = ""
    response = requests.request("GET", url, data=payload)
    users = response.json()
    users_within_radius = []
    for user in users:
        # get distance between center and target
        distance_between = get_distance(float(user['latitude']), float(user['longitude']), center_lat, center_long)
        # all users within radius of center are appended to the list
        if distance_between <= miles:
            users_within_radius.append(user)
    return users_within_radius


london_lat = 51.509865
london_long = -0.118092
# get users that are in london
result = get_city_users("London")
# get users within 50 mile radius of london
result.extend(get_users_within_radius(london_lat, london_long, 50))
print(json.dumps(result,sort_keys=True, indent=4))
