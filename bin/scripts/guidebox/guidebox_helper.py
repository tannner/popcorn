import sys
import logging
import time

import guidebox_api


class GuideboxHelper:
    """Helper class for retrieving data from Guidebox API"""

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.guidebox = guidebox_api.GuideboxAPI()

    def get_all_movies(self, max_count=None):
        """
        Retrieve all movies from Guidebox or 'max_count' movies
        :param max_count: Max number of movies to fetch (optional)
        :return: List of movie dicts
        """
        max_desc = str(max_count)
        if max_count is None:
            max_count = sys.maxint
            max_desc = 'all'
        self.logger.info('Retrieving %s movies from Guidebox', max_desc)
        index = 0
        all_movies = []
        while index < max_count:
            response = self.guidebox.get_movies(index, 250)
            movies = response['results']
            for result in movies:
                movie = self.get_movie(result['id'])
                all_movies.append(movie)
            total_returned = movies['total_returned']
            total_results = movies['total_results']
            index += total_returned
            if index > total_results:
                break
            time.sleep(1)
        return all_movies

    def get_movie(self, movie_id):
        """
        Retrieve the given movie from Guidebox containing only
        application relevant movie data
        :param movie_id: Guidebox ID of movie to retrieve
        :return: Dict describing movie
        """
        movie_data = self.guidebox.get_movie(movie_id)
        genres = ",".join([genre['title'] for genre in movie_data['genres']])
        movie = {
            "id": movie_id,
            "title": movie_data['title'],
            "release_year": movie_data['release_year'],
            "imdb": movie_data['imdb'],
            "release_date": movie_data['release_date'],
            "rating": movie_data['rating'],
            "overview": movie_data['overview'],
            "poster_small": movie_data['poster_120x171'],
            "poster_medium": movie_data['poster_240x342'],
            "poster_large": movie_data['poster_400x570'],
            "genres": genres
        }
        return movie

