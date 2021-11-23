"""
Bike Class
"""
import random
import api
class Bike():
    """
    bike class 
    """
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
    directions = ["n", "ne", "e", "se", "nw", "w", "sw", "s"]
    statusarray = ['available', 'unavailable','service', 'charging']
    def __init__(self, _id,  X, Y, battery, status):
        """
        constructor for bike.
        """
        self._id = _id
        self.X = float(X)
        self.Y = float(Y)
        self.status = status
        self.battery = int(battery)
        self.velocity = 0
        self.timesrun = 0
        self.triplength = random.randint(len(self.statusarray)-1, 12)
        self.servicecount = 0
        self.prevdirection = self.directions[random.randint(0, len(self.directions)-1)]
    
    def updatePos(self):
        """
        updates the velocity; increasing or decreasing it
        updates the direction it will go next
        moves the bike; checks if inside the circle
        decreases the battery by 1 unit
        """
        #updates the speed
        self.updateVelocity()
        #get new direction
        direction = self.getDirection()
        #move the bike
        self.moveBike(direction)
        #checks if inside the city
        checklist = api.areaCheck(self.X, self.Y)
        self.moveToCity(checklist[0])
        #decrease battery
        if self.velocity > 0:
            self.battery = self.battery - 1

    def moveToCity(self, cityval):
        """
        checks if the value in cityval is false; move to center of random city
        """
        if cityval == False:
            rand = random.randint(0, len(api.CITIES)-1)
            city = api.CITIES[rand]
            self.X = city[0]
            self.Y = city[1]

    def updateVelocity(self):
        """
        increases velocity until triplenght equals times run then it slows down
        """
        if self.battery == 0:
            self.velocity = 0
            self.status = self.statusarray[2]
        elif self.battery > 1:
            index = self.speeds.index(self.velocity)
            if self.timesrun < self.triplength:
                self.increaseVelocity(index)
            else:
                self.decreaseVelocity(index)

    def increaseVelocity(self, index):
        """
        increases the velocity
        """
        self.timesrun += 1
        try:
            #try to increase velocity
            self.velocity = self.speeds[index+1]
        except:
            #max velocity reached!
            self.velocity = self.speeds[3]
            #keep current velocity (max speed reached)
            pass
        #sets speed to 10km/h if inside centrum
        self.inCentrum()

    def decreaseVelocity(self, index):
        """
        decreases the velocity
        """
        self.timesrun += 1
        if index - 1 != -1:
            #decreases velocity if index isn't -1
            self.velocity = self.speeds[index-1]
            #sets speed to 10km/h if inside centrum
            self.inCentrum()
        else:
            # destination reached!
            self.velocity = self.speeds[0]
            # setting to available again
            self.status = self.statusarray[0]

    def inCentrum(self):
        """
        if bike is in centrum set velocity to slower one
        """
        for city in api.CITIES:
            res = api.insidecircle(city[0], city[1], float(city[2])/10, self.X, self.Y)
            if res != False:
                # print("--------------I AM IN CENTRUM--------------")
                self.velocity = self.speeds[1]

    def putRequest(self):
        """
        sends put request to api to update bike
        """
        api.putBikes(self._id, self.X, self.Y, self.status, self.battery, self.velocity)

    def bikeprint(self):
        """
        prints information about the bikes current situation
        """
        print(f'Bike: {self._id} status: {self.status}, battery: {self.battery}, velocity: {self.velocity}, current position ({self.X}, {self.Y})')

    def charging(self):
        """
        starts charging bike if its inside a chargingstation
        otherwise its marked as available
        """
        station = api.chargingCheck(self.X, self.Y)
        if self.battery < 100 and station != False:
            if self.status != "charging":
                self.status = self.statusarray[3]
            self.battery = self.battery + 1
        else:
            if self.battery == 100:
                self.removeFromCharging()
            self.status = "available"

    def moveToCharging(self):
        """
        move bike to random charging station
        """
        rand = random.randint(0, len(api.CHARGING)-1)
        # print(rand)
        station = api.CHARGING[rand]
        self.X = station[0]
        self.Y = station[1]

    def removeFromCharging(self):
        """
        removes bike from charging station and places it inside random city
        """
        rand = random.randint(0, len(api.CITIES)-1)
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
        case switch for moving bike in all cardinal directions
        """
        if direction == "n":
            # (0,Y)
            self.Y += round(self.velocity, 6)
        elif direction == "ne":
            # (Y/2,X/2)
            self.X += round(self.velocity/2, 6)
            self.Y += round(self.velocity/2, 6)
        elif direction == "e":
            # (X,0)
            self.X += round(self.velocity, 6)
        elif direction == "se":
            # (Y/2,-X/2)
            self.X += round(self.velocity/2, 6)
            self.Y -= round(self.velocity/2, 6)
        elif direction == "nw":
            # (-Y/2,X/2)
            self.X -= round(self.velocity/2, 6)
            self.Y += round(self.velocity/2, 6)
        elif direction == "w":
            # (-X,0)
            self.X -= round(self.velocity, 6)
        elif direction == "sw":
            # (-Y/2,-X/2)
            self.X -= round(self.velocity/2, 6)
            self.Y -= round(self.velocity/2, 6)
        elif direction == "s":
            # (0,-Y)
            self.Y -= round(self.velocity, 6)

    def getDirection(self):
        """
        randomizes a new direction if direction is opposite of previous randomize new one
        """
        newdirection = self.directions[random.randint(0, len(self.directions)-1)]
        if newdirection != self.opposite():
            return newdirection
        return self.getDirection()

    def service(self):
        """
        bike is under service
        """
        if self.servicecount > 0:
            self.status = self.statusarray[2]
            self.servicecount -= 1
        elif self.servicecount == 0:
            # self.servicecount = 0
            self.status = self.statusarray[0]
