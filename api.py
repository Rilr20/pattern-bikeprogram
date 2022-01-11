"""
API functions
"""
import requests
PORT = "8000"
#ändra
TOKEN = "EGVk90euINcyV67gfH8hleel0ftezAmovJyLGVRlEjBKVMNdwG7BvOJ7mzRO"
HEADER = {
    'role':'bike',
    'Api_Token':f'{TOKEN}'
    }

API_URL = f'http://backend:{PORT}/sparkapi/v1/'
CITIES = []
PARKING = []
CHARGING = []
def get_users():
    """
    maybe remove?
    sends get request for users
    """
    req = requests.get(f'{API_URL}users')
    req.raise_for_status()
    json = req.json()
    return json

def get_bikes():
    """
    sends get request for all bikes
    """
    req = requests.get(f'{API_URL}bikes',headers=HEADER)
    req.raise_for_status() #gives error if request doesn't work
    json = req.json()
    # print(json)
    return json

def get_one_bike(_id):
    """
    request specific bike
    """
    req = requests.get(f'{API_URL}bikes/{_id}',headers=HEADER)
    req.raise_for_status()
    json = req.json()
    return json

def put_bikes(_id, x_pos, y_pos, status, battery, velocity):
    """
    updates a bikes information
    """
    req_session = requests.Session()
    data = {
        "X": x_pos,
        "Y": y_pos,
        "status": status,
        "battery": battery,
        "velocity": velocity
    }
    req = requests.put(f'{API_URL}bikes/{_id}', data=data, headers=HEADER)
    print(f'PUT status: {req.status_code}')

def get_city_zones():
    """
    gets request for all cities
    """
    req = requests.get(f'{API_URL}cities', headers=HEADER)
    req.raise_for_status()
    json = req.json()
    for row in json:
        # print(row["id"])
        # print(row["city"])
        # print(row["X"])
        # print(row["Y"])
        # print(row["radius"])
        CITIES.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(CITIES)
    return json

def get_parkingspaces():
    """
    get request for all parking spaces
    """
    req = requests.get(f'{API_URL}parkingspaces', headers=HEADER)
    req.raise_for_status()
    json = req.json()
    for row in json:
        # print(json)
        PARKING.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(PARKING)

    return json

def get_chargingstations():
    """
    get request for all chargingstations
    """
    req = requests.get(f'{API_URL}chargingstations', headers=HEADER)
    req.raise_for_status()
    json = req.json()
    for row in json:
        CHARGING.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(CHARGING)
    return json

def area_check(x_pos, y_pos):
    """
    checks if bike is inside city, parkingspace or chargingstation
    returns list
    """
    check_list = []
    check_list.append(city_check(x_pos, y_pos))
    check_list.append(parking_check(x_pos, y_pos))
    check_list.append(charging_check(x_pos, y_pos))
    return check_list

def city_check(x_pos, y_pos):
    """
    checks if bike is inside city, returns false or city id
    """
    if len(CITIES) == 0:
        get_city_zones()
    for city in CITIES:
        result = inside_circle(city[0], city[1],city[2], x_pos, y_pos)
        if result:
            return city[3]
    return False

def parking_check(x_pos, y_pos):
    """
    checks if bike is inside parkingspace, returns false or parking id
    """
    if len(PARKING) == 0:
        get_parkingspaces()

    for parking in PARKING:
        result = inside_circle(parking[0], parking[1],parking[2], x_pos, y_pos)
        if result:
            return parking[3]
    return False

def charging_check(x_pos, y_pos):
    """
    checks if bike is inside chargingstation, returns false or charging id
    """
    if len(CHARGING) == 0:
        get_chargingstations()
    for charging in CHARGING:
        result = inside_circle(charging[0], charging[1],charging[2], x_pos, y_pos)
        if result:
            return charging[3]
    return False

def inside_circle(center_x, center_y, radius, x_pos, y_pos):
    """
    checks if a point is inside a circle or not returns true or false
    """
    square_dist = (center_x - x_pos) ** 2 + (center_y - y_pos) ** 2
    return square_dist <= radius ** 2

def available_bikes():
    """
    sorts through all bikes and keeps the available ones
    """
    bikes = get_bikes()
    bike_list = []
    for bike in bikes:
        if bike["status"] == "available":
            bike_list.append(bike)
    return bike_list

# def post_bike_og():
#     # req_session = requests.Session()
#     # data = {
#     # }
#     # r = requests.post(f'{API_URL}', data=data)
#     # print(f'PUT status: {r.status_code}',headers=HEADER)
#     pass

# def put_bike_log():
#     pass
