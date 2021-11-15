"""
Bike Class
"""
import api

class Bike():
    speeds = [0, 0.250, 0.500, 0.750]
    directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
    statusarray = ['available', 'unavailable','service', 'charging']
    def __init__(self, _id,  X, Y):
        self._id = _id
        self.X = float(X)
        self.Y = float(Y)
        self.status = self.statusarray[0]
        self.battery = 100
        self.velocity = 0
        self.customer = None
        self.timesrun = 0
        self.prevdirection = None
    
    def updatePos(self):
        self.updateVelocity(self.velocity)
        self.X = self.X + self.velocity
        self.Y = self.Y + self.velocity
        self.battery = self.battery - 1
        #gör api request
    def updateVelocity(self, velocity):
        for i in range(len(self.speeds)):
            # print(i)
            # print(self.timesrun)
            if self.timesrun >= 3 and velocity == self.speeds[i] and self.battery > 0:
                self.velocity = self.speeds[i-1]
                self.timesrun = self.timesrun + 1
                if self.speeds[i-1] == 0:
                    self.timesrun = 0
                    #destination reached?
                # print(self.timesrun)
                # print(self.velocity)
                # print("self.velocity")
                break

            elif velocity == self.speeds[i] and self.battery > 0:
                self.velocity = self.speeds[i+1]
                self.timesrun = self.timesrun + 1
                # print(self.velocity)
                # print("self.velocity")
                break
            if self.battery == 0: 
                self.velocity = 0
                self.status = self.statusarray[2]
    def putRequest(self):
        api.putBikes(self._id, self.X, self.Y, self.battery, self.velocity)

    def bikeprint(self):
        print(f'Bike {self._id} status: {self.status}, battery: {self.battery}, velocity: {self.velocity}, current position ({self.X}, {self.Y})')
    
    def charging(self):
        if self.battery < 100:
            self.battery = self.battery + 1
        else:
            self.status == "tillgänglig"
