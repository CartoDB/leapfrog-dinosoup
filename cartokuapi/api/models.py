from django.db import models

import logging

class App(models.Model):
    username = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    oauth_client_id = models.CharField(max_length=64)
    oauth_client_secret = models.CharField(max_length=64)


class Deploy(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    log = models.TextField(default='')
    _logger = None

    def logger(self):
        if self._logger:
            return self._logger

        class DbHandler(logging.StreamHandler):
            def __init__(self, deploy_model):
                logging.StreamHandler.__init__(self)
                self.model = deploy_model

            def emit(self, record):
                msg = self.format(record)
                self.model.log += msg + "\n"
                self.model.save()

        self._logger = logging.Logger(f'deploy:{self.id}')
        self._logger.setLevel(logging.DEBUG)
        handler = DbHandler(self)
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        self._logger.addHandler(handler)

        return self._logger

