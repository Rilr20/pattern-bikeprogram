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
    # directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
    directions = ["n", "ne", "e", "se", "nw", "w", "sw", "s"]
    statusarray = ['available', 'unavailable','service', 'charging']
    def __init__(self, _id,  X, Y, status):
        self._id = _id
        self.X = float(X)
        self.Y = float(Y)
        self.status = status
        self.battery = 100
        self.velocity = 0
        self.customer = None
        self.timesrun = 0
        self.servicecount = 0
        self.prevdirection = self.directions[random.randint(0, len(self.directions)-1)]
    
    def updatePos(self):
        self.updateVelocity(self.velocity)
        # funcion that adds velocity to X & Y depending on direction
        # self.X = self.X + self.velocity
        # self.Y = self.Y + self.velocity
        direction = self.getDirection()
        self.moveBike(direction)
        checklist = api.areaCheck(self.X, self.Y)
        self.battery = self.battery - 1

    def moveToCity(self, cityval):
        if cityval == False:
            rand = random.randint(0, len(api.CHARGING))
            city = api.CITIES[rand]
            self.X = city[0]
            self.Y = city[1]

    def updateVelocity(self, velocity):
        for i in range(len(self.speeds)):
            if self.timesrun >= 3 and velocity == self.speeds[i] and self.battery > 0:
                self.velocity = self.speeds[i-1]
                self.timesrun = self.timesrun + 1
                if self.speeds[i-1] == 0:
                    self.timesrun = 0
                    #destination reached!
                    # setting to available again
                    self.status = self.statusarray[0]
                break
            elif velocity == self.speeds[i] and self.battery > 0:
                self.velocity = self.speeds[i+1]
                self.timesrun = self.timesrun + 1
                break
            if self.battery == 0: 
                self.velocity = 0
                self.status = self.statusarray[2]

    def putRequest(self):
        api.putBikes(self._id, self.X, self.Y, self.status, self.battery, self.velocity)

    def bikeprint(self):
        print(f'Bike {self._id} status: {self.status}, battery: {self.battery}, velocity: {self.velocity}, current position ({self.X}, {self.Y})')
    
    def charging(self):
        """
        starts charging bike if its inside a chargingstation
        otherwise its marked as available
        """
        station = api.chargingCheck(self.X, self.Y)
        if self.battery < 100 and station != False:
            self.battery = self.battery + 1
        else:
            self.status == "available"
    def moveToCharging(self):
        """
        move bike to random charging station
        """
        rand = random.randint(0, len(api.CHARGING))
        station = api.CHARGING[rand]
        self.X = station[0]
        self.Y = station[1]

    def removeFromCharging(self):
        """
        removes bike from charging station and places it inside random city
        """
        rand = random.randint(0, len(api.CITIES))
        city = api.CITIES[rand]
        self.X = city[0]
        self.Y = city[1]

    def opposite(self):
        """
        returns the opposite direction to previous
        """
        index = self.directions.index(self.prevdirection)
        index += 1
        return self.directions[-index]

    def moveBike(self, direction):
        """
        case switch for moving bike
        """
        if direction == "n":
            # (0,Y)
            self.Y += round(self.velocity, 6)
            pass
        elif direction == "ne":
            # (Y/2,X/2)
            self.X += round(self.velocity/2, 6)
            self.Y += round(self.velocity/2, 6)
            pass
        elif direction == "e":
            # (X,0)
            self.X += round(self.velocity, 6)
            pass
        elif direction == "se":
            # (Y/2,-X/2)
            self.X += round(self.velocity/2, 6)
            self.Y -= round(self.velocity/2, 6)
            pass
        elif direction == "nw":
            # (-Y/2,X/2)
            self.X -= round(self.velocity/2, 6)
            self.Y += round(self.velocity/2, 6)
            pass
        elif direction == "w":
            # (-X,0)
            self.X -= round(self.velocity, 6)
            pass
        elif direction == "sw":
            # (-Y/2,-X/2)
            self.X -= round(self.velocity/2, 6)
            self.Y -= round(self.velocity/2, 6)
            pass
        elif direction == "s":
            # (0,-Y)
            self.Y -= round(self.velocity, 6)
            pass

    def getDirection(self):
        """
        randomizes a new direction if direction is opposite of previous randomize new one
        """
        newdirection = self.directions[random.randint(0, len(self.directions)-1)]
        if newdirection != self.opposite():
            return newdirection
        else:
            return self.getDirection()

    def service(self):
        """
        bike is under service
        """
        if self.servicecount < 10:
            self.status = self.statusarray[2]
            self.servicecount += 1
        else:
            self.servicecount = 0
            self.status = self.statusarray[0]
