from django.db import models


# Create your models here.


class Conversion(models.Model):
    model_id = models.IntegerField()
    value = models.FloatField()
