"""
Main file
"""
from bike import Bike
from user import User
from bikethread import BikeThread
import api

api.PORT = input("Which port is used? ")
url = input("what is the url used? http://")
if url is not None:
    api.API_URL = f'http://{url}:{api.PORT}/sparkapi/v1/'
print(api.API_URL + " is now used")

def create_bikes():
    """
    Creates bikes with json from get request
    """
    # sends requests gets all bikes
    json = api.get_bikes()
    bikearray = []
    #uses the json data to create bike objects
    for element in json:
        _id = element["id"]
        x_pos = element["X"]
        y_pos = element["Y"]
        status = element["status"]
        battery = element["battery"]
        # print(status)
        bike = Bike(_id, x_pos, y_pos, battery, status)
        bikearray.append(bike)
    return bikearray

def create_users(length):
    """
    creates users
    """
    userlist = []
    for i in range(0, length):
        user = User(i)
        userlist.append(user)
    return userlist

BIKES = create_bikes()
print("done creating bikes")
USERS = create_users(1000)
print("done creating users")
api.get_city_zones()
api.get_parkingspaces()
api.get_chargingstations()
def helptext():
    """
    writes out the commands you can use
    """
    #simulate users?
    print("----------------Bike Program----------------")
    print("help:        Get Info About Commands")
    print("start:       Starts the bike thread")
    print("stop:        Stops the bike thread")
    print("once:        Does the simulation one time")
    print("charge:      Charges all bikes")
    print("q | quit:    Exit Program")

def start_thread(running, simulation):
    """
    starts the bike thread
    """
    try:
        simulation.start()
    except:
        if running is False:
            simulation = BikeThread(BIKES, USERS)
            simulation.start()
            simulation.setName('simulation thread')
    return simulation
def create_thread(bikes, users):
    """
    creates a bikethread
    """
    simulation = BikeThread(bikes, users)
    return simulation

def main():
    """
    main function
    """
    helptext()
    simulation = create_thread(BIKES, USERS)
    simulation.setName('simulation thread')
    running = False
    while True:
        choice = input("--> ")
        choice = choice.lower()
        if choice == "help":
            #writes a help text
            helptext()
        elif choice == "start":
            #starts the simulation
            simulation = start_thread(running, simulation)
            running = True
        elif choice == "stop":
            #stops the simulation
            try:
                simulation.terminate()
                simulation.join()
                print("bye thread!")
                running = False
            except:
                print("thread is not running run start command")
        elif choice == "once":
            #runs the simulation once
            simulation = start_thread(running, simulation)
            simulation.terminate()
            simulation.join()
            print("stopped")
        elif choice == "charge":
            #sends all bikes to chargingstations
            for bike in BIKES:
                bike.move_to_charging()
                bike.put_request()
            print("Bikes are not charging")
        elif choice in ("q", 'quit'):
            try:
                simulation.terminate()
                simulation.join()
            except:
                print("No thread to stop")
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
