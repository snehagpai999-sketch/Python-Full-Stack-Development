from django.core.management.base import BaseCommand
from reviews.models import Movie

SAMPLE_MOVIES = [
    ("Inception", "A skilled thief enters dreams to steal secrets and is offered a chance at redemption.", "Sci-Fi", 2010, "Christopher Nolan", "English", "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg"),
    ("Interstellar", "A team travels beyond this galaxy to find a future for humanity.", "Sci-Fi", 2014, "Christopher Nolan", "English", "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"),
    ("The Dark Knight", "Batman faces a criminal mastermind who plunges Gotham into chaos.", "Action", 2008, "Christopher Nolan", "English", "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"),
    ("Parasite", "A poor family schemes to become employed by a wealthy household.", "Thriller", 2019, "Bong Joon-ho", "Korean", "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"),
    ("The Grand Budapest Hotel", "A legendary concierge and his lobby boy become involved in a mystery.", "Comedy", 2014, "Wes Anderson", "English", "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg"),
    ("Spirited Away", "A young girl enters a mysterious world of spirits.", "Animation", 2001, "Hayao Miyazaki", "Japanese", "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg"),
    ("Get Out", "A young man visits his girlfriend's family and uncovers a disturbing secret.", "Horror", 2017, "Jordan Peele", "English", "https://image.tmdb.org/t/p/w500/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg"),
    ("La La Land", "A musician and an aspiring actor fall in love in Los Angeles.", "Romance", 2016, "Damien Chazelle", "English", "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"),
]

class Command(BaseCommand):
    help = "Add sample movies to the database"

    def handle(self, *args, **options):
        created_count = 0
        for title, description, genre, year, director, language, poster in SAMPLE_MOVIES:
            _, created = Movie.objects.get_or_create(
                title=title,
                defaults={
                    "description": description, "genre": genre,
                    "release_year": year, "director": director,
                    "language": language, "poster_url": poster,
                },
            )
            created_count += int(created)
        self.stdout.write(self.style.SUCCESS(f"Sample movie setup complete. Added {created_count} movies."))
