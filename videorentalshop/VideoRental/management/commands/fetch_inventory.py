import logging
import random

import requests
from django.core.management.base import BaseCommand, CommandError
from tenacity import retry, stop_after_attempt
from VideoRental.models import VideoTape


def convert(given_list):
    """Converts list of dictionaries into a plain string.

    Args:
        given_list (): any list.

    Returns:
        str: list changed to string.

    """
    new_list = []
    for item in given_list:
        correct_item = item.get('name')
        new_list.append(correct_item)
    listToStr = ', '.join([str(elem) for elem in new_list])
    return listToStr


class Command(BaseCommand):
    """Command to fetch items (movies) from themoviedb API"""
    help = "Fetch inventory from themoviedb"

    def add_arguments(self, parser):
        """Adds arguments (start & end id of movies)."""
        parser.add_argument("--start-id", type=int, default=0)
        parser.add_argument("--end-id", type=int, default=1)

    def process_response_data(self, data):
        """ Process response data from themoviedb API."""
        return {
            "title": data["original_title"],
            "description": data["overview"],
            "genres": convert(data["genres"]),
            "production_countries": convert(data["production_countries"]),
            "release_date": data["release_date"],
            "vote_average": data["vote_average"],
            "thumbnail": "https://image.tmdb.org/t/p/original" + data["poster_path"],
            "quantity": random.randint(1,10)
        }

    @retry(stop=stop_after_attempt(3))
    def fetch(self, url):
        """ If an exception is thrown inside this function, the query (fetch) will be repeated (maximum 3 times)."""
        return requests.get(url)

    def fetch_items(self, start_id, end_id):
        """ Fetch items (movies) from themoviedb API.

        Args:
            start_id (): beginning of the range of movie ID's.
            end_id (): end of the range of movie ID's.
        """
        for movie_id in range(start_id, end_id):
            response = self.fetch(
                f"https://api.themoviedb.org/3/movie/"
                f"{movie_id}?api_key=6b75a2b772a76c265d6d9de64e1f59c3"
            )
            if response.ok:
                yield self.process_response_data(response.json())
            else:
                logging.warning("Unable to load movie with id %s", movie_id)

    def handle(self, *args, **options):
        """ Create a new product with the get_or_create method. It allows to avoid adding a movie with the same title
        multiple times. """
        for item in self.fetch_items(
            options["start_id"],
            options["end_id"]
        ):
            title = item.pop("title")
            _, created = VideoTape.objects.get_or_create(
                title=title,
                defaults=item
            )
            if created:
                logging.info("New video added titled: %s", title)
