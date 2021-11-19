from threading import Thread
import time

class bikeThread(Thread):
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
            print("arg")
            # print(f'running update thread {self.getName()}')
            self.update_users()
            self.update_bikes()
            time.sleep(10) #pauses for 10seconds
    def terminate(self):
        """
        stops the thread
        """
        self._running = False

    def update_bikes(self):
        """
        runs the updatePos method on bikes where upptagen is true
        """
        for bike in self.bikelist:
            # print(bike.status)
            # print(bike._id)
            if bike.status == 'unavailable':
                # print("biketime")
                bike.updatePos()
                bike.bikeprint()
                bike.putRequest()
                if bike.velocity == 0:
                    print("stop!!!! BIKE!")
                    self.get_off_bike(bike._id)
            elif bike.status == 'charging':
                bike.velocity = 0
                bike.charging()
                bike.bikeprint()
                bike.putRequest
                print(f'{bike._id} updated')

    def update_users(self):
        for user in self.userlist:
            _id = user.decreasewait()
            user.userprint()
            if _id != None:
                self.update_bike(_id)
                pass
            

    def update_bike(self, _id):
        # update cykenln
        for bike in self.bikelist:
            if bike._id == _id:
                bike.status == bike.statusarray[1]
                # print(bike._id)
                # print(bike.status)

        # pass

    def get_off_bike(self, bike_id):
        for user in self.userlist:
            if user.bike != None and user.bike["id"] == bike_id:
                user.getOffbike()
