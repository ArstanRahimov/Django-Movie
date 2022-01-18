from tabnanny import verbose
from django.db import models


class Contact(models.Model):
    """Подписка по email"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)  # дата подписки

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.email
