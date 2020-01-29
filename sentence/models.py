from django.db import models


class Sentence(models.Model):
    is_show = models.BooleanField(default=False)
    content = models.CharField(max_length=50)
