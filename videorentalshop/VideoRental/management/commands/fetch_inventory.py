import logging
import requests
from django.core.management.base import BaseCommand, CommandError
from tenacity import retry, stop_after_attempt
from VideoRental.models import VideoTape


class Command(BaseCommand):
    help = "Fetch inventory from themoviedb"

    def add_arguments(self, parser):
        parser.add_argument("--start-id", type=int, default=0)
        parser.add_argument("--end-id", type=int, default=1)

    def process_response_data(self, data):
        return {
            "title": data["original_title"],
            "description": data["overview"],
            "genres": data["genres"],
            "production_countries": data["production_countries"],
            "release_date": data["release_date"],
            "vote_average": data["vote_average"],
            "thumbnail": "https://image.tmdb.org/t/p/original" + data["poster_path"]
        }

    @retry(stop=stop_after_attempt(3))
    def fetch(self, url):
        return requests.get(url)

    def fetch_items(self, start_id, end_id):
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
