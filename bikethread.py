"""
A thread that simulates user and bikes
"""
from threading import Thread
import time

class BikeThread(Thread):
    """
    bike thread class where it runs creates a thread and runs an update on bikes
    """
    def __init__(self, bikes, users):
        """
        thread constructor
        """
        Thread.__init__(self)
        self.bikelist = bikes
        self.userlist = users
        self._running = True

    def run(self):
        """
        starts a thread
        """
        while self._running:
            # print(f'running update thread {self.getName()}')
            print("-------------------------------------")
            self.update_users()
            self.update_bikes()
            time.sleep(5) #pauses for 10seconds

    def terminate(self):
        """
        stops the thread
        """
        self._running = False

    def update_bikes(self):
        """
        runs the update_pos method on bikes where upptagen is true
        """
        for bike in self.bikelist:
            # print(bike.status)
            # print(bike._id)
            if bike.status == "available" and bike.battery <= 30:
                # print(f'Bike {bike._id} is {bike.status}: {bike.battery}%')
                bike.move_to_charging()
                bike.charging()
                bike.put_request()

            if bike.status == 'unavailable':
                # print("biketime")
                bike.update_pos()
                if bike.velocity == 0:
                    # print("stop!!!! BIKE!")
                    self.get_off_bike(bike._id)
                bike.put_request()

            elif bike.status == 'charging':
                bike.velocity = 0
                bike.charging()
                # bike.bike_print()
                bike.put_request()
                print(f'Bike {bike._id} is {bike.status}: {bike.battery}%')

            elif bike.status == 'service':
                # print("bike needs service")¨
                bike.service()
                bike.put_request()

    def update_users(self):
        """
        updates the user, runs the users decrease_wait function
        """
        # print("user update")
        for user in self.userlist:
            if user.bike is None:
                _id = user.decrease_wait()
                user.user_print()
                if _id is not None:
                    self.update_bike(_id)

    def update_bike(self, _id):
        """
        updates all bikes in bikelist
        """
        # update cykenln
        # print("bike update")
        for bike in self.bikelist:
            if bike._id == _id:
                bike.status = bike.statusarray[1]
                # bike.put_request()
                bike.bike_print()
                # print(bike._id)
                # print(bike.status)

    def get_off_bike(self, bike_id):
        """
        removes user from the bike
        """
        for user in self.userlist:
            if user.bike is not None and user.bike["id"] == bike_id:
                user.get_off_bike()
