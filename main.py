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
    return bikearray

def createUsers():
    userlist = []
    for i in range(0, 1):
        user = User(i)
        userlist.append(user)
    print("done")
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
    print("init:        Gets bikes from API")
    print("start:       Starts the bike thread")
    print("stop:        Stops the bike thread")
    print("once:        Does the simulation one time")
    # print("url:         Changes the url")
    print("q | quit:    Exit Program")
def main():
    helptext()
    while True:
        choice = input("--> ")
        choice = choice.lower()
        if choice == "help":
            #funktion
            # print("test")
            helptext()
        # elif choice == "init":
        #     print("inits")
        #     bikeinit()
            # mythread.start()
            # print("sleepy time")
            # time.sleep(120)
            # print("sleepy time done")
        elif choice == "start":
            # print(len(BIKES))
            if len(BIKES) != 0:
                print("start thread")
                mythread = bikeThread(BIKES, USERS)
                mythread.setName('bike update thread')
                mythread.start()
            else:
                print("Bike program not initialized")
        elif choice == "stop":
            try:
                mythread.terminate()
                print("bye thread!")
            except:
                print("thread is not running run start command")
        elif choice == "once":
            if len(BIKES) > 0:
                mythread = bikeThread(BIKES, USERS)
                mythread.setName('bike update thread')
                mythread.start()
                mythread.terminate()
            else:
                print("Bike program not initialized")
        elif choice == "test":
            # json = api.getCityZones()
            # print(json)
            # json = api.getParkingspaces()
            # print(json)
            # json = api.getChargingstations()
            # print(json)
            # json  = api.availablebikes()
            # print(json)
            user = User(1)
            user.getOnBike()
        elif choice == "q" or choice == "quit":
            break
        else:
            print("Invalid command")

    # text = r.text
    # print(text)
    # print(dictionary)
    # bike.updateVelocity(0)
    # bike.updateVelocity(0.250)
    # bike.updateVelocity(0.500)
    # bike.updateVelocity(0.750)
    # bike.updateVelocity(0.500)
    # bike.updateVelocity(0.250)

if __name__ == "__main__":
    main()
