from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    class Types(models.TextChoices):
        WEBSITE = 'website'
        BOOK = 'book'
        ARTICLE = 'article'
        MUSIC = 'music'
        VIDEO = 'video'

    title = models.CharField(max_length=255, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    image = models.URLField(blank=True)
    type = models.CharField(max_length=10, choices=Types.choices, default=Types.WEBSITE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owners = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='links')
    collections = models.ManyToManyField(to='Collection', blank=True, related_name='links')

    objects = models.Manager()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owners = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="collections", null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title
