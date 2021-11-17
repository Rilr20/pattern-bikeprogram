from threading import Thread
import time

class bikeThread(Thread):
    """
    bike thread class where it runs creates a thread and runs an update on bikes
    """
    def __init__(self, bikes):#,users):
        """
        thread constructor 
        """
        Thread.__init__(self)
        self.bikelist = bikes
        # self.userlist = userss
        self._running = True
    
    def run(self):
        """
        starts a thread
        """
        while self._running:
            print("arg")
            # print(f'running update thread {self.getName()}')
            # self.update_users()
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
            if bike.status == 'unavailable':
                # print("biketime")
                bike.updatePos()
                bike.bikeprint()
                bike.putRequest()
            elif bike.status == 'charging':
                bike.velocity = 0
                bike.charging()
                bike.bikeprint()
                bike.putRequest
                print(f'{bike._id} updated')

    def update_users(self):
        pass
        # for user in self.userlist:
        #     user.decreasewait()