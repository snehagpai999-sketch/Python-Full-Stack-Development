from django.contrib import admin
from .models import Movie, Review, Watchlist

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "release_year", "language")
    search_fields = ("title", "director")
    list_filter = ("genre", "release_year", "language")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("movie__title", "user__username", "title")

admin.site.register(Watchlist)
