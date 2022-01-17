from dataclasses import field
from pyexpat import model
from django import forms

from .models import Reviews, Rating, RatingStar


# Благодаря формам можно проверить на валидность передаваемых данных от пользователей
class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        # достаем все звезды из RatingStar, widget - это то, как будет представлена форма в html
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star', )