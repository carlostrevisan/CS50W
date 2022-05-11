import black
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    username = models.CharField(max_length=30)
    post_body = models.CharField(max_length=144, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()

    def __str__(self):
        return self.post_body

