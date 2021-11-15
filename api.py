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
        CITIES.append([float(row["X"]), float(row["Y"]), float(row["radius"])])
    print(CITIES)
    return json

def getParkingspaces():
    r = requests.get(f'{API_URL}parkingspaces')
    r.raise_for_status()
    json = r.json()
    for row in json:
        # print(json)
        PARKING.append([float(row["X"]), float(row["Y"]), float(row["radius"])])
    print(PARKING)

    return json

def getChargingstations():
    r = requests.get(f'{API_URL}chargingstations')
    r.raise_for_status()
    json = r.json()
    for row in json:
        CHARGING.append([float(row["X"]), float(row["Y"]), float(row["radius"])])
    print(CHARGING)
    return json

def areacheck(X, Y):
    #absolutbelopet av X & Y för att sedan se om de är mindre eller lika med området i city

    pass

def cityCheck(X, Y):
    if len(CITIES) == 0:
        getCityZones()
    # print(X)
    X = abs(X)
    # print(X)
    Y = abs(Y)
    for city in CITIES:
        # print(city)
        cityX = abs(city[0])
        cityY = abs(city[1])
        cityR = city[2]
        # print(X)
        # print(cityX)
        # print(cityR)
        if cityX + cityR > X > cityX and cityY + cityR > Y > cityY:
            return True
    return False

def parkingCheck(X, Y):
    if len(PARKING) == 0:
        getParkingspaces()
    X = abs(X)
    Y = abs(Y)
    for parking in PARKING:
        parkingX = abs(parking[0])
        parkingY = abs(parking[1])
        parkingR = parking[2]
        print(parkingR)
        if parkingX > X and parkingY > Y:
            return True
    return False

def chargingCheck(X, Y):
    if len(CHARGING) == 0:
        getChargingstations()
    X = abs(X)
    Y = abs(Y)
    for charging in CHARGING:
        chargingX = abs(charging[0])
        chargingY = abs(charging[1])
        charingR = charging[2]
        print(charingR)
        if chargingX > X and chargingY > Y:
            return True
    return False
