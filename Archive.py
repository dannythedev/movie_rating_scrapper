import json

from Cinemas.YesPlanet import YesPlanet
from Reviewers.IMDB import IMDB
from Reviewers.Metacritic import Metacritic
import threading

from Reviewers.RottenTomatoes import RottenTomatoes


class Archive:
    def __init__(self):
        self.movies = YesPlanet().get_movies()
        self.reviewers = [Metacritic(), RottenTomatoes(), IMDB()]
        self.progress = 0

    def initialize(self):
        """Initializes the module."""
        self.get_movies_data()
        self.sort_by_rating()
        self.export_json()

    def get_movies_data(self):
        """Gets the movie data from all the critics."""
        threads = []
        for reviewer in self.reviewers:
            thread = threading.Thread(target=reviewer.initialize, args=[self.movies])
            threads.append(thread)
        for thread in threads:
            thread.join()

    def get_progress(self):
        """Gets progress of current pages scanned against total pages."""
        current = sum([reviewer.progress for reviewer in self.reviewers])
        total = len(self.movies) * (len(self.reviewers))
        return int(current / total * 100)

    def sort_by_rating(self):
        """Calculates total rating for each movie in Archive, then sorts them by this value."""
        [movie.accumulate_rating() for movie in self.movies]
        self.movies = sorted(self.movies, key=lambda d: d.total_rating, reverse=True)

    def export_json(self):
        """Exports data as a JSON file."""
        dumps = json.dumps([movie.__dict__ for movie in self.movies], indent=4)
        f = open('movies.json', 'w')
        f.write(dumps)
        f.close()
