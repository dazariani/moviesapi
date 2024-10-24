from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Actor(models.Model):
  name = models.CharField(max_length=70, blank=True)
  

  def __str__(self):
    return f'{self.name}'
  


class Genre(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name
  

class Director(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name  
  

class Movie(models.Model):
  title = models.CharField(max_length=50)
  year = models.IntegerField()
  genre = models.ManyToManyField(Genre, related_name='movies')
  rating = models.DecimalField(max_digits=4, decimal_places=2)
  director = models.ManyToManyField(Director, related_name='movies')
  actors = models.ManyToManyField(Actor, related_name='movies')
  poster = models.ImageField(upload_to='images/posters/', blank=True, default='images/posters/default.jpeg')
  country = models.CharField(max_length=20)
  language = models.CharField(max_length=20)
  plot = models.TextField(max_length=350, blank=True)
  url = models.CharField(max_length=500, blank=True)

  class Meta:
    ordering = ["id"]

  def __str__(self):
    return f'{self.title + " " + str(self.rating)}'
  

class CustomUser(AbstractUser):
  avatar = models.ImageField(upload_to='images/users/', blank=True, default='images/users/default.png')
  bookmarked = models.ManyToManyField(Movie, related_name="movie", blank=True, default=False)

  def __str__(self):
    return self.username
