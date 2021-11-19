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
        if len(bikes) > 0:
            print("new bike")
            bikeindex = random.randint(0, len(bikes)-1)
            self.bike = bikes[bikeindex]
            # self.bike["status"] = "unavailable"
            # print(self.bike)
            api.putBikes(self.bike["id"],self.bike["X"],self.bike["Y"],self.bike["status"],self.bike["battery"], self.bike["velocity"])
            return self.bike["id"]
        else: 
            print("no bike available")
            self.wait += 1
            return None
        # print(self.bike)
        # print(self.bike["status"])
        # print(self.bike["status"])
        # print(self.bike["id"])
        # pass

    def getOffbike(self):
        self.bike["status"] = "available"
        bikeinfo = api.getOneBike(self.bike["id"])
        print(bikeinfo)
        api.putBikes(self.bike["id"],bikeinfo["X"],bikeinfo["Y"],self.bike["status"],bikeinfo["battery"], bikeinfo["velocity"])
        self.bike = None
        self.wait = random.randint(5,20)
    
    def decreasewait(self):
        if self.wait > 0:
            self.wait -= 1
            return None
        elif self.wait == 0 and self.bike == None:
            return self.getOnBike()
        else:
            print(f'user {self._id} is on route')

    def userprint(self):
        print(f'User {self._id} Bike: {self.bike} Waittime: {self.wait}')