from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ReviewForm
from .models import Movie, Review, Watchlist

def home(request):
    movies = Movie.objects.all()
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "")
    year = request.GET.get("year", "")
    sort = request.GET.get("sort", "title")

    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(director__icontains=query) | Q(description__icontains=query))
    if genre:
        movies = movies.filter(genre=genre)
    if year.isdigit():
        movies = movies.filter(release_year=year)

    if sort == "newest":
        movies = movies.order_by("-release_year", "title")
    elif sort == "oldest":
        movies = movies.order_by("release_year", "title")
    elif sort == "rating":
        movies = movies.annotate(avg_rating=Avg("reviews__rating")).order_by("-avg_rating", "title")

    return render(request, "reviews/home.html", {
        "movies": movies,
        "genres": Movie.GENRES,
        "query": query,
        "selected_genre": genre,
        "selected_year": year,
        "selected_sort": sort,
    })

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.reviews.select_related("user")
    user_review = None
    in_watchlist = False
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()
    form = ReviewForm(instance=user_review)
    return render(request, "reviews/movie_detail.html", {
        "movie": movie, "reviews": reviews, "form": form,
        "user_review": user_review, "in_watchlist": in_watchlist,
    })

@login_required
def save_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    existing = Review.objects.filter(movie=movie, user=request.user).first()
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been saved.")
        else:
            messages.error(request, "Please correct the review form.")
    return redirect("movie_detail", pk=pk)

@login_required
@require_POST
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    movie_id = review.movie_id
    review.delete()
    messages.success(request, "Your review has been deleted.")
    return redirect("movie_detail", pk=movie_id)

@login_required
@require_POST
def toggle_watchlist(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    item, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        item.delete()
        messages.info(request, "Movie removed from your watchlist.")
    else:
        messages.success(request, "Movie added to your watchlist.")
    return redirect("movie_detail", pk=pk)

@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user=request.user).select_related("movie")
    return render(request, "reviews/watchlist.html", {"items": items})

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related("movie")
    return render(request, "reviews/my_reviews.html", {"reviews": reviews})
