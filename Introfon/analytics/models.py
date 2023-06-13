from django.db import models

# Create your models here.


class Analytics_User(models.Model):
    quantity_user = models.IntegerField()
    data = models.DateTimeField(auto_now=True)


class Analytics_actions(models.Model):
    clicks_quantity = models.IntegerField()
    button_clicks = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

