from django.db import models


class Human(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    age = models.IntegerField()
