"""
API functions
"""
import requests
PORT = "8000"
API_URL = f'http://localhost:{PORT}/sparkapi/v1/'
CITIES = []
PARKING = []
CHARGING = []
def getBikes():
    r = requests.get(f'{API_URL}bikes')
    r.raise_for_status() #gives error if request doesn't work
    json = r.json()
    return json

def putBikes(_id, X, Y, battery, velocity):
        req_session = requests.Session()
        data = {
            "X": X,
            "Y": Y,
            "battery": battery,
            "velocity": velocity
        }
        r = requests.put(f'{API_URL}bikes/{_id}', data=data)
        print(f'PUT status: {r.status_code}')

def getCityZones():

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
    r = requests.get(f'{API_URL}parkingspaces')
    r.raise_for_status()
    json = r.json()
    for row in json:
        # print(json)
        PARKING.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(PARKING)

    return json

def getChargingstations():
    r = requests.get(f'{API_URL}chargingstations')
    r.raise_for_status()
    json = r.json()
    for row in json:
        CHARGING.append([float(row["X"]), float(row["Y"]), float(row["radius"]), row["id"]])
    # print(CHARGING)
    return json

def areacheck(X, Y):
    #absolutbelopet av X & Y för att sedan se om de är mindre eller lika med området i city

    pass

def cityCheck(X, Y):
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
    if len(PARKING) == 0:
        getParkingspaces()

    for parking in PARKING:
        result = insidecircle(parking[0], parking[1],parking[2], X, Y)
        if result:
            return parking[3]
    return False

def chargingCheck(X, Y):
    if len(CHARGING) == 0:
        getChargingstations()
    for charging in CHARGING:
        result = insidecircle(charging[0], charging[1],charging[2], X, Y)
        if result:
            return charging[3]
    return False

def insidecircle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2