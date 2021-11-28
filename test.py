"""
unittest test
"""

# import unittest
# from unittest import mock
from unittest.case import TestCase
import api
import main
from bike import Bike
from user import User

class TestAPI(TestCase):
    """Unittest API submodule"""
    def test_init(self):
        """init test"""
        self.assertEqual(api.PORT, "8000")
        self.assertEqual(api.API_URL, f'http://localhost:{api.PORT}/sparkapi/v1/')
        self.assertIsNotNone(api.CITIES)

    def test_city_check(self):
        """
        tests the citycheck function
        """
        test_array = [[0.025, 0.035, 1], [1000, 0, False]]
        for item in test_array:
            # print(item)
            res = api.cityCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

    def test_parking_check(self):
        """
        testing the parkingcheck function
        """
        test_array = [[-0.025,-0.025, 1], [1000, 0, False]]
        for item in test_array:
            # print(item)
            res = api.parkingCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

    def test_charging_check(self):
        """
        testing the chargingcheck function
        """
        test_array = [[0.025,0.025, 1], [1000, 0, False]]
        for item in test_array:
            # print(item)
            res = api.chargingCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

    def test_inside_circle(self):
        """
        testing to see if point is inside a circle
        """
        circle_variable = (0,0,5)
        point = [(0,0),(-1,-0.5)]
        for item in point:
            result = api.insidecircle(
                    circle_variable[0],
                    circle_variable[1],
                    circle_variable[2],
                    item[0],
                    item[1]
                )
            self.assertEqual(result,True)
            result = api.insidecircle(10, 10,circle_variable[2],item[0],item[1])
            self.assertEqual(result,False)

class TestBike(TestCase):
    """
    unittest Bike class
    """
    def test_opposite(self):
        """
        testing the opposite function so it returns the opposite direction
        """
        testbike = Bike(0,0,0,100, "available")
        directions = ["n", "ne", "e", "se", "nw", "w", "sw", "s"]
        rev = ["s", "sw", "w", "nw", "se", "e", "ne", "n"]
        # print(len(directions))
        # for i in  range(0, len(directions)):
        count = 0
        for i in directions:
            testbike.prevdirection = i
            new = testbike.opposite()
            self.assertEqual(new, rev[count])
            count += 1

    def test_move_bike(self):
        """
        testing the movebike function
        """
        testbike = Bike(0,0,0,100, "available")
        testbike.velocity = 1
        directions = ["n", "ne", "e", "se", "nw", "w", "sw", "s"]
        expected = [(0,1), (0.5,0.5), (1,0), (0.5,-0.5), (-0.5,0.5), (-1,0), (-0.5,-0.5), (0,-1)]
        count = 0
        # for i in range(0, len(directions)):
        for i in directions:
            # print(directions[i])
            testbike.moveBike(i)
            restuple = (testbike.X, testbike.Y)
            self.assertEqual(expected[count], restuple)
            testbike.X = 0
            testbike.Y = 0
            count += 1

    def test_move_to_city(self):
        """
        test to move bikes to city if outside border
        """
        testbike = Bike(1000,1000,0,100, "available")
        testbike.moveToCity(False)
        self.assertEqual(testbike.X,0)
        self.assertEqual(testbike.Y,0)

    def test_increase_velocity(self):
        """
        test to increase velocity
        """
        speeds = [0, 0.001383, 0.002973, 0.004464]
        expected = [0.001383, 0.002973, 0.004464, 0.004464]
        testbike = Bike(10,10,0,100, "available")
        count = 0
        for i in speeds:
            index = speeds.index(i)
            testbike.increaseVelocity(index)
            # print(testbike.velocity)
            # print(expected[count])
            self.assertEqual(testbike.velocity, expected[count])
            count += 1

    def test_decrease_velocity(self):
        """
        test to decrease velocity
        """
        speeds = [0, 0.001383, 0.002973, 0.004464]
        expected = [0.002973, 0.001383, 0,0]
        testbike = Bike(10,10,0.004464,100, "unavailable")
        count = 0
        for i in reversed(speeds):
            index = speeds.index(i)
            testbike.decreaseVelocity(index)
            self.assertEqual(testbike.velocity, expected[count])
            count += 1
        self.assertEqual(testbike.status, "available")

    def test_in_centrum(self):
        """
        testing velocity changes while in centrum of city
        """
        testbike = Bike(0,0,0,100,"available")
        #max speed increasing should become second slowest
        testbike.increaseVelocity(3)
        self.assertEqual(testbike.velocity, 0.001383)
        #max speed decreaseing hould become second slowest
        testbike.decreaseVelocity(3)
        self.assertEqual(testbike.velocity, 0.001383)
        #slowest speed should stop in centrum
        testbike.decreaseVelocity(0)
        self.assertEqual(testbike.velocity, 0)

    def test_move_to_charging(self):
        """
        testing move bike to a charging station
        """
        testbike = Bike(0,0,0,10,"available")
        testbike.moveToCharging()
        self.assertEqual(testbike.X, 0.025)
        self.assertEqual(testbike.Y, 0.025)

    def test_remove_from_charging(self):
        """
        testing removing bike from charging station
        """
        testbike = Bike(0,0,0,10,"available")
        testbike.removeFromCharging()
        self.assertEqual(testbike.X, 0)
        self.assertEqual(testbike.Y, 0)

    def test_charging(self):
        """
        testing charging bike
        """
        testbike = Bike(0,0.025,0.025,9,"available")
        count = 10
        testbike.charging()
        self.assertEqual(testbike.status, "charging")
        while count < 100:
            count += 1
            testbike.charging()
            self.assertEqual(testbike.battery, count)
        testbike.charging()
        self.assertEqual(testbike.status, "available")

    def test_charging_outside_of_station(self):
        """
        testing what happens when bike charge outside of charging station
        """
        testbike = Bike(0,0,0,9,"charging")
        testbike.charging()
        self.assertEqual(testbike.status, "available")

    def test_sercice(self):
        """
        testing the service function
        """
        testbike = Bike(0,0,0,100, "available")
        testlength = 10
        testbike.servicecount = testlength

        for i in range(0, testlength):
            # print(testlength-i-1)
            # print(testbike.servicecount)
            self.assertEqual(testlength-i, testbike.servicecount)
            testbike.service()
            self.assertEqual("service", testbike.status)
        testbike.service()
        self.assertEqual("available", testbike.status)

class TestUser(TestCase):
    """
    testing the user class
    """
    def test_decreasewait(self):
        """
        testing decrease wait function on user
        """
        testuser = User(0)
        start = 10
        testuser.wait = start
        self.assertEqual(testuser.bike, None)
        for i in range(start):
            self.assertEqual(testuser.wait, start-i)
            testuser.decreasewait()

class TestMain(TestCase):
    """
    testing the main file
    """
    def test_create_users(self):
        """
        testing create user function
        """
        length = [1, 5, 10, 0]
        for i in length:
            users = main.create_users(i)
            self.assertEqual(len(users), i)
