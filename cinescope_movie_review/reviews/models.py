from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

class Movie(models.Model):
    GENRES = [
        ("Action", "Action"), ("Adventure", "Adventure"), ("Animation", "Animation"),
        ("Comedy", "Comedy"), ("Crime", "Crime"), ("Drama", "Drama"),
        ("Fantasy", "Fantasy"), ("Horror", "Horror"), ("Romance", "Romance"),
        ("Sci-Fi", "Sci-Fi"), ("Thriller", "Thriller"), ("Documentary", "Documentary"),
    ]
    title = models.CharField(max_length=160)
    description = models.TextField()
    genre = models.CharField(max_length=30, choices=GENRES)
    release_year = models.PositiveIntegerField()
    director = models.CharField(max_length=120, blank=True)
    language = models.CharField(max_length=60, default="English")
    poster_url = models.URLField(blank=True, help_text="Optional image URL for the movie poster")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        result = self.reviews.aggregate(value=Avg("rating"))["value"]
        return round(result, 1) if result is not None else None

    @property
    def review_count(self):
        return self.reviews.count()


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movie_reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    title = models.CharField(max_length=120)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["movie", "user"], name="one_review_per_user_per_movie")
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.rating}/10 by {self.user}"


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="one_watchlist_entry_per_user_movie")
        ]
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user} - {self.movie}"
