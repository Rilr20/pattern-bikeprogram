"""
unittest test
"""

import unittest
from unittest import mock
import api
from bike import Bike

class TestAPI(unittest.TestCase):
    """Unittest API submodule"""
    def test_init(self):
        """init test"""
        self.assertEqual(api.PORT, "8000")
        self.assertEqual(api.API_URL, f'http://localhost:{api.PORT}/sparkapi/v1/')
        self.assertIsNotNone(api.CITIES)

    def test_cityCheck(self):
        """
        tests the citycheck function
        """
        testArray = [[0.025, 0.035, 1], [1000, 0, False]]
        for item in testArray:
            # print(item)
            res = api.cityCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

    def test_parkingCheck(self):
        """
        testing the parkingcheck function
        """
        testArray = [[-0.025,-0.025, 1], [1000, 0, False]]
        for item in testArray:
            # print(item)
            res = api.parkingCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

    def test_chargingCheck(self):
        """
        testing the chargingcheck function
        """
        testArray = [[0.025,0.025, 1], [1000, 0, False]]
        for item in testArray:
            # print(item)
            res = api.chargingCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

class TestBike(unittest.TestCase):
    """
    unittest Bike class
    """
    def test_opposite(self):
        """
        testing the opposite function so it returns the opposite direction
        """
        testbike = Bike(0,0,0, "available")
        directions = ["n", "ne", "e", "se", "nw", "w", "sw", "s"]
        rev = ["s", "sw", "w", "nw", "se", "e", "ne", "n"]
        # print(len(directions))
        for i in  range(0, len(directions)):
            testbike.prevdirection = directions[i]
            new = testbike.opposite()
            self.assertEqual(new, rev[i])

    def test_moveBike(self):
        """
        testing the movebike function
        """
        testbike = Bike(0,0,0, "available")
        testbike.velocity = 1
        directions = ["n", "ne", "e", "se", "nw", "w", "sw", "s"]
        expected = [(0,1), (0.5,0.5), (1,0), (0.5,-0.5), (-0.5,0.5), (-1,0), (-0.5,-0.5), (0,-1)]
        for i in range(0, len(directions)):
            # print(directions[i])
            testbike.moveBike(directions[i])
            restuple = (testbike.X, testbike.Y)
            self.assertEqual(expected[i], restuple)
            testbike.X = 0
            testbike.Y = 0

    # def test_getDirection(self):
    #     testbike = Bike(0,0,0)
    #     pass

    def test_sercice(self):
        testbike = Bike(0,0,0, "available")
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
