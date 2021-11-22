"""
Main file
"""
import requests
from bike import Bike
from user import User
from bikethread import bikeThread
import api
import time

#TODO: ta ut api:et och flytta till en egen modul
#TODO: kolla vilka routes som behövs.
# skapa order?
# skicka till bikehistory
# hämta användare
#
#TODO: vilka kommandon behövs?
# starta användare thread
#   påbörja resa
#   avsluta resa
#   få faktura
#
# slump på användaren så att kanske 50% av användarna använder cyklarna samtidigt
# # stoppa användare thread
# cykel & användar thread startas samditigt. 
# gör en check om cykel är inom parkerings området / laddningsområdet.
# gör en check om cykel är inom centrumzonen
# gör en check om cykel är inom stadszonen
#TODO: Nattsimulering? dvs. de flyttas till laddstationer
#


# def bikeinit():
    
#     print(BIKES)
def createBikes():
    # sends requests gets all bikes
    json = api.getBikes()
    bikearray = []
    # print(json[0])
    #uses the json data to create bike objects
    for i in range(0, len(json)):
        element = json[i]
        _id = element["id"]
        X = element["X"]
        Y = element["Y"]
        status = element["status"]
        battery = element["battery"]
        # print(status)
        bike = Bike(_id, X, Y, battery, status)
        bikearray.append(bike)
    print("done creating bikes")
    return bikearray

def createUsers():
    userlist = []
    for i in range(0, 1):
        user = User(i)
        userlist.append(user)
    print("done creating users")
    return userlist

BIKES = createBikes()
USERS = createUsers()
api.getCityZones()
api.getParkingspaces()
api.getChargingstations()
def helptext():
    #simulate users?
    print("----------------Bike Program----------------")
    print("help:        Get Info About Commands")
    print("start:       Starts the bike thread")
    print("stop:        Stops the bike thread")
    print("once:        Does the simulation one time")
    print("charge:      Charges all bikes")
    print("q | quit:    Exit Program")
def main():
    helptext()
    simulation = bikeThread(BIKES, USERS)
    simulation.setName('simulation thread')
    running = False
    while True:
        choice = input("--> ")
        choice = choice.lower()
        if choice == "help":
            #writes a help text 
            helptext()
        elif choice == "start":
            #starts theg simulation 
            try:
                simulation.start()
                running = True
            except:
                if running == False:
                    simulation = bikeThread(BIKES, USERS)
                    simulation.start()
                    running = True
        elif choice == "stop":
            #stops the simulation
            try:
                simulation.terminate()
                print("bye thread!")
                running = False
            except:
                print("thread is not running run start command")
        elif choice == "once":
            #runs the simulation once
            try:
                simulation.start()
            except:
                simulation = bikeThread(BIKES, USERS)
                simulation.start()
            simulation.terminate()
            print("stopped")
        elif choice == "charge":
            #sends all bikes to chargingstations
            try:
                simulation.terminate()
            except:
                pass
            for bike in BIKES:
                bike.moveToCharging()
                bike.putRequest()
            print("Bikes are not charging")
        elif choice == "test":
            user = User(1)
            user.getOnBike()
        elif choice == "q" or choice == "quit":
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
