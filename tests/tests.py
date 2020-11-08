"""
Unit Tests
"""

import json
import os
from unittest import TestCase
from init import create_app
from services.movies_api_services import MoviesAPIServices


class Tests(TestCase):
    """
    Unit Tests
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up testing flask application
        """
        # create app
        cls.app = create_app(config='testing')

        # set test client
        cls.client = cls.app.test_client()

        # set up movies api service
        cls.movies_api_services_tester = MoviesAPIServices(api_base_url=cls.app.config['API_BASE_URL'],
                                                           movies_endpoint=cls.app.config['API_MOVIES_ENDPOINT'],
                                                           people_endpoint=cls.app.config['API_PEOPLE_ENDPOINT'],
                                                           results_limit=cls.app.config['API_MAX_RESULTS'])
        # read test data
        cls.test_movies = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/test_data/test_movies.json'))
        cls.test_characters = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/test_data/test_characters.json'))

    def test_display_movies(self):
        """
        Test display movies route
        """
        response = self.client.get('/movies/')
        # check response is correct
        self.assertEqual(response.status_code, 200)

    def test_get_movies(self):
        """
        Test get movies request
        """
        response = self.movies_api_services_tester.get_movies()
        # list not empty
        self.assertGreater(len(response), 0)
        # all results contain id and title
        self.assertTrue(['id', 'title'] in x.keys() for x in response)

    def test_get_characters(self):
        """
        Test get characters request
        """
        response = self.movies_api_services_tester.get_characters()
        # list not empty
        self.assertGreater(len(response), 0)
        # all results contain name and films
        self.assertTrue(['name', 'films'] in x.keys() for x in response)

    def test_get_movies_characters_combination(self):
        """
        Test get movies characters combination
        """
        results = self.movies_api_services_tester.get_movies_characters_combination(movies=self.test_movies,
                                                                                    characters=self.test_characters)

        # check film 1 has 2 characters associated
        self.assertEquals(len(results[0]['characters']), 2)

        # check character 1 is in films 1, 2, 3
        self.assertTrue(self.test_characters[0]['name'] in results[0]['characters'])
        self.assertTrue(self.test_characters[0]['name'] in results[1]['characters'])
        self.assertTrue(self.test_characters[0]['name'] in results[2]['characters'])

        # check film 2 has 1 character associated
        self.assertEquals(len(results[1]['characters']), 1)

        # check character 2 is in films 1 and 3
        self.assertTrue(self.test_characters[1]['name'] in results[0]['characters'])
        self.assertTrue(self.test_characters[1]['name'] in results[2]['characters'])

        # check film 3 has 3 characters associated
        self.assertEquals(len(results[2]['characters']), 3)

        # check characters 1, 2, 3 are in film 3
        self.assertTrue(self.test_characters[0]['name'] in results[2]['characters'])
        self.assertTrue(self.test_characters[1]['name'] in results[2]['characters'])
        self.assertTrue(self.test_characters[2]['name'] in results[2]['characters'])
