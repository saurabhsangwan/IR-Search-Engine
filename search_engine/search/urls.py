from django.urls import path
from search.views import index, search

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='index'),
]
