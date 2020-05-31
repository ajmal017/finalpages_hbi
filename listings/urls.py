from django.urls import path

from . import views

"""
urlpatterns = [
    path('', views.index, name='listings'),             #127.0.0.1:8000/listings -> execute index() which renders templates/listings/listings.html
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
]
"""