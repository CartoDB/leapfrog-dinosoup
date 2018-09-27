from django.db import models

# Create your models here.
class Deploy(models.Model):
    app = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
