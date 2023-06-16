from django.db import models


# Create your models here.


class Analytics_User(models.Model):
    quantity_user = models.IntegerField()
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Аналітика користувачі'
        verbose_name_plural = 'Аналітика користувачі'


class Analytics_actions(models.Model):
    clicks_quantity = models.IntegerField()
    button_clicks = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Аналітика дії'
        verbose_name_plural = 'Аналітика дії'
