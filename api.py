"""
API functions
"""
import requests
PORT = "8000"
API_URL = f'http://localhost:{PORT}/sparkapi/v1/'
CITIES = []
PARKING = []
CHARGING = []
def getUsers():
    """
    maybe remove?
    sends get request for users
    """
    r = requests.get(f'{API_URL}users')
    r.raise_for_status()
    json = r.json()
    return json

def getBikes():
    """
    sends get request for all bikes
    """
    r = requests.get(f'{API_URL}bikes')
    r.raise_for_status() #gives error if request doesn't work
    json = r.json()
    # print(json)
    return json

def getOneBike(_id):
    """
    request specific bike
    """
    r = requests.get(f'{API_URL}bikes/{_id}')
    r.raise_for_status()
    json = r.json()
    return json

def putBikes(_id, X, Y, status, battery, velocity):
    """
    updates a bikes information
    """
    req_session = requests.Session()
    data = {
        "X": X,
        "Y": Y,
        "status": status,
        "battery": battery,
        "velocity": velocity
    }
    r = requests.put(f'{API_URL}bikes/{_id}', data=data)
    print(f'PUT status: {r.status_code}')

def getCityZones():
    """
    gets request for all cities
    """
    r = requests.get(f'{API_URL}cities')
    r.raise_for_status()
    json = r.json()
    for row in json:
        # print(row["id"])
        # print(row["city"])
        # print(row["X"])
        # print(row["Y"])
        # print(row["radius"])
        CITIES.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(CITIES)
    return json

def getParkingspaces():
    """
    get request for all parking spaces
    """
    r = requests.get(f'{API_URL}parkingspaces')
    r.raise_for_status()
    json = r.json()
    for row in json:
        # print(json)
        PARKING.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(PARKING)

    return json

def getChargingstations():
    """
    get request for all chargingstations
    """
    r = requests.get(f'{API_URL}chargingstations')
    r.raise_for_status()
    json = r.json()
    for row in json:
        CHARGING.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(CHARGING)
    return json

def areaCheck(X, Y):
    """
    checks if bike is inside city, parkingspace or chargingstation
    returns list
    """
    checkList = []
    checkList.append(cityCheck(X, Y))
    checkList.append(parkingCheck(X, Y))
    checkList.append(chargingCheck(X, Y))
    return checkList
    # pass

def cityCheck(X, Y):
    """
    checks if bike is inside city, returns false or city id
    """
    if len(CITIES) == 0:
        getCityZones()
    # print(X)
    # print(X)
    for city in CITIES:
        # print(city)
        # cityX = city[0]
        # cityY = city[1]
        # cityR = city[2]
        # print(f'{cityX}, {cityY}, {cityR}')
        # if cityX + cityR > X > cityX and cityY + cityR > Y > cityY:
        #     return city[3]
        result = insidecircle(city[0], city[1],city[2], X, Y)
        if result:
            return city[3]
    return False

def parkingCheck(X, Y):
    """
    checks if bike is inside parkingspace, returns false or parking id
    """
    if len(PARKING) == 0:
        getParkingspaces()

    for parking in PARKING:
        result = insidecircle(parking[0], parking[1],parking[2], X, Y)
        if result:
            return parking[3]
    return False

def chargingCheck(X, Y):
    """
    checks if bike is inside chargingstation, returns false or charging id
    """
    if len(CHARGING) == 0:
        getChargingstations()
    for charging in CHARGING:
        result = insidecircle(charging[0], charging[1],charging[2], X, Y)
        if result:
            return charging[3]
    return False

def insidecircle(center_x, center_y, radius, x, y):
    """
    checks if a point is inside a circle or not returns true or false
    """
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

def availablebikes():
    """
    sorts through all bikes and keeps the available ones
    """
    bikes = getBikes()
    availablebikes = []
    for bike in bikes:
        if bike["status"] == "available":
            availablebikes.append(bike)
    return availablebikes

# def postBikeLog():
#     # req_session = requests.Session()
#     # data = {
#     # }
#     # r = requests.post(f'{API_URL}', data=data)
#     # print(f'PUT status: {r.status_code}')
#     pass

# def putBikeLog():
#     pass
