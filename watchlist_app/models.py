from platform import platform
from statistics import mode
from turtle import title
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class StremVideos (models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=150)

    def __str__(self):
        return self.name


class WatchList (models.Model):
    title = models.CharField(max_length=255)
    storyline = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_of_rating = models.IntegerField(default=0)
    platform = models.ForeignKey(
        StremVideos, on_delete=models.CASCADE, related_name="watchlist")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review (models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=255)
    WatchList = models.ForeignKey(
        WatchList, on_delete=models.CASCADE, related_name='Review')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.Rating) + " " + self.WatchList.title
