from django import template
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Actor, Category, Movie, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset =  Movie.objects.filter(draft=False)  # чтобы не выводились черновики

    # template_name = 'movies/movies.html'
    # мы не указыаем template, так он автоматически добавляет к названию модели суффикс _list и ищет template с таким названием (movie_list.html)


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'  # отвечает за то, по какому полю нужно искать запись

    # мы не указываем template, так он автоматически добавляет к названию модели суффикс _detail и ищет template с таким названием (movie_detail.html)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # commit=False приостанавливает хранение формы, чтобы мы могли внести изменения в форму
            if request.POST.get('parent', None):  # ключ parent это name="parent" в html
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()  # теперь данные из формы будут сохранены в БД
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'  # поле, по которому будем искать актеров


class FilterMoviesView(GenreYear, ListView):
    """Фильтрация фильмов"""
    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist('year')) | Q(genres__in=self.request.GET.getlist('genre'))
        )
        return queryset


class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):  # метод для получения IP-адреса клиента
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(  # если запись уже была создана - то она обновится
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
