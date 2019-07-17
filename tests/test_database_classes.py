import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from scripts.database_classes import ScienceDirectPaper as SDP

SCIENCE_DIRECT_TEST_URL = "https://www.sciencedirect.com/science/article/pii/S0167739X18316753"
SCIENCE_DIRECT_TEST_URL_RESULTS = {
        "Government regulations in cyber security: Framework, standards and recommendations": {
            "title": "Government regulations in cyber security: Framework, standards and recommendations",
            "authors": [
                {
                    "surname": "Srinivas",
                    "first_name": "Jangirala"
                },
                {
                    "surname": "Das",
                    "first_name": "Ashok Kumar"
                },
                {
                    "surname": "Kumar",
                    "first_name": "Neeraj"
                }
            ],
            "citations": "2"
        }
    }

class TestDatabaseClassesScienceDirect(unittest.TestCase):
    """This calss tests the functions for the ScienceDirect meta data gathering"""

    # def setUp(self):
    #     """Setting Up the driver for all tests listed below"""
    #     self.driver = webdriver.Firefox()


    # def tearDown(self):
    #     """Quits the Selenium driver after all tests have been run"""
    #     self.driver.quit()


    def test_get_title(self):
        """Tests for the ScienceDirect Database classes"""
        driver = webdriver.Firefox()
        driver.get(SCIENCE_DIRECT_TEST_URL)
        title = SDP.get_title(self, driver)
        self.assertEqual(title, "Government regulations in cyber security: Framework, standards and recommendations")
        driver.quit()

