from django.db import models


class CalcOperation(models.Model):
    date = models.DateTimeField()
    first = models.IntegerField()
    second = models.IntegerField()
    result = models.IntegerField()
