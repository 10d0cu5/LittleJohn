from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Account(User):
    watchlist = models.TextField(null=False, blank=False)
