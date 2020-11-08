"""
Movies API Services
"""

import json
import requests


class MoviesAPIServices:
    """
    Movies API Services
    """
    def __init__(self, api_base_url, movies_endpoint, people_endpoint, results_limit):
        """
        :param str api_base_url: API Base URL
        :param str movies_endpoint: API Movies Endpoint
        :param str people_endpoint: API People Endpoint
        :param int results_limit: Maximum results to return in API request
        """
        self.api_base_url = api_base_url
        self.movies_endpoint = movies_endpoint
        self.people_endpoint = people_endpoint
        self.results_limit = results_limit

    def get_movies(self):
        """
        Get movies from API

        :return: List of movies
        :rtype list
        """
        return self.__get_results(endpoint=self.movies_endpoint, fields=['id', 'title'])

    def get_characters(self):
        """
        Get characters from API

        :return: List of characters
        :rtype list
        """
        return self.__get_results(endpoint=self.people_endpoint, fields=['name', 'films'])

    def get_movies_characters_combination(self, movies, characters):
        """
        Get movies and their characters from API

        :param list movies: List of movies
        :param list characters: List of characters
        :return: List of movies - characters combination
        :rtype list
        """
        for character in characters:

            # get character's movies ids
            movie_ids = [x.split(self.movies_endpoint + '/')[1] for x in character['films']]

            # get movies matching character's movies ids
            matching_movies = list(filter(lambda item: item['id'] in movie_ids, movies))

            # if there are matching movies
            if matching_movies:

                # iterate movies
                for movie in matching_movies:

                    # if characters info already present, append new name
                    if 'characters' in movie:
                        movie['characters'].append(character['name'])

                    # if no character's info, initialize it with new name
                    else:
                        movie['characters'] = [character['name']]

        return movies

    def __make_api_request(self, endpoint, payload):
        """
        Make request to ghibliapi

        :param str endpoint: API Endpoint
        :param dict payload: Payload Dictionary
        :return: Dictionary indicating status and parsed API response if successful
        :rtype dict
        """
        # prepare response
        response = {
            'success': True,
            'data': None
        }

        try:
            # make request
            api_response = requests.request(method='GET',
                                            url='{}/{}'.format(self.api_base_url,
                                                               endpoint),
                                            params=payload)

            # if request successful
            if api_response.status_code == requests.codes['ok']:

                # parse response as json
                response['data'] = json.loads(api_response.text)

            # if request failed
            else:

                # set response as error
                response['success'] = False

        # if there's no response from API
        except ConnectionRefusedError:

            # set response as error
            response['success'] = False

        return response

    def __get_results(self, endpoint, fields):
        """
        Get API results list

        :param str endpoint: API Endpoint
        :param list fields: List of fields to retrieve
        :return: List of movies
        :rtype list
        """
        # set fields to return and maximum number of results
        payload = {'fields': ','.join(fields), 'limit': self.results_limit}

        # get api response
        response = self.__make_api_request(endpoint=endpoint, payload=payload)

        # return results if response successful or empty list otherwise
        return response['data'] if response['success'] else list()
