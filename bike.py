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
    def __init__(self, _id,  x_pos, y_pos, battery, status):
        """
        constructor for bike.
        """
        self._id = _id
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.status = status
        self.battery = int(battery)
        self.velocity = 0
        self.timesrun = 0
        self.triplength = random.randint(len(self.statusarray)-1, 12)
        self.servicecount = 0
        self.prevdirection = self.directions[random.randint(0, len(self.directions)-1)]

    def update_pos(self):
        """
        updates the velocity; increasing or decreasing it
        updates the direction it will go next
        moves the bike; checks if inside the circle
        decreases the battery by 1 unit
        """
        #updates the speed
        self.update_velocity()
        #get new direction
        direction = self.get_direction()
        #move the bike
        self.move_bike(direction)
        #checks if inside the city
        check_list = api.area_check(self.x_pos, self.y_pos)
        self.move_to_city(check_list[0])
        #decrease battery
        if self.velocity > 0:
            self.battery = self.battery - 1

    def move_to_city(self, cityval):
        """
        checks if the value in cityval is false; move to center of random city
        """
        if cityval is False:
            rand = random.randint(0, len(api.CITIES)-1)
            city = api.CITIES[rand]
            self.x_pos = city[0]
            self.y_pos = city[1]

    def update_velocity(self):
        """
        increases velocity until triplenght equals times run then it slows down
        """
        if self.battery == 0:
            self.velocity = 0
            self.status = self.statusarray[2]
        elif self.battery > 1:
            index = self.speeds.index(self.velocity)
            if self.timesrun < self.triplength:
                self.increase_velocity(index)
            else:
                self.decrease_velocity(index)

    def increase_velocity(self, index):
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
        #sets speed to 10km/h if inside centrum
        self.in_centrum()

    def decrease_velocity(self, index):
        """
        decreases the velocity
        """
        self.timesrun += 1
        if index - 1 != -1:
            #decreases velocity if index isn't -1
            self.velocity = self.speeds[index-1]
            #sets speed to 10km/h if inside centrum
            self.in_centrum()
        else:
            # destination reached!
            self.velocity = self.speeds[0]
            # setting to available again
            self.status = self.statusarray[0]

    def in_centrum(self):
        """
        if bike is in centrum set velocity to slower one
        """
        for city in api.CITIES:
            res = api.inside_circle(city[0], city[1], float(city[2])/10, self.x_pos, self.y_pos)
            if res is not False:
                # print("--------------I AM IN CENTRUM--------------")
                self.velocity = self.speeds[1]

    def put_request(self):
        """
        sends put request to api to update bike
        """
        api.put_bikes(self._id, self.x_pos, self.y_pos, self.status, self.battery, self.velocity)

    def bike_print(self):
        """
        prints information about the bikes current situation
        """
        print(f'Bike: {self._id} \
                status: {self.status}, \
                battery: {self.battery}, \
                velocity: {self.velocity}, \
                current position ({self.x_pos}, {self.y_pos})')

    def charging(self):
        """
        starts charging bike if its inside a chargingstation
        otherwise its marked as available
        """
        station = api.charging_check(self.x_pos, self.y_pos)
        if self.battery < 100 and station is not False:
            if self.status != "charging":
                self.status = self.statusarray[3]
            self.battery = self.battery + 1
        else:
            if self.battery == 100:
                self.remove_from_charging()
            self.status = "available"

    def move_to_charging(self):
        """
        move bike to random charging station
        """
        rand = random.randint(0, len(api.CHARGING)-1)
        # print(rand)
        station = api.CHARGING[rand]
        self.x_pos = station[0]
        self.y_pos = station[1]

    def remove_from_charging(self):
        """
        removes bike from charging station and places it inside random city
        """
        rand = random.randint(0, len(api.CITIES)-1)
        city = api.CITIES[rand]
        self.x_pos = city[0]
        self.y_pos = city[1]

    def opposite(self):
        """
        returns the opposite direction to previous
        """
        index = self.directions.index(self.prevdirection)
        index += 1
        return self.directions[-index]

    def move_bike(self, direction):
        """
        moves the bike in all cardinal directions
        """
        velocity_list = [
                (0, self.velocity), #n
                (self.velocity/2, self.velocity/2), #ne
                (self.velocity, 0), #e
                (self.velocity/2, -(self.velocity/2)), #se
                (-(self.velocity/2), self.velocity/2), #nw
                (-(self.velocity), 0), #w
                (-(self.velocity/2), -(self.velocity/2)), #sw
                (0, -(self.velocity)) #s
            ]
        index = self.directions.index(direction)
        new_x = velocity_list[index][0]
        new_y = velocity_list[index][1]
        self.x_pos = round(self.x_pos + new_x, 6)
        self.y_pos = round(self.y_pos + new_y, 6)

    def get_direction(self):
        """
        randomizes a new direction if direction is opposite of previous randomize new one
        """
        newdirection = self.directions[random.randint(0, len(self.directions)-1)]
        if newdirection != self.opposite():
            return newdirection
        return self.get_direction()

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
