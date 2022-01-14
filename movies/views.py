from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Movie
from .forms import ReviewForm


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


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # commit=False приостанавливает хранение формы, чтобы мы могли внести изменения в форму
            form.movie = movie
            form.save()  # теперь данные из формы будут сохранены в БД
        return redirect(movie.get_absolute_url())
