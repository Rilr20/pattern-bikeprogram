"""
user class
"""
import random
import api

class User():
    """
    class of a user
    """
    def __init__(self, _id):
        """
        users constructor
        """
        self._id = _id
        self.bike = None
        self.wait = random.randint(0, 35)

    def get_on_bike(self):
        """
        puts the user on a random available bike
        """
        # post request bikehistory
        _id = None
        bikes = api.available_bikes()
        if len(bikes) > 0:
            print("new bike")
            bikeindex = random.randint(0, len(bikes)-1)
            self.bike = bikes[bikeindex]
            # self.bike["status"] = "unavailable"
            # print(self.bike)
            api.put_bikes(self.bike["id"],
                self.bike["X"],
                self.bike["Y"],
                self.bike["status"],
                self.bike["battery"],
                self.bike["velocity"]
                )
            _id = self.bike["id"]
        else:
            print("no bike available")
            self.wait += 1
        return _id
        # print(self.bike)
        # print(self.bike["status"])
        # print(self.bike["status"])
        # print(self.bike["id"])

    def get_off_bike(self):
        """
        removes user from the bike, makes the bike available
        """
        self.bike["status"] = "available"
        bikeinfo = api.get_one_bike(self.bike["id"])
        print(bikeinfo)
        api.put_bikes(
                self.bike["id"],
                bikeinfo["X"],
                bikeinfo["Y"],
                self.bike["status"],
                bikeinfo["battery"],
                bikeinfo["velocity"]
                )
        self.bike = None
        self.wait = random.randint(5,85)

    def decrease_wait(self):
        """
        decrease wait time by 1 if 0 get on a bike
        """
        _id = None
        if self.wait > 0:
            self.wait -= 1
        elif self.wait == 0 and self.bike is None:
            _id = self.get_on_bike()
        else:
            print(f'user {self._id} is on route')
        return _id

    def user_print(self):
        """
        prints information about a user
        """
        print(f'User {self._id} Bike: {self.bike} Waittime: {self.wait}')
