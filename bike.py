"""
Bike Class
"""
import api
import random
class Bike():
    # om de går max 30km/h så är det 500m/min som max hastighet
    # 0km/h
    # 10km/h = 166m/min
    # 20km/h = 333m/min
    # 30km/h = 500m/min
    # 0.5 i kordinater ungefär 50km
    # 0.25 i kordinater ungefär 27.80km
    # 0.0025 i kordinater ungefär 279,80m
    # 0.00025 i kordinater ungefär 29,80m
    # 0.00005 i kordinater ungefär 5m
    # 0.001383 ungefär 153m
    # 0.002973 ungefär 330m
    # 0.004464 ungefär 495m
    speeds = [0, 0.001383, 0.002973, 0.004464]
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
        # self.prevdirection = None
    
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
        station = api.chargingCheck(self.X, self.Y)
        if self.battery < 100 and station != False:
            self.battery = self.battery + 1
        else:
            self.status == "tillgänglig"
    def moveToCharging(self):
        rand = random.randint(0, len(api.CHARGING))
        station = api.CHARGING[rand]
        self.X = station[0]
        self.Y = station[1]

    def removeFromCharging(self):
        rand = random.randint(0, len(api.CITIES))
        city = api.CITIES[rand]
        self.X = city[0]
        self.Y = city[1]