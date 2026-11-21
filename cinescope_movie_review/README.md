# CineScope – Movie Review & Recommendation Platform

A Django full-stack starter project featuring movie discovery, search and filters, user accounts, movie reviews, ratings, personal watchlists, and Django admin management.

## Requirements
- Python 3.10 or newer
- pip
- Internet connection for Google Fonts and remote sample poster images (optional)

## Windows PowerShell setup

Open PowerShell in the extracted `cinescope_movie_review` folder.

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_movies
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

If PowerShell blocks activation, run this once in the same terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

You can also skip activation and use:
```powershell
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_movies
py manage.py runserver
```

## First use
1. Register a user from the website.
2. Log in and open a movie.
3. Submit one review per movie per account. You can edit your own review by submitting the form again.
4. Add movies to your watchlist.
5. Sign in to `/admin/` with the superuser account to add/edit movies and moderate reviews.

## Add movies
Use Django Admin (`/admin/`) → Movies → Add Movie. A poster URL is optional.
You can also rerun `python manage.py seed_movies`; it will not duplicate the sample titles.

## Features included
- Responsive dark movie discovery interface
- Registration, login and logout
- Movie search by title, director and description
- Genre, year and sort filters
- Movie detail pages
- One review per user per movie, with update/delete
- Ratings from 1 to 10 and average movie ratings
- Personal watchlist
- Personal review history
- Django admin for movie and review management

## Notes
- SQLite is configured by default for easy local development.
- Sample poster images use remote image URLs. If an image is unavailable, the movie title still appears.
- This is a development project. Before public deployment, set a secure environment-based SECRET_KEY, set DEBUG=False, configure ALLOWED_HOSTS, HTTPS, static/media hosting and production database settings.
