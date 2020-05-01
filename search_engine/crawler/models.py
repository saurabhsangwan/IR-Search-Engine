from django.db import models

# Create your models here.
class TextData(models.Model):
    url = models.CharField(blank=False, max_length=255)
    text = models.TextField(blank=False, null=False)