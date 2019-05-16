from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    username =  models.CharField(max_length=255, unique=True, default="")
    last_name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    dt_login = models.DateTimeField(auto_now_add=True)

    class meta:
        unique_together = (("username", "email"),)

    def __str__(self):
        return "{}- {}".format(self.username, self.email)
