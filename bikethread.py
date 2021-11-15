from threading import Thread
import time

class bikeThread(Thread):
    """
    bike thread class where it runs creates a thread and runs an update on bikes
    """
    def __init__(self, bikes):
        """
        thread constructor 
        """
        Thread.__init__(self)
        self.bikelist = bikes
        self._running = True
    
    def run(self):
        """
        starts a thread
        """
        while self._running:
            # print(f'running update thread {self.getName()}')
            self.update_bikes()

            time.sleep(10) #pauses for 1 min
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
            if bike.status == 'unavailable':
                bike.updatePos()
                bike.bikeprint()
                bike.putRequest()
            elif bike.status == 'charging':
                bike.velocity = 0
                bike.charging()
                bike.bikeprint()
                bike.putRequest
                print(f'{bike._id} updated')

