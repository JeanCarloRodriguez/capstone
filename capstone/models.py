from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Merchandise(models.Model):

    user = models.ForeignKey(User, related_name="merchandise", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    title = models.CharField(max_length=64)
    description = models.TextField()
    quantity = models.IntegerField()
    acquisition_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AcquisitionCost(models.Model):
    pass