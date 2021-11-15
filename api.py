"""
API functions
"""
import requests
PORT = "8000"
API_URL = f'http://localhost:{PORT}/sparkapi/v1/'
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
    return json

def getParkingspaces():
    r = requests.get(f'{API_URL}parkingspaces')
    r.raise_for_status()
    json = r.json()
    return json

def getChargingstations():
    r = requests.get(f'{API_URL}chargingstations')
    r.raise_for_status()
    json = r.json()
    return json