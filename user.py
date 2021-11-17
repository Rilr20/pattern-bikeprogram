"""
user class
"""
import api
import random
import bikethread

class User():
    def __init__(self, _id):
        self._id = _id
        self.bike = None
        self.wait = random.randint(0, 10)
        
    def getOnBike(self):
        # post request bikehistory
        # fungerar inte då bikethread måste bli skapat som ett object
        
        bikes = api.availablebikes()
        bikeindex = random.randint(0, len(bikes)-1)
        self.bike = bikes[bikeindex]
        print(self.bike)
        print(self.bike["status"])
        self.bike["status"] = "unavailable"
        print(self.bike["status"])

        # print(self.bike["id"])
        api.putBikes(self.bike["id"],self.bike["X"],self.bike["Y"],self.bike["status"],self.bike["battery"], self.bike["velocity"])
        # pass

    def getOffbike(self):
        # put request bikehistory
        # put request bike status
        self.bike["status"] = "available"
        api.putBikes(self.bike["id"],self.bike["X"],self.bike["Y"],self.bike["status"],self.bike["battery"], self.bike["velocity"])
        self.bike = None
        self.wait = random.randint(5,20)
        # pass
    
    def decreasewait(self):
        if self.wait > 0:
            self.wait -= 1
        elif self.wait == 0 and self.bike == None:
            self.getOnBike()

    def userprint(self):
        print(f'User {self._id} Bike: {self.bike} Waittime: {self.wait}')