from django.db import models


class App(models.Model):
    username = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    oauth_client_id = models.CharField(max_length=64)
    oauth_client_secret = models.CharField(max_length=64)


class Deploy(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    log = models.TextField(default='')
