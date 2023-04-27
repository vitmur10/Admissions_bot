from django.db import models


# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    social_media_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPE_CHOICES = (
        ('Найчастіші запитання', 'Найчастіші запитання'),
        ('Питання щодо навчання', 'Питання щодо навчання'),
        ('Фінанси', 'Фінанси'),
        ('Приймальна комісія', 'Приймальна комісія'),
    )
    text = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.text