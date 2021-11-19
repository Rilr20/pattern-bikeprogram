from threading import Thread
import time

class userThread(Thread):
    def __init__(self, users):
        Thread.__init__(self)
        self.userlist = users
        self._running = True

    def run(self):
        """
        starts the thread
        """
        while self._running:
            self.update_users()
    
    def terminate(self):
        self._running = False
    
    def update_users(self):
        for user in self.userlist:
            print(user)
