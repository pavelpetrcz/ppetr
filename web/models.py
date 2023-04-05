from django.db import models


class Blogpost(models.Model):
    title = models.CharField(max_length=1000)
    summary = models.CharField(max_length=1000)
    image_url = models.URLField()
    body = models.TextField()
