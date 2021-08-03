from django.db import models


class User(models.Model):
    external_id = models.IntegerField()
    username = models.CharField(max_length=255,  blank=True, null=True)
    weather_pass = models.BooleanField(unique=False, default=False)

    def __str__(self):
        return str(self.username)
