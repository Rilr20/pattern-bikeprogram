"""
unittest test
"""

import unittest
from unittest import mock
import api

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
        testArray = [[0.025, 0.035, True], [-0.025,-0.035, True], [10, 0, False], [-10,0, False]]
        for item in testArray:
            # print(item)
            res = api.cityCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

    def test_parkingCheck(self):
        """
        testing the parkingcheck function
        """
        testArray = [[0.00025, 0.00035, True], [-0.00025,-0.00035, True], [10, 0, False], [-10,0, False]]
        for item in testArray:
            # print(item)
            res = api.parkingCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])

    def test_chargingCheck(self):
        """
        testing the chargingcheck function
        """
        testArray = [[0.00025, 0.00035, True], [-0.00025,-0.00035, True], [10, 0, False], [-10,0, False]]
        for item in testArray:
            # print(item)
            res = api.chargingCheck(item[0], item[1])
            # print(res)
            self.assertEqual(res, item[2])
