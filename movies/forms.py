from pyexpat import model
from django import forms

from .models import Reviews


# Благодаря формам можно проверить на валидность передаваемых данных от пользователей
class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')