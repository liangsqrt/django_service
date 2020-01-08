from django.db import models

# Create your models here.


class question(models):
    num = models.CharField()
    title = models.CharField()
    question = models.CharField()
    answer = models.CharField()
