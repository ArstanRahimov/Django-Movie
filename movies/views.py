from pyexpat import model
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset =  Movie.objects.filter(draft=False)  # чтобы не выводились черновики

    # template_name = 'movies/movies.html'
    # мы не указыаем template, так он автоматически добавляет к названию модели суффикс _list и ищет template с таким названием (movie_list.html)


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'  # отвечает за то, по какому полю нужно искать запись

    # мы не указыаем template, так он автоматически добавляет к названию модели суффикс _detail и ищет template с таким названием (movie_detail.html)
